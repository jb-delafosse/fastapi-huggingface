from collections import Counter
from typing import Any
from app.adapter.monolite_api import get_communities

from app.usecase.similar_content import get_similar_content


def get_community_recommendation(user_jwt: str, query:str) -> Any:
    similar_posts = get_similar_content(query, 10, 1)
    recommended_community_ids = Counter([post.community_id for post in similar_posts])
    most_common_communities_ids = [most_common_community_tuple[0] for most_common_community_tuple in recommended_community_ids.most_common(3) ]

    communities = get_communities(user_jwt, most_common_communities_ids)
    return communities
