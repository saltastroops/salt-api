import uuid
from typing import Any, Dict, Optional
from unittest.mock import patch

from fastapi.testclient import TestClient
from starlette import status

from saltapi.service.mail_service import MailService
from saltapi.web.schema.user import LegalStatus
from tests.conftest import (
    authenticate,
    find_username,
    misauthenticate,
    not_authenticated,
)

USERS_URL = "/users/"

TOKEN_URL = "/token"


def _random_string() -> str:
    return str(uuid.uuid4())[:8]


def _new_user_details(username: Optional[str] = None) -> Dict[str, Any]:
    _username = username if username else _random_string()
    return dict(
        username=_username,
        password=_random_string(),
        alternative_emails=[],
        email=f"{_username}@example.com",
        given_name=_random_string(),
        family_name=_random_string(),
        institution_id=5,
        affiliations=[
            {
                "institution_id": 5,
                "partner_code": "RSA",
                "partner_name": "South Africa",
                "name": "South African Astronomical Observatory",
                "department": " ",
            }
        ],
        legal_status=LegalStatus.OTHER,
        race=None,
        gender=None,
        has_phd=None,
        year_of_phd_completion=None,
    )


@patch.object(MailService, "send_email")
def test_post_user_should_be_allowed_for_unauthenticated_user(
    mocker,
    email_service_mock,
    client: TestClient,
) -> None:
    not_authenticated(client)

    response = client.post(USERS_URL, json=_new_user_details())
    assert response.status_code == status.HTTP_201_CREATED


@patch.object(MailService, "send_email")
def test_post_user_should_be_allowed_for_misauthenticated_user(
    mocker,
    email_service_mock,
    client: TestClient,
) -> None:
    misauthenticate(client)
    mocker.patch.object(email_service_mock, "send_email")
    response = client.post(USERS_URL, json=_new_user_details())
    assert response.status_code == status.HTTP_201_CREATED


@patch.object(MailService, "send_email")
def test_post_user_should_be_allowed_for_authenticated_user(
    mocker, email_service_mock, client: TestClient
) -> None:
    username = find_username("Investigator", proposal_code="2019-2-SCI-006")
    authenticate(username, client)
    mocker.patch.object(email_service_mock, "send_email")
    response = client.post(USERS_URL, json=_new_user_details())
    assert response.status_code == status.HTTP_201_CREATED


def test_post_user_should_return_400_if_username_exists_already(
    client: TestClient,
) -> None:
    authenticate(find_username("Administrator"), client)
    existing_username = find_username("Investigator", proposal_code="2019-2-SCI-006")

    response = client.post(
        USERS_URL, json=_new_user_details(username=existing_username)
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "username" in response.json()["message"].lower()


@patch.object(MailService, "send_email")
def test_post_user_should_create_a_new_user(
    mocker, email_service_mock, client: TestClient
) -> None:
    new_user_details = _new_user_details()
    expected_user = new_user_details.copy()
    del expected_user["password"]
    del expected_user["institution_id"]
    del expected_user["legal_status"]
    del expected_user["gender"]
    del expected_user["race"]
    del expected_user["has_phd"]
    del expected_user["year_of_phd_completion"]
    expected_user["roles"] = []

    mocker.patch.object(email_service_mock, "send_email")

    response = client.post(USERS_URL, json=new_user_details)
    assert response.status_code == status.HTTP_201_CREATED

    # check properties other than the user id
    created_user = response.json()
    del created_user["id"]
    assert created_user == expected_user

    # It would be nice to check the password as well, but as the authentication method
    # is replaced with a dummy one for testing, we cannot easily be achieved. The
    # password should thus rather be tested implicitly as part of an end-to-end test for
    # creating a new user.
