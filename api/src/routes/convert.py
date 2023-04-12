from pathlib import Path
import uuid

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from pydantic import BaseModel
import rq
from rq.job import Retry

from ..config import settings
from ..jobs import convert_youtube_url_to_mp3, get_queue
from ..jobs.limiter import rate_limiter

router = APIRouter()


class Item(BaseModel):
    file_id: str


@router.get("/convert", status_code=200)
@rate_limiter(times=1, seconds=10, whitelist=("127.0.0.1",))
def convert(request: Request, url: str, queue: rq.Queue = Depends(get_queue)) -> Item:
    """Fetch URL from user and queue job to convert it into desired format."""
    file_id = uuid.uuid1().hex
    queue.enqueue(
        convert_youtube_url_to_mp3,
        url,
        Path(settings.output_dir) / file_id,
        job_id=file_id,
        retry=Retry(max=3, interval=1),
    )
    return Item(file_id=file_id)
