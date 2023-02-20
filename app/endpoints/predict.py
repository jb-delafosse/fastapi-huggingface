import logging
from typing import Any, Dict

from fastapi import APIRouter

from app.usecase.predict import predict

router = APIRouter(
    prefix="/predict",
    tags=["predict"],
)


@router.get("", status_code=200)
async def api_analyse_stream(input: str) -> Any:
    response = await predict(input=input)
    logging.info(response)
    return response
