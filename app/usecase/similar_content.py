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

def get_similar_content(query: str):
    docs = database.FAISS_DB.similarity_search_with_score(query, k=10, fetch_k=1000)
    logging.info(docs[0])
    with open("./local/data/the-posts.csv", 'r') as f:
        csvr = csv.reader(f)
        csvr = list(csvr)
        for doc in docs:
            logging.info(docs)
            yield SimilarPost(
                id=doc[0].metadata["source"],
                score=str(doc[1]),
                title=csvr[doc[0].metadata["row"]][0],
                text=csvr[doc[0].metadata["row"]][1]
            )