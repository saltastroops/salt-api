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
    "proposal_code,allowed",
    [
        ("2020-1-SCI-005", True ),
        ("2020-1-SCI-005", False ),
        ("2016-1-COM-001", True),
        ("2016-1-SVP-001", False),
        ("2019-1-GWE-005", True),
        ("2022-1-ORP-001", False),
        ("2020-2-DDT-005", True),
    ],
)
def test_update_is_self_activatable_should_allow_admins_and_salt_astronomers_to_change_self_activation(
        proposal_code: str, allowed: bool, client: TestClient
) -> None:
    admin = find_username("Administrator")
    authenticate(admin, client)
    response = client.put(_url(proposal_code), json={'allowed': allowed})
    assert response.status_code == status.HTTP_200_OK
    sa = find_username("SALT Astronomer")
    authenticate(sa, client)
    response = client.put(_url(proposal_code), json={'allowed': allowed})
    assert response.status_code == status.HTTP_200_OK


def test_update_is_self_activatable_should_not_allow_for_a_wrong_proposal_code(
        client: TestClient,
) -> None:
    # Administrators and SALT Astronomers can not update with a wrong proposal code
    proposal_code = "2022-1-NOT-CODE-099"
    user = find_username("Administrator")
    authenticate(user, client)

    response = client.put(_url(proposal_code), json={'allowed', True})
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.parametrize(
    "user_role, proposal_code",
    [
        ("Principal Investigator", "2018-1-SCI-037"),
        ("Principal Investigator", "2020-1-MLT-005"),
        ("Principal Contact", "2018-2-LSP-001"),
        ("Investigator", "2019-2-SCI-006")
    ]
)
def test_update_is_self_activatable_returns_403_for_pi_pc_and_investigator(
        user_role:str, proposal_code: Optional[str], client: TestClient,
) -> None:
    user = find_username(user_role, proposal_code)
    authenticate(user, client)
    response = client.put(
        _url(proposal_code), json={'allowed', True}
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.parametrize(
    "user_role, partner_code",
    [
        ("TAC Chair", "RSA"),
        ("TAC Member", "RSA"),
    ]
)
def test_update_is_self_activatable_return_403_for_tacs(
        user_role:str, partner_code: Optional[str], client: TestClient,
) -> None:
    user = find_username(user_role, partner_code=partner_code)
    authenticate(user, client)
    proposal_code = "2020-1-SCI-005"
    response = client.put(
        _url(proposal_code), json={'allowed', True}
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.parametrize(
    "user_role",
    ["SALT Operator", "Board Member"]
)
def test_update_is_self_activatable_return_403_for_operator_and_board_member(
        user_role:str, client: TestClient,
) -> None:
    user = find_username(user_role)
    authenticate(user, client)
    proposal_code = "2020-1-SCI-005"
    response = client.put(
        _url(proposal_code), json={'allowed', True}
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
