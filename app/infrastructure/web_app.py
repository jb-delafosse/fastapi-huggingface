

from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from app.endpoints import predict


def create_app() -> FastAPI:
    app = FastAPI(redoc_url="/redoc")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(predict.router)
    load_dotenv()
    return app
