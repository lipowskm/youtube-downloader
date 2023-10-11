from redis import Redis
from rq import Queue

from ..config import settings
from .jobs import convert_youtube_url_to_mp3, delete_all_files_older_than

redis_conn = Redis(host=settings.redis.host, port=settings.redis.port)
default_queue = Queue(name="default", connection=redis_conn)
high_queue = Queue(name="high", connection=redis_conn)


def get_redis():
    yield redis_conn


def get_default_queue():
    yield default_queue
