

from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from app.endpoints import predict


def create_app() -> FastAPI:
    app = FastAPI(redoc_url="/redoc")
    origins = [
        "http://localhost",
        "http://localhost:8080",
        "http://localhost:9580",
        "http://100.125.89.106:8080",
        "http://100.125.89.106:9580",

    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(predict.router)
    load_dotenv()
    return app
