from pydantic import BaseModel

class CommunityRecommendationsRequest(BaseModel):
    query: str


class SimilarPostsRequest(BaseModel):
    query: str
    max_relevance_score: str

class GuessAnswerRequest(BaseModel):
    query: str

class GuessQuestionRequest(BaseModel):
    query: str


class QuestionDto(BaseModel):
    questions: list[str]