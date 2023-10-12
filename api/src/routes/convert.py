from pathlib import Path
import uuid

from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from pydantic import BaseModel
import rq
from rq.job import Retry

from ..config import settings
from ..handlers import UnsupportedDomainError, get_handler
from ..jobs import download_and_convert, get_default_queue
from ..jobs.limiter import rate_limiter

router = APIRouter()


class Item(BaseModel):
    file_id: str


@rate_limiter(times=1, seconds=10, whitelist=("127.0.0.1",))
@router.get("/convert", status_code=200)
def convert(
    request: Request, url: str, queue: rq.Queue = Depends(get_default_queue)
) -> Item:
    """Fetch URL from user and queue job to convert it into desired format."""
    try:
        handler = get_handler(url)
    except (ValueError, UnsupportedDomainError) as e:
        raise HTTPException(status_code=404, detail=str(e))
    file_id = uuid.uuid1().hex
    queue.enqueue(
        download_and_convert,
        handler,
        url,
        Path(settings.output_dir) / file_id,
        job_id=file_id,
        retry=Retry(max=3, interval=1),
    )
    return Item(file_id=file_id)
