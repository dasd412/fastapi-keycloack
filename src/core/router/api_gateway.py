from fastapi import APIRouter
from domain.hello.router import hello_router

basic_router=APIRouter()

"""
router가 추가될 때마다 여기에 추가하세요
"""
basic_router.include_router(hello_router)