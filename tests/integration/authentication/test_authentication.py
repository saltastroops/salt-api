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


@pytest.mark.parametrize("endpoint", [TOKEN_URL, LOGIN_URL])
def test_should_return_403_if_user_not_active(
        endpoint: str,
        client: TestClient,
) -> None:
    response = client.post(
        endpoint, data={"username": "dod", "password": "secret"}
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "Your account is not active" in response.json()["message"]


@pytest.mark.parametrize("endpoint", [TOKEN_URL, LOGIN_URL])
def test_should_return_403_if_user_not_verified(
        endpoint: str,
        client: TestClient,
) -> None:
    response = client.post(
        endpoint, data={"username": "Renierht", "password": "secret"}
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "Your account has not been validated" in response.json()["message"]


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


def test_login_should_return_secondary_auth_token(client: TestClient) -> None:
    response = client.get("/proposals/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = client.post(
        LOGIN_URL, data={"username": "hettlage", "password": "secret"}
    )
    assert (
        "secondary_auth_token" in response.cookies
        and len(response.cookies["secondary_auth_token"]) > 0
    )


def test_cookie_auth_requires_session_cookie(client: TestClient) -> None:
    response = client.get("/proposals/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client.post(LOGIN_URL, data={"username": "hettlage", "password": "secret"})
    del client.cookies["session"]

    response = client.get("/proposals/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_cookie_auth_requires_secondary_auth_token_cookie(client: TestClient) -> None:
    response = client.get("/proposals/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client.post(LOGIN_URL, data={"username": "hettlage", "password": "secret"})
    del client.cookies["secondary_auth_token"]

    response = client.get("/proposals/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_cookie_auth_requires_consistent_cookies(client: TestClient) -> None:
    response = client.get("/proposals/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client.post(LOGIN_URL, data={"username": "hettlage", "password": "secret"})

    # Update the secondary authentication token cookie.
    # The cookie must be deleted first, as otherwise there will be two cookies with the
    # same key but different domains, and the existing value will still be ysed by the
    # backend.
    del client.cookies["secondary_auth_token"]
    client.cookies["secondary_auth_token"] = "some-other-value"

    response = client.get("/proposals/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_logout_should_log_user_out(client: TestClient) -> None:
    client.post(LOGIN_URL, data={"username": "hettlage", "password": "secret"})

    response = client.get("/proposals/")
    assert response.status_code == status.HTTP_200_OK

    client.post("/logout")

    response = client.get("/proposals/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_logout_should_remove_cookies(client: TestClient) -> None:
    response = client.get("/proposals/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client.post(LOGIN_URL, data={"username": "hettlage", "password": "secret"})
    assert "session" in client.cookies
    assert "secondary_auth_token" in client.cookies

    client.post(LOGOUT_URL)
    assert "session" not in client.cookies
    assert "secondary_auth_token" not in client.cookies


def test_logout_should_work_if_you_are_not_logged_in(client: TestClient) -> None:
    response = client.post(
        LOGOUT_URL, data={"username": "hettlage", "password": "secret"}
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert "session" not in response.cookies
