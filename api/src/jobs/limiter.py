import functools
from typing import Callable

from api.src.jobs import redis_conn
from fastapi import HTTPException, status
from fastapi.requests import Request


def rate_limiter(times: int, seconds: int) -> Callable:
    """
    Decorator for rate limiting endpoint per IP.

    :param times: how many times endpoint can be reached during given interval
    :param seconds: number of seconds after rate limit will reset
    """

    def wrapper(func: Callable):
        @functools.wraps(func)
        def wrapper_func(*args, **kwargs):
            request: Request = kwargs.get("request")
            if not request:
                return func(*args, **kwargs)
            ip = request.client.host
            requests = redis_conn.incr(ip)
            if requests == 1:
                redis_conn.expire(ip, seconds)
                ttl = seconds
            else:
                ttl = redis_conn.ttl(ip)
            if requests > times:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Rate limit reached, please try again after {ttl} seconds.",
                )
            return func(*args, **kwargs)

        return wrapper_func

    return wrapper
