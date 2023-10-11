from datetime import datetime, timedelta
import glob
import os
from pathlib import Path
import shutil
import tempfile
from typing import Union

from .utils import download_youtube_video, get_mp3_from_video_file


def convert_youtube_url_to_mp3(url: str, output_dir: Union[str, Path]):
    with tempfile.TemporaryDirectory() as tmpdir:
        video_file_path = download_youtube_video(url, tmpdir)
        mp3_path = get_mp3_from_video_file(video_file_path, output_dir)
    return mp3_path


def delete_all_files_older_than(path: str, seconds: int) -> None:
    """
    Deletes all files older than specified as parameter in seconds, in specified directory.

    :param path: path to directory
    :param seconds: maximum allowed file lifetime in seconds
    """
    if not Path(path).is_dir():
        raise ValueError("Specified path is not a path to directory.")
    files = glob.glob(f"{path}/*")
    for f in files:
        ts = Path(f).stat().st_mtime
        modified_at = datetime.fromtimestamp(ts)
        if datetime.now() < (modified_at + timedelta(seconds=seconds)):
            continue
        if Path(f).is_dir():
            shutil.rmtree(f)
        else:
            os.remove(f)
