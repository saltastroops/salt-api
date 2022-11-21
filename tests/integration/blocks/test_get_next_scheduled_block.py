from typing import Any, Callable, Optional

import pytest
from fastapi.testclient import TestClient
from starlette import status

import saltapi.repository.block_repository
from saltapi.service.block import Block
from tests.conftest import authenticate, find_username, not_authenticated

BLOCKS_URL = "/blocks"


BLOCK_ID = 1


def test_get_next_scheduled_block_requires_authentication(
    client: TestClient,
) -> None:
    not_authenticated(client)
    response = client.get(BLOCKS_URL + "/next-scheduled-block")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize(
    "username",
    [
        find_username("Investigator", proposal_code="2016-1-COM-001"),
        find_username("Principal Contact", proposal_code="2016-1-COM-001"),
        find_username("Principal Investigator", proposal_code="2016-1-COM-001"),
        find_username("TAC Member", partner_code="POL"),
        find_username("TAC Chair", partner_code="POL"),
        find_username("Board Member"),
    ],
)
def test_get_next_scheduled_block_requires_permissions(
    username: str, client: TestClient
) -> None:
    authenticate(username, client)
    response = client.get(BLOCKS_URL + "/next-scheduled-block")
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize(
    "username",
    [
        find_username("SALT Astronomer"),
        find_username("SALT Operator"),
        find_username("Administrator"),
    ],
)
def test_get_next_scheduled_block(
    username: str,
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    check_data: Callable[[Any], None],
) -> None:
    authenticate(username, client)

    def mock_get_scheduled_block_id(*args: Any, **kwargs: Any) -> Optional[Block]:
        block_id = 1
        return block_id

    monkeypatch.setattr(
        saltapi.repository.block_repository.BlockRepository,
        "get_scheduled_block_id",
        mock_get_scheduled_block_id,
    )

    response = client.get(BLOCKS_URL + "/next-scheduled-block")

    assert response.status_code == status.HTTP_200_OK
    check_data(response.json())
