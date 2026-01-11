from fastapi import APIRouter
from src.hello.router import router

basic_router=APIRouter()

basic_router.include_router(router)