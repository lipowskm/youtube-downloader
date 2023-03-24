from fastapi import APIRouter

from api.src.jobs.jobs import convert_youtube_url_to_mp3

router = APIRouter()


@router.get("/convert")
def convert(youtube_url: str) -> str:
    """Fetch YouTube URL from user to convert it into MP3."""
    raise NotImplementedError
