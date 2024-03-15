import pytest
from starlette import status
from starlette.testclient import TestClient

from tests.conftest import authenticate, find_username, not_authenticated, authenticate_with_validation_token, \
    get_user_by_username

USERS_URL = "/users"
LOGIN_URL = "/login"


def test_user_verification_requires_authentication(
        client: TestClient,
) -> None:
    user_id = 1062

    not_authenticated(client)
    response = client.post(
        f"{USERS_URL}/{user_id}/verify-user", json={}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_user_verification_requires_valid_user_id(
        client: TestClient,
) -> None:
    user_id = 0
    username = find_username("administrator")
    user = get_user_by_username(username)
    authenticate_with_validation_token(user.id, client)

    response = client.post(
        f"{USERS_URL}/{user_id}/verify-user",
        json={},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_user_cannot_validate_user_with_authentication_token(
        client: TestClient,
) -> None:
    user_id = 0
    username = find_username("administrator")
    authenticate(username, client)

    response = client.post(
        f"{USERS_URL}/{user_id}/verify-user",
        json={},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize(
    "username",
    [
        find_username("Board Member"),
        find_username("TAC Chair", partner_code="RSA"),
        find_username("SALT Astronomer"),
    ],
)
def test_verify_user_requires_permissions(
        username: str,
        client: TestClient,
) -> None:
    other_user_id = 1000
    user = get_user_by_username(username)
    authenticate_with_validation_token(user.id, client)

    response = client.post(
        f"{USERS_URL}/{other_user_id}/verify-user",
        json={},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_admins_can_other_users(
        client: TestClient,
) -> None:
    other_user_id = 1000
    username = find_username("administrator")
    user = get_user_by_username(username)
    authenticate_with_validation_token(user.id, client)

    response = client.post(
        f"{USERS_URL}/{other_user_id}/verify-user",
        json={},
    )
    assert response.status_code == status.HTTP_200_OK
