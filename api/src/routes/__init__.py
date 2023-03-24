from api.src.routes import convert
from fastapi import APIRouter

main_router = APIRouter()
main_router.include_router(convert.router, tags=["convert"])


@main_router.get("/")
async def index():
    return {"message": "Hello World!"}
