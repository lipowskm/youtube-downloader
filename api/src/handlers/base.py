from abc import ABC, abstractmethod


class BaseHandler(ABC):
    @staticmethod
    @abstractmethod
    def download_file(url: str, output_dir: str) -> str:
        """Downloads media file from URL and returns path to downloaded file."""
        pass

    @staticmethod
    @abstractmethod
    def is_valid_url(url: str) -> bool:
        """Checks if URL points to valid media file source."""
        pass
