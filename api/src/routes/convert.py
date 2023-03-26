import uuid

from fastapi import APIRouter
from pydantic import BaseModel
from redis import Redis
from rq.job import Job, Retry
from sqlmodel import Session

from ..db import engine
from ..jobs import convert_youtube_url_to_mp3, queue
from ..models import File

router = APIRouter()


class Item(BaseModel):
    job_id: str


def add_file_to_database(job: Job, connection: Redis, result: str, *_, **__):
    file = File(
        id=job.id,
        path=result,
        youtube_url=job.args[0],
    )
    with Session(engine) as session:
        session.add(file)
        session.commit()
        session.refresh(file)


@router.get("/convert", status_code=200)
def convert(youtube_url: str) -> Item:
    """Fetch YouTube URL from user to convert it into MP3."""
    job_id = uuid.uuid1().hex
    queue.enqueue(
        convert_youtube_url_to_mp3,
        youtube_url,
        f"/home/lipowskm/muza/{job_id}",
        job_id=job_id,
        on_success=add_file_to_database,
        retry=Retry(max=3, interval=1),
    )
    return Item(job_id=job_id)
