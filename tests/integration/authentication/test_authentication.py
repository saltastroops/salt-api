import pytest
from fastapi.testclient import TestClient
from starlette import status

TOKEN_URL = "/token"

LOGIN_URL = "/login"

LOGOUT_URL = "/logout"


@pytest.mark.parametrize("endpoint", [TOKEN_URL, LOGIN_URL])
def test_should_return_401_if_you_login_with_incorrect_username(
    endpoint: str,
    client: TestClient,
) -> None:
    response = client.post(
        endpoint, data={"username": "idontexist", "password": "secret"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize("endpoint", [TOKEN_URL, LOGIN_URL])
def test_should_return_401_if_you_login_with_invalid_password(
    endpoint: str,
    client: TestClient,
) -> None:
    response = client.post(
        endpoint, data={"username": "hettlage", "password": "wrongpassword"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_should_return_a_token(
    client: TestClient,
) -> None:
    response = client.post(
        TOKEN_URL, data={"username": "hettlage", "password": "secret"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()


def test_token_should_authenticate_user(client: TestClient) -> None:
    response = client.get("/proposals/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = client.post(
        TOKEN_URL, data={"username": "hettlage", "password": "secret"}
    )
    token = response.json()["access_token"]

    client.headers["Authorization"] = f"Bearer {token}"
    response = client.get("/proposals/")
    assert response.status_code == status.HTTP_200_OK


def test_login_should_log_user_in(client: TestClient) -> None:
    response = client.get("/proposals/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = client.post(
        LOGIN_URL, data={"username": "hettlage", "password": "secret"}
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get("/proposals/")
    assert response.status_code == status.HTTP_200_OK


def test_logout_should_log_user_out(client: TestClient) -> None:
    response = client.post(
        LOGIN_URL, data={"username": "hettlage", "password": "secret"}
    )

    response = client.get("/proposals/")
    assert response.status_code == status.HTTP_200_OK

    client.post("/logout")

    response = client.get("/proposals/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_logout_should_work_if_you_are_not_logged_in(client: TestClient) -> None:
    response = client.post(
        LOGOUT_URL, data={"username": "hettlage", "password": "secret"}
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert "session" not in response.cookies
