from fastapi.testclient import TestClient
from starlette import status

PIPT_NEWS_URL = "/pipt-news/"


def _url(days: int) -> str:
    return f"{PIPT_NEWS_URL}{days}"


def test_get_pipt_news_returns_200_with_news(client: TestClient) -> None:
    response = client.get(_url(370))
    assert response.status_code == status.HTTP_200_OK
    news = response.json()
    assert isinstance(news, list)


def test_get_pipt_news_should_return_404_if_no_news_found(client: TestClient) -> None:
    response = client.get(_url(9999))
    assert response.status_code == status.HTTP_404_NOT_FOUND
