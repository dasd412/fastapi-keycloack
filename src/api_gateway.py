from fastapi import APIRouter

from domain.system_setting.router import system_setting_router

basic_router = APIRouter()

"""
router가 추가될 때마다 여기에 추가하세요
"""
basic_router.include_router(system_setting_router)
