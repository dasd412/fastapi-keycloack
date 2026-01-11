import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

import api_gateway
from core.config.settings import get_settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware)
app.include_router(prefix="/api/v1", router=api_gateway.basic_router)

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=get_settings().uvicorn_port,
        proxy_headers=True,
        forwarded_allow_ips="*",
        reload=get_settings().uvicorn_reload,
    )
