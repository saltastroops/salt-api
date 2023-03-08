import pytest
from fastapi.testclient import TestClient
from starlette import status

from tests.conftest import authenticate, find_username, not_authenticated

PROPOSALS_URL = "/proposals"


def test_investigator_approval_proposal_status_update_requires_authentication(
    client: TestClient,
) -> None:
    proposal_code = "2021-2-LSP-001"
    data = {"status": "Accept", "user_id": 1006}
    not_authenticated(client)
    response = client.put(
        PROPOSALS_URL + "/" + proposal_code + "/investigator-proposal-approval-status",
        json=data,
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_investigator_approval_proposal_status_update_requires_user_id(
    client: TestClient,
) -> None:
    proposal_code = "2021-2-LSP-001"
    username = find_username("administrator")
    data = {"status": "Reject"}

    authenticate(username, client)

    response = client.put(
        PROPOSALS_URL + "/" + proposal_code + "/investigator-proposal-approval-status",
        json=data,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_investigator_approval_proposal_status_update_requires_approval_status(
    client: TestClient,
) -> None:
    proposal_code = "2021-2-LSP-001"
    username = find_username("administrator")
    data = {"user_id": 10}

    authenticate(username, client)

    response = client.put(
        PROPOSALS_URL + "/" + proposal_code + "/investigator-proposal-approval-status",
        json=data,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_investigator_approval_proposal_status_update_requires_valid_approval_status(
    client: TestClient,
) -> None:
    proposal_code = "2019-2-SCI-006"
    username = find_username("Investigator", proposal_code="2019-2-SCI-006")
    data = {"status": "Wrong status", "user_id": 658}

    authenticate(username, client)

    response = client.put(
        PROPOSALS_URL + "/" + proposal_code + "/investigator-proposal-approval-status",
        json=data,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize(
    "username",
    [
        find_username("SALT Astronomer"),
        find_username("TAC Member", partner_code="RSA"),
        find_username("TAC Chair", partner_code="RSA"),
    ],
)
def test_investigator_approval_proposal_status_update_requires_permissions(
    username: str,
    client: TestClient,
) -> None:
    proposal_code = "2019-2-SCI-006"
    data = {"status": "Reject", "user_id": 658}
    authenticate(username, client)

    response = client.put(
        PROPOSALS_URL + "/" + proposal_code + "/investigator-proposal-approval-status",
        json=data,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_investigator_approval_proposal_status_update(
    client: TestClient,
) -> None:
    proposal_code = "2019-2-SCI-006"
    username = find_username("Principal Contact", proposal_code="2019-2-SCI-006")
    authenticate(username, client)

    data = {"status": "Reject", "user_id": 1413}

    response = client.put(
        PROPOSALS_URL + "/" + proposal_code + "/investigator-proposal-approval-status",
        json=data,
    )
    assert response.status_code == status.HTTP_200_OK
