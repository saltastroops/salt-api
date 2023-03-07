import pytest
from fastapi.testclient import TestClient
from starlette import status

from tests.conftest import (
    authenticate,
    find_username,
    misauthenticate,
    not_authenticated,
)

def _url(proposal_code: str) -> str:

    return "/proposals/" + proposal_code + "/liaison-astronomer"


def test_update_liaison_astronomer_returns_401_for_unauthenticated_user(
        client: TestClient,
) -> None:
    not_authenticated(client)
    proposal_code = "2020-1-SCI-005"
    response = client.put(
        _url(proposal_code), json={'id': 494}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_liaison_astronomer_returns_401_for_user_with_invalid_auth_token(
        client: TestClient,
) -> None:
    misauthenticate(client)
    proposal_code = "2020-1-SCI-005"
    response = client.put(
        _url(proposal_code), json={'id': 494}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize(
    "user_role",
    [
        "Administrator",
        "SALT Astronomer"
    ],
)
def test_update_liaison_astronomer_should_allow_admins_and_salt_astronomers_to_update_liaison_astronomer(
        user_role: str, client: TestClient
) -> None:
    admin = find_username("Administrator")
    authenticate(admin, client)
    proposal_code = "2022-2-SCI-039"

    response = client.put(_url(proposal_code), json={'id':494})
    assert response.status_code == status.HTTP_200_OK
    new_liaison_astronomer = response.json()
    assert new_liaison_astronomer["id"] == 494
    proposal_response = client.get("proposals/" + proposal_code)
    proposal = proposal_response.json()
    assert proposal["general_info"]["liaison_salt_astronomer"]['id'] == 494


@pytest.mark.parametrize(
    "user_role",
    [
        "Administrator",
        "SALT Astronomer"
    ],
)
def test_update_liaison_astronomer_should_allow_admins_and_salt_astronomers_to_remove_liaison_astronomer(
        user_role: str, client: TestClient
) -> None:
    username = find_username(user_role)
    authenticate(username, client)
    proposal_code = "2022-2-SCI-039"
    response = client.put(_url(proposal_code), json={'id': None})
    assert response.status_code == status.HTTP_200_OK
    proposal_response = client.get("proposals/" + proposal_code)
    proposal = proposal_response.json()
    assert proposal["general_info"]["liaison_salt_astronomer"] is None


def test_update_liaison_astronomer_should_not_allow_update_for_none_salt_astronomer(
        client: TestClient,
) -> None:
    # Update should not happen for non-SALT Astronomers
    user = find_username("Administrator")
    authenticate(user, client)
    response = client.put(_url("2022-1-SCI-005"), json={'id':230})
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_update_liaison_astronomer_should_not_allow_update_for_non_existing_users(
        client: TestClient,
) -> None:
    # Update should not happen for non-existing users

    user = find_username("Administrator")
    authenticate(user, client)
    response = client.put(_url("2022-1-SCI-005"),  json={'id':-1})
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.parametrize(
    "username",
    [
        find_username("Principal Investigator", "2018-1-SCI-037"),
        find_username("Principal Investigator", "2020-1-MLT-005"),
        find_username("Principal Contact", "2018-2-LSP-001"),
        find_username("Investigator", "2019-2-SCI-006"),
        find_username("TAC Chair", partner_code="RSA"),
        find_username("TAC Member", partner_code="RSA"),
        find_username("SALT Operator"),
        find_username("Board Member")
    ]
)
def test_update_liaison_astronomer_return_403_for_unauthorized_users(
        username, client: TestClient,
) -> None:
    authenticate(username, client)
    proposal_code = '2022-2-SCI-039'
    response = client.put(
        _url(proposal_code), json={'id': 494}
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
