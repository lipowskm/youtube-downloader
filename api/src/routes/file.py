import asyncio
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.websockets import WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from redis.client import Redis
from rq.exceptions import NoSuchJobError
from rq.job import Job, JobStatus

from ..jobs import get_redis

router = APIRouter()


class FileJob(BaseModel):
    id: str
    status: str
    queue_position: Optional[int] = None


@router.get("/file/{file_id}", status_code=200)
def get_file(file_id: str, redis: Redis = Depends(get_redis)) -> FileResponse:
    """Returns .mp3 file to user."""
    try:
        job = Job.fetch(id=file_id, connection=redis)
    except NoSuchJobError:
        raise HTTPException(status_code=404, detail="File not found")
    result = job.return_value()
    if result and Path(result).is_file():
        headers = {"Content-Disposition": f'attachment; filename="{Path(result).name}"'}
        return FileResponse(result, headers=headers)
    raise HTTPException(status_code=404, detail="File not found")


@router.websocket("/notify/{file_id}/ws")
async def notify(
    websocket: WebSocket, file_id: str, redis: Redis = Depends(get_redis)
) -> None:
    """Send job status on each change until the job has finished."""
    last_message = None

    async def send_message(websocket: WebSocket, job: Job):
        nonlocal last_message
        message = FileJob(
            id=job.id,
            status=job.get_status(refresh=True),
            queue_position=job.get_position(),
        ).json()
        if last_message != message:
            await websocket.send_json(message)
            last_message = message

    await websocket.accept()
    try:
        job = Job.fetch(id=file_id, connection=redis)
    except NoSuchJobError:
        await websocket.close(reason="File not found")
        return
    try:
        while job.get_status(refresh=True) not in (
            JobStatus.FINISHED,
            JobStatus.FAILED,
            JobStatus.STOPPED,
            JobStatus.CANCELED,
        ):
            await send_message(websocket, job)
            await asyncio.sleep(1)
        await send_message(websocket, job)
        await websocket.close()
    except WebSocketDisconnect:
        job.delete()
        await websocket.close(code=1001)
