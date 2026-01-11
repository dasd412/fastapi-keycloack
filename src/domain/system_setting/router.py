from fastapi import APIRouter, status

system_setting_router = APIRouter(prefix="/system_setting")


@system_setting_router.get(
    path="", response_model_exclude_none=True, status_code=status.HTTP_200_OK
)
def get():
    return {"message": "Hello World"}
