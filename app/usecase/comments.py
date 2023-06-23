import logging
from app.adapter.monolite_api import get_post_comments, get_posts
from app.usecase.similar_content import get_similar_content


def get_comments_and_posts(
    user_jwt: str,
    query: str
) -> list[dict]:
    """
    Looks for similar posts to 'query' and returns
    the top-level comments to the X most similar
    posts.
    """
    similar_posts = list(get_similar_content(query))
    comments = get_post_comments(user_jwt, [post.id for post in similar_posts])

    return {
        "posts": similar_posts,
        "comments": comments
    }
