from api.src.routes import main_router
from fastapi import FastAPI

app = FastAPI()
app.include_router(main_router)
