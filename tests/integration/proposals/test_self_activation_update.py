import pytest
from fastapi.testclient import TestClient
from starlette import status

from tests.conftest import (
    authenticate,
    find_username,
    misauthenticate,
    not_authenticated,
)

TEST_DATA = "integration/users/get_user.yaml"


def _url(proposal_code: str) -> str:
    return "/proposals/" + proposal_code + "/self-activation"


def test_update_is_self_activatable_returns_401_for_unauthenticated_user(
        client: TestClient,
) -> None:
    not_authenticated(client)
    proposal_code = "2020-1-SCI-005"
    response = client.put(
        _url(proposal_code), json={'allowed': False}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_is_self_activatable_returns_401_for_user_with_invalid_auth_token(
        client: TestClient,
) -> None:
    misauthenticate(client)
    proposal_code = "2020-1-SCI-005"
    response = client.put(
        _url(proposal_code), json={'allowed': False}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize(
    "user_role",
    [
        "Administrator",
        "SALT Astronomer"
    ],
)
def test_update_is_self_activatable_should_allow_admins_and_salt_astronomers_to_change_self_activation(
        user_role: str, client: TestClient
) -> None:
    username = find_username(user_role)
    authenticate(username, client)
    proposal_code = "2020-2-SCI-039"

    # Test self activation part 1. Setting to `true`
    # Set self activation allowed to true
    response = client.put(_url(proposal_code), json={'allowed': True})
    # Check status to be 200 OK
    assert response.status_code == status.HTTP_200_OK
    new_self_activation = response.json()
    # Check response value to be `true`
    assert new_self_activation["allowed"] == True
    # Get this proposal
    proposal_response = client.get("proposals/" + proposal_code)
    proposal = proposal_response.json()
    # Check if self activation is `true`
    assert proposal["general_info"]["is_self_activatable"] == True

    # Test self activation part 2. Setting to `false`
    response = client.put(_url(proposal_code), json={'allowed': False})
    assert response.status_code == status.HTTP_200_OK
    new_self_activation = response.json()
    assert new_self_activation["allowed"] == False
    proposal_response = client.get("proposals/" + proposal_code)
    proposal = proposal_response.json()
    assert proposal["general_info"]["is_self_activatable"] == False


def test_update_is_self_activatable_should_not_allow_for_a_wrong_proposal_code(
        client: TestClient,
) -> None:
    # Administrators and SALT Astronomers can not update with a wrong proposal code
    proposal_code = "2022-1-NOT-CODE-099"
    user = find_username("Administrator")
    authenticate(user, client)

    response = client.put(_url(proposal_code), json={'allowed': True})
    assert response.status_code == status.HTTP_404_NOT_FOUND

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
def test_update_is_self_activatable_returns_403_for_unauthorized_users(
        username:str, client: TestClient,
) -> None:
    authenticate(username, client)
    response = client.put(
        _url('2022-2-SCI-039'), json={'allowed': True}
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
