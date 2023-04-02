import fakeredis
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from rq.job import Job


def test_convert_status_code(api_client: TestClient):
    response = api_client.get(
        "/convert", params={"url": "https://www.youtube.com/watch?v=test"}
    )
    assert response.status_code == 200


def test_convert_returns_file_id(api_client: TestClient):
    response = api_client.get(
        "/convert", params={"url": "https://www.youtube.com/watch?v=test"}
    )
    assert "file_id" in response.json()
    assert response.json().get("file_id")


def test_convert_queues_job(
    api_client: TestClient, redis: fakeredis.FakeStrictRedis, mocker: MockerFixture
):
    mock_convert = mocker.patch("api.src.jobs.jobs.convert_youtube_url_to_mp3")
    mock_convert.return_value = "abc"

    response = api_client.get(
        "/convert", params={"url": "https://www.youtube.com/watch?v=test"}
    )
    mock_convert.assert_called_once()
    file_id = response.json().get("file_id")
    job = Job.fetch(file_id, connection=redis)
    assert job.return_value() == "abc"
