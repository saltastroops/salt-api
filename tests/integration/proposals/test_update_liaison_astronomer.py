from typing import Optional

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
    "proposal_code",
    [
        "2020-1-SCI-005",
        "2016-1-COM-001",
        "2016-1-SVP-001",
        "2019-1-GWE-005",
        "2022-1-ORP-001",
        "2020-2-DDT-005",
    ],
)
def test_update_liaison_astronomer_should_allow_admins_and_salt_astronomers_to_update_liaison_astronomer(
        proposal_code: str, client: TestClient
) -> None:
    admin = find_username("Administrator")
    authenticate(admin, client)
    response = client.put(_url(proposal_code), json={'id':494})
    assert response.status_code == status.HTTP_200_OK
    sa = find_username("SALT Astronomer")
    authenticate(sa, client)
    response = client.put(_url(proposal_code), json={'id':494})
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.parametrize(
    "proposal_code",
    [
        "2020-1-SCI-005",
        "2016-1-COM-001",
        "2016-1-SVP-001",
        "2019-1-GWE-005",
        "2022-1-ORP-001",
        "2020-2-DDT-005",
    ],
)
def test_update_liaison_astronomer_should_allow_admins_and_salt_astronomers_to_remove_liaison_astronomer(
        proposal_code: str, client: TestClient
) -> None:
    admin = find_username("Administrator")
    authenticate(admin, client)
    response = client.put(_url(proposal_code), json={'id': None})
    assert response.status_code == status.HTTP_200_OK
    sa = find_username("SALT Astronomer")
    authenticate(sa, client)
    response = client.put(_url(proposal_code), json={'id': None})
    assert response.status_code == status.HTTP_200_OK

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
    "user_role, proposal_code",
    [
        ("Principal Investigator", "2018-1-SCI-037"),
        ("Principal Investigator", "2020-1-MLT-005"),
        ("Principal Contact", "2018-2-LSP-001"),
        ("Investigator", "2019-2-SCI-006")
    ]
)
def test_update_liaison_astronomer_return_403_for_pi_pc_and_investigator(
        user_role:str, proposal_code: Optional[str], client: TestClient,
) -> None:
    #  Principal Investigator, Principal Contact and Investigator are not allowed to update liaison astronomer.
    user = find_username(user_role, proposal_code)
    authenticate(user, client)
    response = client.put(
        _url(proposal_code), json={'id': 494}
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.parametrize(
    "user_role, partner_code",
    [
        ("TAC Chair", "RSA"),
        ("TAC Member", "RSA"),
    ]
)
def test_update_liaison_astronomer_return_403_for_tacs(
        user_role:str, partner_code: Optional[str], client: TestClient,
) -> None:
    #  TAC's are not allowed to update liaison astronomer.
    user = find_username(user_role, partner_code=partner_code)
    authenticate(user, client)
    proposal_code = "2020-1-SCI-005"
    response = client.put(
        _url(proposal_code), json={'id': 494}
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.parametrize(
    "user_role",
    ["SALT Operator", "Board Member"]
)
def test_update_liaison_astronomer_return_403_for_operator_and_board_member(
        user_role:str, client: TestClient,
) -> None:
    #  SALT Operator and Board Member are not allowed to update liaison astronomer.
    user = find_username(user_role)
    authenticate(user, client)
    proposal_code = "2020-1-SCI-005"
    response = client.put(
        _url(proposal_code), json={'id': 494}
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
