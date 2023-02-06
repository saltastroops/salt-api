import pytest
from fastapi.testclient import TestClient
from starlette import status

from tests.conftest import authenticate, find_username, not_authenticated

PROPOSALS_URL = "/proposals"


def test_proposal_status_update_requires_authentication(
    client: TestClient,
) -> None:
    proposal_code = "2021-2-LSP-001"
    proposal_status_value = "Active"
    proposal_inactive_reason = None

    not_authenticated(client)
    response = client.put(
        PROPOSALS_URL + "/" + proposal_code + "/status",
        json={"status": proposal_status_value, "reason": proposal_inactive_reason},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_proposal_status_update_requires_proposal_status(
    client: TestClient,
) -> None:
    proposal_code = "2021-2-LSP-001"
    username = find_username("administrator")
    authenticate(username, client)

    response = client.put(
        PROPOSALS_URL + "/" + proposal_code + "/status",
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_proposal_status_update_requires_valid_proposal_status_value(
    client: TestClient,
) -> None:
    proposal_code = "2023-1-MLT-006"
    username = find_username("administrator")
    authenticate(username, client)

    proposal_status_value = "Wrong status"
    proposal_inactive_reason = None

    response = client.put(
        PROPOSALS_URL + "/" + proposal_code + "/status",
        json={"status": proposal_status_value, "reason": proposal_inactive_reason},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_proposal_status_update_requires_valid_proposal_inactive_reason(
    client: TestClient,
) -> None:
    proposal_code = "2023-1-MLT-006"
    username = find_username("administrator")
    authenticate(username, client)

    proposal_status_value = "Under scientific review"
    proposal_inactive_reason = "Wrong inactive reason"

    response = client.put(
        PROPOSALS_URL + "/" + proposal_code + "/status",
        json={"status": proposal_status_value, "reason": proposal_inactive_reason},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_proposal_status_update(
    client: TestClient,
) -> None:
    proposal_code = "2023-1-MLT-006"
    username = find_username("administrator")
    authenticate(username, client)

    proposal_status_value = "Active"
    proposal_inactive_reason = None

    response = client.put(
        PROPOSALS_URL + "/" + proposal_code + "/status",
        json={"status": proposal_status_value, "reason": proposal_inactive_reason},
    )
    assert response.status_code == status.HTTP_200_OK

    proposal_status = response.json()

    assert proposal_status["value"] == proposal_status_value
    assert proposal_status["reason"] == proposal_inactive_reason

    resp = client.get(PROPOSALS_URL + "/" + proposal_code + "/status")
    assert resp.status_code == status.HTTP_200_OK

    new_block_status = resp.json()

    assert new_block_status["value"] == proposal_status_value
    assert new_block_status["reason"] == proposal_inactive_reason


def test_proposal_status_update_with_inactive_reason(
        client: TestClient,
) -> None:
    proposal_code = "2022-2-SCI-007"
    username = find_username("administrator")
    authenticate(username, client)

    proposal_status_value = "Inactive"
    proposal_inactive_reason = "Undoable"

    response = client.put(
        PROPOSALS_URL + "/" + proposal_code + "/status",
        json={"status": proposal_status_value, "reason": proposal_inactive_reason},
        )
    assert response.status_code == status.HTTP_200_OK

    proposal_status = response.json()

    assert proposal_status["value"] == proposal_status_value
    assert proposal_status["reason"] == proposal_inactive_reason

    resp = client.get(PROPOSALS_URL + "/" + proposal_code + "/status")
    assert resp.status_code == status.HTTP_200_OK

    new_block_status = resp.json()

    assert new_block_status["value"] == proposal_status_value
    assert new_block_status["reason"] == proposal_inactive_reason
