from rq import Worker

from api.src.jobs import redis_conn

w = Worker(['default'], connection=redis_conn)
w.work(with_scheduler=True)
