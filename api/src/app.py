from fastapi import FastAPI

from api.src.db import create_db_and_tables, engine
from api.src.routes import main_router

app = FastAPI()
app.include_router(main_router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables(engine)
