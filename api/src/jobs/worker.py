from api.src.jobs import redis_conn
from rq import Worker

w = Worker(["default"], connection=redis_conn)
w.work(with_scheduler=True)
