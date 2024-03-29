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
    return "/proposals/" + proposal_code + "/request-data"


_valid_request_body = {
    "observation_ids": [26766, 26981, 27101],
    "data_formats": ["All"],
}


def test_request_observations_returns_401_for_unauthenticated_user(
    client: TestClient,
) -> None:
    not_authenticated(client)
    proposal_code = "2020-1-SCI-005"
    response = client.post(_url(proposal_code), json=_valid_request_body)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_request_observations_returns_401_for_user_with_invalid_auth_token(
    client: TestClient,
) -> None:
    misauthenticate(client)
    proposal_code = "2020-1-SCI-005"
    response = client.post(_url(proposal_code), json=_valid_request_body)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize(
    "username",
    [
        find_username("Administrator"),
        find_username("SALT Astronomer"),
        find_username("Principal Investigator", "2019-2-SCI-006"),
        find_username("Principal Contact", "2019-2-SCI-006"),
        find_username("Investigator", "2019-2-SCI-006"),
    ],
)
def test_request_observations_should_allow_authorised_users_to_request(
    username: str, client: TestClient
) -> None:
    authenticate(username, client)
    proposal_code = "2019-2-SCI-006"

    response = client.post(_url(proposal_code), json=_valid_request_body)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    "username",
    [
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
    response = client.post(_url("2019-2-SCI-006"), json=_valid_request_body)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_request_observations_returns_400_for_block_visit_belonging_to_another_proposal(
    client: TestClient,
) -> None:
    request_body = {
        "observation_ids": [27101],
        "data_formats": ["All"],
    }

    authenticate(find_username("Administrator"), client)
    proposal_code = "2020-1-SCI-039"
    response = client.post(_url(proposal_code), json=request_body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    message = response.json()["message"]
    assert "27101" in message and proposal_code in message


def test_request_observations_returns_400_for_an_invalid_block_visit_id(
    client: TestClient,
) -> None:
    request_body = {
        "observation_ids": [-1],
        "data_formats": ["All"],
    }

    authenticate(find_username("Administrator"), client)
    proposal_code = "2019-2-SCI-006"
    response = client.post(_url(proposal_code), json=request_body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    message = response.json()["message"]
    assert "-1" in message and proposal_code in message


def test_request_observations_returns_400_for_an_invalid_data_format(
    client: TestClient,
) -> None:
    request_body = {
        "observation_ids": [26766],
        "data_formats": ["not_format"],
    }

    authenticate(find_username("Administrator"), client)
    proposal_code = "2019-2-SCI-006"
    response = client.post(_url(proposal_code), json=request_body)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_request_observations_returns_404_for_an_invalid_proposal_code(
    client: TestClient,
) -> None:
    authenticate(find_username("Administrator"), client)
    proposal_code = "2019-2-NOT_CODE-0011"
    response = client.post(_url(proposal_code), json=_valid_request_body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
