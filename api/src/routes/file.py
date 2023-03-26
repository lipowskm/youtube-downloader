import asyncio
from pathlib import Path

from fastapi import APIRouter, HTTPException
from sqlmodel import select
from fastapi.responses import FileResponse
from fastapi.websockets import WebSocket, WebSocketDisconnect

from ..db import ActiveSession
from ..models import File

router = APIRouter()


@router.get("/file/{file_id}", status_code=200)
def get_file(file_id: str, session: ActiveSession) -> FileResponse:
    """Returns .mp3 file to user."""
    statement = select(File).where(File.id == file_id)
    file = session.exec(statement).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    headers = {'Content-Disposition': f'attachment; filename="{Path(file.path).name}"'}
    return FileResponse(file.path, headers=headers)


@router.websocket("/notify/{file_id}/ws")
async def notify(websocket: WebSocket, file_id: str, session: ActiveSession):
    try:
        await websocket.accept()
        statement = select(File).where(File.id == file_id)
        while not (file := session.exec(statement).first()):
            await asyncio.sleep(1)
        await websocket.send_json(file.json())
        await websocket.close()
    except WebSocketDisconnect:
        await websocket.close()
