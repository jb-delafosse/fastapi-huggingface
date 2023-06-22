from app.adapter.monolite_api import get_post_comments
from app.usecase.similar_content import get_similar_content


def get_comments(
    user_jwt: str,
    query: str
) -> list[dict]:
    """
    Looks for similar posts to 'query' and returns
    the top-level comments to the X most similar
    posts.
    """
    similar_posts = get_similar_content(query)
    return get_post_comments(user_jwt, similar_posts)
