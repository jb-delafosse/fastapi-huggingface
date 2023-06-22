import logging
from typing import Any

from starlette.requests import Request
from starlette.responses import Response

from app.usecase.answers import get_answer
from app.usecase.similar_content import get_similar_content

from fastapi import APIRouter

from app.usecase.predict import predict

router = APIRouter(
    prefix="",
    tags=["predict"],
)


@router.get("/predict", status_code=200)
async def api_analyse_stream(input: str) -> Any:
    response = await predict(input=input)
    logging.info(response)
    return response

@router.get("/content/search", status_code=200)
async def search_similar_content(query: str) -> Any:
    response = get_similar_content(query=query)
    return response


@router.get("/guess-query-answer", status_code=200)
def guess_query_answer(query: str, request: Request, response: Response) -> Any:
    authorization = request.headers.get("Authorization")
    if not authorization:
        response.status_code = 401
        return
    jwt = authorization[len("Bearer :"):]
    get_answer(jwt, query)
