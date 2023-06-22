import csv
from dataclasses import dataclass
import logging
from typing import Optional
from app.adapter import database

@dataclass
class SimilarPost:
    id: str
    score: str
    title: Optional[str] = None
    text: Optional[str] = None
    community_id: Optional[str] = None

def get_similar_content(query: str, max_results: int = 3, max_relevance_score: float = 1):
    docs = database.FAISS_DB.similarity_search_with_score(query, k=max_results)

    for doc in docs:
        if doc[1] >= max_relevance_score:
            break

        yield SimilarPost(
            id=doc[0].metadata["id"],
            score=str(doc[1]),
            title=doc[0].metadata["title"],
            text=doc[0].metadata["text"],
            community_id=doc[0].metadata["community_id"]
        )