import uuid

from fastapi import APIRouter, Depends
from pydantic import BaseModel
import rq
from rq.job import Retry

from ..jobs import convert_youtube_url_to_mp3, get_queue

router = APIRouter()


class Item(BaseModel):
    file_id: str


@router.get("/convert", status_code=200)
def convert(youtube_url: str, queue: rq.Queue = Depends(get_queue)) -> Item:
    """Fetch YouTube URL from user and queue job to convert it into MP3."""
    file_id = uuid.uuid1().hex
    queue.enqueue(
        convert_youtube_url_to_mp3,
        youtube_url,
        f"/home/lipowskm/muza/{file_id}",
        job_id=file_id,
        retry=Retry(max=3, interval=1),
    )
    return Item(file_id=file_id)
