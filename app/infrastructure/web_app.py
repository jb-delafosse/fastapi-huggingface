

from fastapi import FastAPI
from dotenv import load_dotenv

from app.endpoints import predict


def create_app() -> FastAPI:
    app = FastAPI(redoc_url="/redoc")
    app.include_router(predict.router)
    load_dotenv()
    return app
