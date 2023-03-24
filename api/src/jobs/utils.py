from pathlib import Path
import subprocess

from pytube import YouTube


def download_youtube_video(url: str, output_dir: str) -> str:
    """
    Download video from YouTube.

    :param url: URL to YouTube video
    :param output_dir: output directory for video file
    :return: full path to downloaded video file
    """
    return YouTube(url).streams.get_audio_only().download(output_dir)


def convert_video_file_to_mp3(path: str, output_dir: str) -> str:
    base_bath = Path(path)
    input_path = str(base_bath.absolute())
    output_path = str(Path(output_dir) / base_bath.with_suffix(".mp3").name)
    process = subprocess.run(
        [
            "ffmpeg",
            "-i",
            input_path,
            "-q:a",
            "0",
            "-map",
            "a",
            output_path,
        ],
        capture_output=True
    )
    if process.returncode != 0:
        raise
    return output_path
