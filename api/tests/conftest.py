from api.src import app
from api.src.jobs import get_queue, get_redis
import fakeredis
from fastapi.testclient import TestClient
import pytest
import rq

server = fakeredis.FakeServer()


def override_get_redis() -> fakeredis.FakeStrictRedis:
    redis = fakeredis.FakeStrictRedis(server=server)
    try:
        yield redis
    finally:
        redis.close()


def override_get_queue() -> rq.Queue:
    redis = fakeredis.FakeStrictRedis(server=server)
    yield rq.Queue(is_async=False, connection=redis)


app.dependency_overrides[get_redis] = override_get_redis
app.dependency_overrides[get_queue] = override_get_queue


@pytest.fixture(scope="function")
def api_client():
    return TestClient(app)


@pytest.fixture(scope="function")
def redis() -> fakeredis.FakeStrictRedis:
    yield fakeredis.FakeStrictRedis(server=server)


@pytest.fixture(scope="function")
def queue() -> rq.Queue:
    redis = fakeredis.FakeStrictRedis(server=server)
    queue = rq.Queue(is_async=False, connection=redis)
    yield queue
    keys = redis.keys("*")
    if keys:
        redis.delete(*keys)
