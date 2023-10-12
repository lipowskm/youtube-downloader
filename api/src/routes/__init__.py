from fastapi import APIRouter

from .convert import router as convert_router
from .file import router as file_router

main_router = APIRouter()
main_router.include_router(convert_router, tags=["convert"])
main_router.include_router(file_router, tags=["file"])


@main_router.get("/")
async def index() -> dict:
    return {"message": "Hello World!"}
