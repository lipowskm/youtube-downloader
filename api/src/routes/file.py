import asyncio
from pathlib import Path
import shutil
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.websockets import WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from redis.client import Redis
from rq.command import send_stop_job_command
from rq.exceptions import NoSuchJobError
from rq.job import Job, JobStatus
from websockets.exceptions import ConnectionClosedOK

from ..config import settings
from ..jobs import get_redis

router = APIRouter()


class FileJob(BaseModel):
    id: str
    status: str
    queue_position: Optional[int] = None


@router.get("/file/{file_id}", status_code=200)
def get_file(file_id: str, redis: Redis = Depends(get_redis)) -> FileResponse:
    """Returns file to user."""
    try:
        job = Job.fetch(id=file_id, connection=redis)
    except NoSuchJobError:
        raise HTTPException(status_code=404, detail="File not found")
    result = job.return_value()
    if result and Path(result).is_file():
        headers = {"Access-Control-Expose-Headers": "Content-Disposition"}
        return FileResponse(result, filename=Path(result).name, headers=headers)
    raise HTTPException(status_code=404, detail="File not found")


@router.websocket("/notify/{file_id}/ws")
async def notify(
    websocket: WebSocket, file_id: str, redis: Redis = Depends(get_redis)
) -> None:
    """Send job status on each change until the job has finished."""

    async def send_message(job: Job) -> None:
        message = FileJob(
            id=job.id,
            status=job.get_status(refresh=True).lower(),
            queue_position=job.get_position(),
        ).dict()
        await websocket.send_json(message)

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
            await send_message(job)
            await asyncio.sleep(1)
        await send_message(job)
        await websocket.close()
    except (WebSocketDisconnect, ConnectionClosedOK):
        send_stop_job_command(redis, job.id)
        job.delete()
        shutil.rmtree(Path(settings.output_dir) / job.id, ignore_errors=True)
        await websocket.close(code=1001)
