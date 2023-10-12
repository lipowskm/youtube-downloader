from src.handlers import YoutubeHandler

youtube_url = "https://www.youtube.com/watch?v=__NeP0RqACU"


def test_is_valid_url() -> None:
    assert YoutubeHandler.is_valid_url(youtube_url)
    assert not YoutubeHandler.is_valid_url(
        "https://www.youtube.com/watch?v=12345678901"
    )
    assert not YoutubeHandler.is_valid_url("https://www.youtube.com/watch?v=123")
    assert not YoutubeHandler.is_valid_url("https://www.google.com/watch?v=123")
