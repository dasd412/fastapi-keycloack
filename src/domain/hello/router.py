from fastapi import APIRouter,status

hello_router = APIRouter(prefix="/hello")


@hello_router.get(path="",
            response_model_exclude_none=True,
            status_code=status.HTTP_200_OK)
def get_hello():
    return {"message": "Hello World"}
