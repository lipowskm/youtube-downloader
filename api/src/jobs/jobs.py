import tempfile
from pathlib import Path

from api.src.jobs.utils import download_youtube_video, convert_video_file_to_mp3


def convert_youtube_url_to_mp3(url: str, output_dir: str):
    Path(output_dir).mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as tmpdir:
        video_file_path = download_youtube_video(url, tmpdir)
        mp3_path = convert_video_file_to_mp3(video_file_path, output_dir)
    return mp3_path
