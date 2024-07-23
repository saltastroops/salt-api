import pytest
from starlette import status
from starlette.testclient import TestClient

from tests.conftest import (
    authenticate,
    find_username,
    not_authenticated,
    get_user_by_username,
    valid_user_verification_token,
)

USERS_URL = "/users"
LOGIN_URL = "/login"


def test_password_update_requires_a_valid_authentication_key(
    client: TestClient,
) -> None:
    user_id = 1062

    not_authenticated(client)
    response = client.post(
        f"{USERS_URL}/{user_id}/update-password",
        json={"password": "very-very-secret", "authentication_key": "invalid-token"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_password_update_requires_authentication_key(
    client: TestClient,
) -> None:
    user_id = 1072
    username = find_username("administrator")
    authenticate(username, client)

    response = client.post(
        f"{USERS_URL}/{user_id}/update-password",
        json={
            "password": "very-very-secret",
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_password_update_requires_password(
    client: TestClient,
) -> None:
    user_id = 1072
    username = find_username("administrator")
    user = get_user_by_username(username)
    valid_token = valid_user_verification_token(user.id)

    response = client.post(
        f"{USERS_URL}/{user_id}/update-password",
        json={"authentication_key": valid_token},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_password_update_requires_valid_user_id(
    client: TestClient,
) -> None:
    user_id = 0
    username = find_username("administrator")
    user = get_user_by_username(username)
    valid_token = valid_user_verification_token(user.id)

    response = client.post(
        f"{USERS_URL}/{user_id}/update-password",
        json={"password": "very-very-secret", "authentication_key": valid_token},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "username",
    [
        find_username("Board Member"),
        find_username("TAC Chair", partner_code="RSA"),
        find_username("SALT Astronomer"),
    ],
)
def test_password_update_requires_permissions(
    username: str,
    client: TestClient,
) -> None:
    other_user_id = 1072

    user = get_user_by_username(username)
    valid_token = valid_user_verification_token(user.id)

    response = client.post(
        f"{USERS_URL}/{other_user_id}/update-password",
        json={"password": "very-very-secret", "authentication_key": valid_token},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_password_update(
    client: TestClient,
) -> None:
    user_id = 1062
    username = "cmofokeng"
    password = "my-shiny-very-very-secret"

    user = get_user_by_username(username)
    valid_token = valid_user_verification_token(user.id)

    response = client.post(
        f"{USERS_URL}/{user_id}/update-password",
        json={"password": password, "authentication_key": valid_token},
    )

    assert response.status_code == status.HTTP_200_OK

    client.post("/logout")

    response = client.post("/login", data={"username": username, "password": password})

    assert response.status_code == status.HTTP_204_NO_CONTENT
