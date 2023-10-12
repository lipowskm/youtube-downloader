from redis import Redis
from rq import Queue

from ..config import settings
from .jobs import delete_all_files_older_than, download_and_convert

redis_conn = Redis(host=settings.redis.host, port=settings.redis.port)
default_queue = Queue(name="default", connection=redis_conn)
high_queue = Queue(name="high", connection=redis_conn)


def get_redis() -> Redis:
    yield redis_conn


def get_default_queue() -> Queue:
    yield default_queue
