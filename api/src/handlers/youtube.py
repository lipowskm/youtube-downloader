from pytube import YouTube
from pytube.exceptions import RegexMatchError, VideoUnavailable
from unidecode import unidecode

from .base import BaseHandler


class YoutubeHandler(BaseHandler):
    @staticmethod
    def download_file(url: str, output_dir: str) -> str:
        """
        Download video from YouTube.

        :param url: URL to YouTube video
        :param output_dir: output directory to save video file
        :return: full path to downloaded video file
        """
        stream = YouTube(url).streams.get_audio_only()
        filename = unidecode(stream.default_filename)
        return stream.download(
            output_dir, filename=filename, max_retries=3, timeout=120
        )

    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Checks whether URL points to valid media file."""
        try:
            YouTube(url).streams
            return True
        except (RegexMatchError, VideoUnavailable):
            return False
