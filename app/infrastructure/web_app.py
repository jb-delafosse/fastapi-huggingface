

from fastapi import FastAPI

from app.endpoints import predict


def create_app() -> FastAPI:
    app = FastAPI(redoc_url="/redoc")
    app.include_router(predict.router)
    return app
