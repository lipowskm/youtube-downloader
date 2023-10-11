from contextlib import asynccontextmanager
from datetime import datetime

from api.src.config import settings
from api.src.dashboard import register_rq_dashboard
from api.src.jobs import delete_all_files_older_than, high_queue, redis_conn
from api.src.routes import main_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rq_scheduler import Scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    register_rq_dashboard(
        app,
        redis_url=f"redis://{settings.redis.host}:{settings.redis.port}",
        endpoint=settings.rq_dashboard.endpoint,
        username=settings.rq_dashboard.username,
        password=settings.rq_dashboard.password,
    )
    scheduler = Scheduler(connection=redis_conn, queue=high_queue)
    job = scheduler.schedule(
        scheduled_time=datetime.utcnow(),
        interval=60,
        func=delete_all_files_older_than,
        kwargs={
            "path": settings.output_dir,
            "seconds": settings.delete_files_older_than_seconds,
        },
    )
    yield
    scheduler.cancel(job)


app = FastAPI(lifespan=lifespan)
app.include_router(main_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
