from redis import Redis
from rq import Queue

from ..config import settings
from .jobs import convert_youtube_url_to_mp3

redis_conn = Redis(host=settings.redis.host, port=settings.redis.port)
queue = Queue(connection=redis_conn)


def get_redis():
    yield redis_conn


def get_queue():
    yield queue
