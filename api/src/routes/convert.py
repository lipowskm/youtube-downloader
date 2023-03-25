import uuid

from api.src.db import ActiveSession
from api.src.jobs import convert_youtube_url_to_mp3, queue
from fastapi import APIRouter
from pydantic import BaseModel
from rq.job import Job
from sqlmodel import Session

router = APIRouter()


class Item(BaseModel):
    job_id: str


def add_item_to_database():
    # item = Item(
    #     id=parent_job.id,
    #     path=parent_job.return_value(refresh=True),
    #     status=parent_job.get_status(refresh=True),
    # )
    # session.add(item)
    print("ITEM ADDED")


@router.get("/convert", status_code=200)
def convert(youtube_url: str, session: ActiveSession) -> Item:
    """Fetch YouTube URL from user to convert it into MP3."""
    job_id = uuid.uuid1().hex
    job = queue.enqueue(
        convert_youtube_url_to_mp3,
        youtube_url,
        f"/home/lipowskm/muza/{job_id}",
        job_id=job_id,
    )
    queue.enqueue(add_item_to_database, depends_on=job)
    return Item(job_id=job_id)
