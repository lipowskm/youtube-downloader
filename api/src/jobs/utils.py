from pathlib import Path
import subprocess
from typing import Union

from pytube import YouTube


def download_youtube_video(url: str, output_dir: str) -> str:
    """
    Download video from YouTube.

    :param url: URL to YouTube video
    :param output_dir: output directory to save video file
    :return: full path to downloaded video file
    """
    return (
        YouTube(url)
        .streams.get_audio_only()
        .download(output_dir, max_retries=3, timeout=120)
    )


def get_mp3_from_video_file(
    path: Union[str, Path], output_dir: Union[str, Path]
) -> str:
    """
    Convert any video file type into mp3.

    :param path: path to video file
    :param output_dir: output directory to save mp3 file
    :return: full path to generated mp3
    """
    if isinstance(path, str):
        path = Path(path)
    input_path = str(path.absolute())
    output_path = str(Path(output_dir) / path.with_suffix(".mp3").name)
    process = subprocess.run(
        ["ffmpeg", "-i", input_path, "-q:a", "0", "-map", "a", output_path, "-y"],
        capture_output=True,
    )
    if process.returncode != 0:
        raise
    return output_path
