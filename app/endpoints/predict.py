import logging
from typing import Any
from app.endpoints.models import CommunityRecommendationsRequest, GuessAnswerRequest, GuessQuestionRequest, SimilarPostsRequest

from starlette.requests import Request
from starlette.responses import Response

from app.usecase.answers import get_answer
from app.usecase.community import get_community_recommendation
from app.usecase.similar_content import get_similar_content

from fastapi import APIRouter, Header

from app.usecase.predict import find_questions, has_questions, predict

router = APIRouter(
    prefix="",
    tags=["predict"],
)


@router.post("/guess-question", status_code=200)
def api_analyse_stream(guess_question: GuessQuestionRequest) -> Any:
    response = has_questions(query=guess_question.query)
    return response

@router.post("/guess-questions", status_code=200)
async def api_analyse_stream(guess_questions: GuessQuestionRequest) -> Any:
    response = find_questions(query=guess_questions.query)
    return response

@router.post("/post/search-similar", status_code=200)
async def search_similar_content(similar_post: SimilarPostsRequest) -> Any:
    response = get_similar_content(query=similar_post.query, max_relevance_score=float(similar_post.max_relevance_score))
    return response

@router.post("/post/community-recommendations", status_code=200)
async def community_recommendations(community_recommendation_request: CommunityRecommendationsRequest, request: Request) -> Any:
    authorization = request.headers.get("Authorization")

    if not authorization:
        response = Response()
        response.status_code = 401
        return response

    jwt = authorization[len("Bearer "):]
    return get_community_recommendation(jwt, community_recommendation_request.query)

@router.post("/guess-query-answer", status_code=200)
def guess_query_answer(guess_request: GuessAnswerRequest, request: Request, response: Response) -> Any:
    authorization = request.headers.get("Authorization")

    if not authorization:
        response.status_code = 401
        return
    jwt = authorization[len("Bearer "):]
    return get_answer(jwt, guess_request.query)
