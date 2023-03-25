from pathlib import Path
import tempfile

from api.src.jobs.utils import download_youtube_video, get_mp3_from_video_file


def convert_youtube_url_to_mp3(url: str, output_dir: str):
    Path(output_dir).mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as tmpdir:
        video_file_path = download_youtube_video(url, tmpdir)
        mp3_path = get_mp3_from_video_file(video_file_path, output_dir)
    return mp3_path
