from fastapi import APIRouter
from domain.hello.router import router

basic_router=APIRouter()

basic_router.include_router(router)