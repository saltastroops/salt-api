from typing import Dict, Optional, Any
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from starlette import status

from saltapi.service.mail_service import MailService
from saltapi.web.schema.user import LegalStatus
from tests.conftest import (
    authenticate,
    create_user,
    find_username,
    misauthenticate,
    not_authenticated,
)

USERS_URL = "/users/"


def _url(user_id: int) -> str:
    return USERS_URL + str(user_id)


def _patch_data(
    given_name: Optional[str],
    family_name: Optional[str],
    email: Optional[str],
    password: Optional[str] = None,
) -> Dict[str, Optional[str]]:
    return {
        "given_name": given_name,
        "family_name": family_name,
        "password": password,
        "email": email,
        "legal_status": LegalStatus.OTHER,
        "race": None,
        "gender": None,
        "has_phd": None,
        "year_of_phd_completion": None,
        "active": True,
        "user_verified": True,
    }


def _remove_untested(user_details: Dict[str, Any]):
    del user_details["affiliations"]
    del user_details["alternative_emails"]
    del user_details["id"]
    del user_details["password"]
    del user_details["roles"]
    del user_details["username"]
    del user_details["active"]
    del user_details["user_verified"]
    return user_details


def test_patch_user_should_return_401_for_unauthenticated_user(
    client: TestClient,
) -> None:
    not_authenticated(client)

    response = client.patch(
        _url(1072), json=_patch_data("Chaka", "Mofokeng", "cmofokeng@saao.ac.za")
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_patch_user_should_return_401_for_user_with_invalid_auth_token(
    client: TestClient,
) -> None:
    misauthenticate(client)

    response = client.patch(
        _url(1072), json=_patch_data("Chaka", "Mofokeng", "cmofokeng@saao.ac.za")
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_patch_user_should_return_404_for_non_existing_user(client: TestClient) -> None:
    username = find_username("Administrator")
    authenticate(username, client)

    response = client.patch(
        _url(0), json=_patch_data("Chaka", "Mofokeng", "cmofokeng@example.com")
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
def test_patch_user_should_return_403_if_non_admin_tries_to_update_other_user(
    username: str, client: TestClient
) -> None:
    other_user_id = 6
    authenticate(username, client)

    response = client.patch(
        _url(other_user_id),
        json=_patch_data("Chaka", "Mofokeng", "cmofokeng@saao.ac.za"),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@patch.object(MailService, "send_email")
def test_patch_user_should_keep_existing_values_by_default(
    mocker, email_service_mock, client: TestClient
) -> None:
    user = create_user(client)
    authenticate(find_username("Administrator"), client)

    mocker.patch.object(email_service_mock, "send_email")
    current_user_details = client.get(_url(user["id"])).json()
    client.patch(_url(user["id"]), json={})
    updated_user_details = client.get(_url(user["id"])).json()

    assert updated_user_details == current_user_details


def test_patch_user_should_update_with_new_values(client: TestClient) -> None:
    username = "cmofokeng"
    user_id = 1062
    authenticate(username, client)

    user_update = _patch_data("Chaka", "Mofokeng", "mofokeng.chk@gmail.com")
    expected_updated_user_details = client.get(_url(user_id)).json()
    expected_updated_user_details.update(user_update)
    expected_updated_user_details = _remove_untested(expected_updated_user_details)

    # the endpoint returns the correct response...
    response = client.patch(_url(user_id), json=user_update)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_updated_user_details

    # ... and the user is indeed updated
    updated_user_details = client.get(_url(user_id)).json()

    assert (
        updated_user_details["given_name"]
        == expected_updated_user_details["given_name"]
    )
    assert (
        updated_user_details["family_name"]
        == expected_updated_user_details["family_name"]
    )
    assert updated_user_details["email"] == expected_updated_user_details["email"]


@patch.object(MailService, "send_email")
def test_patch_user_should_be_idempotent(
    mocker, email_service_mock, client: TestClient
) -> None:
    user = create_user(client)
    authenticate(find_username("Administrator"), client)

    user_update = _patch_data(
        given_name=user["given_name"],
        family_name=user["family_name"],
        email=user["email"],
        password="very_very_secret",
    )
    expected_updated_user_details = user.copy()
    expected_updated_user_details.update(user_update)
    expected_updated_user_details = _remove_untested(expected_updated_user_details)

    mocker.patch.object(email_service_mock, "send_email")
    first_update_response = client.patch(_url(user["id"]), json=user_update)
    second_update_response = client.patch(_url(user["id"]), json=user_update)

    assert first_update_response.json() == expected_updated_user_details
    assert second_update_response.json() == expected_updated_user_details


@patch.object(MailService, "send_email")
def test_patch_user_should_return_400_for_using_someone_elses_email(
    mocker,
    email_service_mock,
    client: TestClient,
) -> None:
    user = create_user(client)
    authenticate(find_username("Administrator"), client)
    existing_email = "hettlage@saao.ac.za"

    user_update = _patch_data(user["given_name"], user["family_name"], existing_email)
    expected_updated_user_details = user.copy()
    expected_updated_user_details.update(user_update)
    mocker.patch.object(email_service_mock, "send_email")
    response = client.patch(_url(user["id"]), json=user_update)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_patch_user_should_allow_admin_to_update_other_user(client: TestClient) -> None:
    other_user_id = 1593
    authenticate(find_username("Administrator"), client)
    user_update = _patch_data("Xola", "Ndaliso", "xola.ndaliso@example.com")
    expected_updated_user_details = client.get(_url(other_user_id)).json()
    expected_updated_user_details.update(user_update)
    expected_updated_user_details = _remove_untested(expected_updated_user_details)
    response = client.patch(_url(other_user_id), json=user_update)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_updated_user_details
