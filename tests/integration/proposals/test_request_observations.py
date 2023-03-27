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
    return "/proposals/" + proposal_code + "/request-observations"


_request_body = {
    "observation_ids": [26766, 26981, 27101],
    "data_formats": ["all"],
}


def test_request_observations_returns_401_for_unauthenticated_user(
    client: TestClient,
) -> None:
    not_authenticated(client)
    proposal_code = "2020-1-SCI-005"
    response = client.post(_url(proposal_code), json=_request_body)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_request_observations_returns_401_for_user_with_invalid_auth_token(
    client: TestClient,
) -> None:
    misauthenticate(client)
    proposal_code = "2020-1-SCI-005"
    response = client.post(_url(proposal_code), json=_request_body)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize(
    "username",
    [
        find_username("Administrator"),
        find_username("SALT Astronomer"),
        find_username("Principal Investigator", "2019-2-SCI-006"),
        find_username("Principal Contact", "2019-2-SCI-006"),
    ],
)
def test_request_observations_should_allow_authenticate_users_to_request(
    username: str, client: TestClient
) -> None:
    authenticate(username, client)
    proposal_code = "2019-2-SCI-006"

    response = client.post(_url(proposal_code), json=_request_body)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    "username",
    [
        find_username("Investigator", "2019-2-SCI-006"),
        find_username("Principal Investigator", "2018-2-LSP-001"),
        find_username("Principal Contact", "2018-2-LSP-001"),
        find_username("TAC Chair", partner_code="RSA"),
        find_username("TAC Member", partner_code="RSA"),
        find_username("SALT Operator"),
        find_username("Board Member"),
    ],
)
def test_request_observations_should_not_allow_request_for_unauthorized_users(
    username: str,
    client: TestClient,
) -> None:
    authenticate(username, client)
    response = client.post(_url("2019-2-SCI-006"), json=_request_body)
    assert response.status_code == status.HTTP_403_FORBIDDEN
