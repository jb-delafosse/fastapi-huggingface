import requests

_MONOLITE_BASE_URL = "https://go-cell-005.api.lumapps.com/"


class MonoliteException(Exception):
    pass


def get_multi_comments(user_jwt: str, comment_ids: list[str]) -> list[dict]:
    response = requests.get(
        url=f"{_MONOLITE_BASE_URL}_ah/api/lumsites/v1/comment/getMulti",
        params={"uid": comment_ids},
        headers={"Authorization": f"Bearer {user_jwt}"},
        allow_redirects=True,
    )
    if response.status_code >= 400:
        raise MonoliteException

    return response.json()["items"]
