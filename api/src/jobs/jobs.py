from pathlib import Path
import tempfile
from typing import Union

from .utils import download_youtube_video, get_mp3_from_video_file


def convert_youtube_url_to_mp3(url: str, output_dir: Union[str, Path]):
    with tempfile.TemporaryDirectory() as tmpdir:
        video_file_path = download_youtube_video(url, tmpdir)
        mp3_path = get_mp3_from_video_file(video_file_path, output_dir)
    return mp3_path
