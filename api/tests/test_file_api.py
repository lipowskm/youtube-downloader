import tempfile

from api.src.routes.file import FileJob
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocketDisconnect
import pytest
import rq
from rq.job import JobStatus


def task(return_value: str) -> str:
    return return_value


def test_get_file(api_client: TestClient, queue: rq.Queue) -> None:
    with tempfile.NamedTemporaryFile() as file:
        job = queue.enqueue(task, file.name, job_id="abc")
        assert job.get_status() == JobStatus.FINISHED
        response = api_client.get("/file/abc")
        assert response.status_code == 200


def test_get_file_when_job_failed(api_client: TestClient, queue: rq.Queue) -> None:
    job = queue.enqueue(task, job_id="abc")
    assert job.get_status() == JobStatus.FAILED
    response = api_client.get("/file/abc")
    assert response.status_code == 404


def test_get_file_when_job_not_existing(api_client: TestClient) -> None:
    response = api_client.get("/file/abc")
    assert response.status_code == 404


def test_get_file_when_file_not_existing(
    api_client: TestClient, queue: rq.Queue
) -> None:
    job = queue.enqueue(task, "file", job_id="abc")
    assert job.get_status() == JobStatus.FINISHED
    response = api_client.get("/file/abc")
    assert response.status_code == 404


def test_notify(api_client: TestClient, queue: rq.Queue) -> None:
    with tempfile.NamedTemporaryFile() as file:
        job = queue.enqueue(task, file.name, job_id="abc")
        assert job.get_status() == JobStatus.FINISHED
        with api_client.websocket_connect("/notify/abc/ws") as websocket:
            response = websocket.receive_json()
            assert FileJob(**response) == FileJob(
                id="abc", status=JobStatus.FINISHED, queue_position=None
            )


def test_notify_when_job_failed(api_client: TestClient, queue: rq.Queue) -> None:
    job = queue.enqueue(task, job_id="abc")
    assert job.get_status() == JobStatus.FAILED
    with api_client.websocket_connect("/notify/abc/ws") as websocket:
        response = websocket.receive_json()
        assert FileJob(**response) == FileJob(
            id="abc", status=JobStatus.FAILED, queue_position=None
        )


def test_notify_when_job_running(api_client: TestClient, queue: rq.Queue) -> None:
    # TODO: Find a way to test this
    pass


def test_notify_when_job_not_existing(api_client: TestClient) -> None:
    with pytest.raises(WebSocketDisconnect), api_client.websocket_connect(
        "/notify/abc/ws"
    ) as websocket:
        websocket.receive_json()
