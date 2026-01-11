from fastapi import APIRouter,status

router = APIRouter(prefix="/hello")


@router.get(path="",
            response_model_exclude_none=True,
            status_code=status.HTTP_200_OK)
def get_hello():
    return {"message": "Hello World"}
