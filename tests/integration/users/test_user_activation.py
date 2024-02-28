import pytest
from starlette import status
from starlette.testclient import TestClient

from tests.conftest import authenticate, find_username, not_authenticated

USERS_URL = "/users"
LOGIN_URL = "/login"


def test_user_activation_requires_authentication(
        client: TestClient,
) -> None:
    user_id = 1062

    not_authenticated(client)
    response = client.post(
        f"{USERS_URL}/{user_id}/activate-user", json={}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_password_update_requires_valid_user_id(
        client: TestClient,
) -> None:
    user_id = 0
    username = find_username("administrator")
    authenticate(username, client)

    response = client.post(
        f"{USERS_URL}/{user_id}/activate-user",
        json={},
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
def test_activate_user_requires_permissions(
        username: str,
        client: TestClient,
) -> None:
    other_user_id = 1072

    authenticate(username, client)

    response = client.post(
        f"{USERS_URL}/{other_user_id}/activate-user",
        json={},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_admins_can_activate_other_users(
        client: TestClient,
) -> None:
    other_user_id = 1000
    username = find_username("administrator")
    authenticate(username, client)

    response = client.post(
        f"{USERS_URL}/{other_user_id}/activate-user",
        json={},
    )
    assert response.status_code == status.HTTP_200_OK
