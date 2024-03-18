from unittest.mock import patch

import pytest
from starlette import status
from starlette.testclient import TestClient

from saltapi.service.mail_service import MailService
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


def test_user_cannot_validate_user_without_authentication_token(
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


def test_admins_can_verify_other_users(
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


@patch.object(MailService, 'send_email')
def test_post_send_verification_link_returns_404_for_unknown_users(
        mocker,
        email_service_mock,
        client: TestClient
) -> None:
    mocker.patch.object(email_service_mock, 'send_email')
    response = client.post(f"{USERS_URL}/send-verification-link", json={"username_email": "unknown@email.ac.za"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response = client.post(f"{USERS_URL}/send-verification-link", json={"username_email": "unknown"})
    assert response.status_code == status.HTTP_404_NOT_FOUND


@patch.object(MailService, 'send_email')
def test_post_send_verification_link_send_email(
        mocker,
        email_service_mock,
        client: TestClient
) -> None:
    username = find_username(user_type="Not Active User"),
    user = get_user_by_username(username)
    mocker.patch.object(email_service_mock, 'send_email')
    response = client.post(f"{USERS_URL}/send-verification-link", json={"username_email": user.username})
    assert response.status_code == status.HTTP_200_OK
    assert "activation link has been sent" in response.json()["message"]

    response = client.post(f"{USERS_URL}/send-verification-link", json={"username_email": user.email})
    assert response.status_code == status.HTTP_200_OK
    assert "activation link has been sent" in response.json()["message"]