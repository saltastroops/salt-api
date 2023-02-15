import pytest
from fastapi.testclient import TestClient
from starlette import status

from tests.conftest import authenticate, find_username, not_authenticated

BLOCK_VISIT_URL = "/block-visits"


def test_patch_block_visit_status_requires_authentication(
    client: TestClient,
) -> None:
    block_visit_id = 1
    not_authenticated(client)
    block_visit_status = {"status": "Accepted", "reason": None}
    response = client.patch(
        BLOCK_VISIT_URL + "/" + str(block_visit_id) + "/status", json=block_visit_status
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_patch_block_visit_status_requires_existing_block_visit(
    client: TestClient,
) -> None:
    block_visit_id = -1
    user = find_username("Administrator")
    authenticate(user, client)
    block_visit_status = {"status": "Accepted", "reason": None}
    response = client.patch(
        BLOCK_VISIT_URL + "/" + str(block_visit_id) + "/status", json=block_visit_status
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_patch_block_visit_status_requires_valid_block_visit_status(
    client: TestClient,
) -> None:
    block_visit_id = 25392  # belongs to proposal 2019-2-SCI-006
    user = find_username("Administrator")
    authenticate(user, client)
    block_visit_status = {"status": "Status", "reason": None}
    response = client.patch(
        BLOCK_VISIT_URL + "/" + str(block_visit_id) + "/status", json=block_visit_status
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_patch_block_visit_status_requires_valid_block_rejection_reason(
    client: TestClient,
) -> None:
    block_visit_id = 25392  # belongs to proposal 2019-2-SCI-006
    user = find_username("Administrator")
    authenticate(user, client)
    block_visit_status = {"status": "Rejected", "reason": "Wrong reason"}
    response = client.patch(
        BLOCK_VISIT_URL + "/" + str(block_visit_id) + "/status", json=block_visit_status
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_patch_block_visit_status_requires_block_visit_status(
    client: TestClient,
) -> None:
    block_visit_id = 25392  # belongs to proposal 2019-2-SCI-006
    user = find_username("Administrator")
    authenticate(user, client)
    block_visit_status = {"status": None, "reason": "Other"}
    response = client.patch(
        BLOCK_VISIT_URL + "/" + str(block_visit_id) + "/status", json=block_visit_status
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_patch_block_visit_status_requires_block_rejection_reason(
    client: TestClient,
) -> None:
    block_visit_id = 25392  # belongs to proposal 2019-2-SCI-006
    user = find_username("Administrator")
    authenticate(user, client)
    block_visit_status = {"status": "Rejected", "reason": None}
    response = client.patch(
        BLOCK_VISIT_URL + "/" + str(block_visit_id) + "/status", json=block_visit_status
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_patch_block_visit_status_requires_no_rejection_reason_for_block_visit_status_not_rejected(
    client: TestClient,
) -> None:
    block_visit_id = 25392  # belongs to proposal 2019-2-SCI-006
    user = find_username("Administrator")
    authenticate(user, client)
    block_visit_status = {"status": "Accepted", "reason": "Phase 2 problems"}
    response = client.patch(
        BLOCK_VISIT_URL + "/" + str(block_visit_id) + "/status", json=block_visit_status
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.parametrize(
    "username",
    [
        find_username("Investigator", proposal_code="2019-2-SCI-006"),
        find_username("Principal Contact", proposal_code="2019-2-SCI-006"),
        find_username("Principal Investigator", proposal_code="2019-2-SCI-006"),
        find_username("TAC Member", partner_code="RSA"),
        find_username("TAC Chair", partner_code="RSA"),
    ],
)
def test_patch_block_visit_status_requires_permissions(
    username: str, client: TestClient
) -> None:
    block_visit_id = 24700  # belongs to proposal 2016-2-COM-001

    authenticate(username, client)
    block_visit_status = {
        "status": "Rejected",
        "reason": "Observing conditions not met",
    }
    response = client.patch(
        BLOCK_VISIT_URL + "/" + str(block_visit_id) + "/status", json=block_visit_status
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_patch_block_visit_status(
    client: TestClient,
) -> None:
    block_visit_id = 27248  # belongs to proposal 2016-2-COM-001

    username = find_username("salt_astronomer")
    authenticate(username, client)

    block_visit_status = "Rejected"
    rejection_reason = "Observing conditions not met"

    resp = client.patch(
        BLOCK_VISIT_URL + "/" + str(block_visit_id) + "/status",
        json={"status": block_visit_status, "reason": rejection_reason},
    )
    assert resp.status_code == status.HTTP_200_OK

    response = client.get(BLOCK_VISIT_URL + "/" + str(block_visit_id))

    new_block_visit = response.json()

    assert new_block_visit["status"] == block_visit_status
    assert new_block_visit["rejection_reason"] == rejection_reason
