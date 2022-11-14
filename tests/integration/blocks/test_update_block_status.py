import pytest
from fastapi.testclient import TestClient
from starlette import status

from tests.conftest import authenticate, find_username, not_authenticated

BLOCKS_URL = "/blocks"


def test_block_status_update_requires_authentication(
    client: TestClient,
) -> None:
    block_id = 1
    block_status_value = "On hold"
    block_status_reason = "Not needed"

    not_authenticated(client)
    response = client.put(
        BLOCKS_URL + "/" + str(block_id) + "/status",
        json={"status": block_status_value, "reason": block_status_reason},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_block_status_update_requires_block_status(
    client: TestClient,
) -> None:
    block_id = 2
    username = find_username("administrator")
    authenticate(username, client)

    response = client.put(
        BLOCKS_URL + "/" + str(block_id) + "/status",
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_block_status_update_requires_valid_block_status_value(
    client: TestClient,
) -> None:
    block_id = 100
    username = find_username("administrator")
    authenticate(username, client)

    block_status_value = "Wrong status"
    block_status_reason = ""

    response = client.put(
        BLOCKS_URL + "/" + str(block_id) + "/status",
        json={"block_status": block_status_value, "status_reason": block_status_reason},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "block_status, status_reason",
    [
        ("Completed", ""),
        ("Deleted", "Not needed"),
        ("Expired", ""),
        ("Not set", ""),
        ("Superseded", ""),
    ],
)
def test_block_status_update_requires_valid_and_allowed_block_status_value(
    block_status: str,
    status_reason: str,
    client: TestClient,
) -> None:
    block_id = 2
    username = find_username("administrator")
    authenticate(username, client)

    response = client.put(
        BLOCKS_URL + "/" + str(block_id) + "/status",
        json={"status": block_status, "reason": status_reason},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_block_status_update(
    client: TestClient,
) -> None:
    block_id = 3
    username = find_username("salt_astronomer")
    authenticate(username, client)

    block_status_value = "Active"
    block_status_reason = ""

    client.get(BLOCKS_URL + "/" + str(block_id) + "/status")

    response = client.put(
        BLOCKS_URL + "/" + str(block_id) + "/status",
        json={"status": block_status_value, "reason": block_status_reason},
    )
    assert response.status_code == status.HTTP_200_OK

    block_status = response.json()

    assert block_status["value"] == block_status_value
    assert block_status["reason"] == block_status_reason

    resp = client.get(BLOCKS_URL + "/" + str(block_id) + "/status")
    assert resp.status_code == status.HTTP_200_OK

    new_block_status = resp.json()

    assert new_block_status["value"] == block_status_value
    assert new_block_status["reason"] == block_status_reason
