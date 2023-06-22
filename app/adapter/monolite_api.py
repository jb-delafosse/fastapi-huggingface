import requests

_MONOLITE_BASE_URL = "https://go-cell-005.api.lumapps.com/"
_ORGANIZATION_ID = "4753443638214656"


class MonoliteException(Exception):
    pass


def get_post_comments(user_jwt: str, post_ids: list[str]) -> list[dict]:
    comments = []
    for post_id in post_ids:
        response = requests.get(
            url=f"{_MONOLITE_BASE_URL}_ah/api/lumsites/v1/comment/list",
            params={"content": post_id},
            headers={"Authorization": f"Bearer {user_jwt}"},
            allow_redirects=True,
        )
        if (code := response.status_code) >= 400:
            raise MonoliteException(f"code: {code}, text: {response.text}")
        comments.extend(response.json()["items"])

    return comments


def get_posts(user_jwt: str, post_ids: list[str]) -> list[dict]:
    response = requests.post(
        url=f"{_MONOLITE_BASE_URL}_ah/api/lumsites/v1/content/list",
        json={"ids": post_ids},
        headers={"Authorization": f"Bearer {user_jwt}", "Lumapps-Organization-Id": _ORGANIZATION_ID},
        allow_redirects=True,
    )
    if (code := response.status_code) >= 400:
        raise MonoliteException(f"code: {code}, text: {response.text}")

    return response.json()["items"]


def get_communities(user_jwt: str, community_ids: list[str]) -> list[dict]:
    response = requests.post(
        url=f"{_MONOLITE_BASE_URL}_ah/api/lumsites/v1/community/list",
        json={"ids": community_ids},
        headers={"Authorization": f"Bearer {user_jwt}", "Lumapps-Organization-Id": _ORGANIZATION_ID},
        allow_redirects=True,
    )
    if (code := response.status_code) >= 400:
        raise MonoliteException(f"code: {code}, text: {response.text}")

    return response.json()["items"]