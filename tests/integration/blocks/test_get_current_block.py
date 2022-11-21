from typing import Any, Callable

import pytest
import requests
from fastapi.testclient import TestClient
from starlette import status

from tests.conftest import authenticate, find_username, not_authenticated

BLOCKS_URL = "/blocks"


def test_get_currently_observed_block_requires_authentication(
    client: TestClient,
) -> None:
    not_authenticated(client)
    response = client.get(BLOCKS_URL + "/current-block")
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
def test_get_currently_observed_block_requires_permissions(
    username: str, client: TestClient
) -> None:
    authenticate(username, client)
    response = client.get(BLOCKS_URL + "/current-block")
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize(
    "username",
    [
        find_username("SALT Astronomer"),
        find_username("SALT Operator"),
        find_username("Administrator"),
    ],
)
def test_get_currently_observed_block(
    username: str,
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    check_data: Callable[[Any], None],
) -> None:
    authenticate(username, client)

    def mock_tcs_call(url: str):
        class MockResponse:
            text = """
<Cluster>
<Name>salt-tcs-icd.xml</Name>
<NumElts>1</NumElts>
<Cluster>
<Name>tcs obs target info</Name>
<NumElts>1</NumElts>
<String>
<Name>block id</Name>
<Val>1</Val>
</String>
</Cluster>
</Cluster>
"""

            def __init__(self):
                self.status_code = 200

        return MockResponse

    monkeypatch.setattr(
        requests,
        "get",
        mock_tcs_call,
    )

    response = client.get(BLOCKS_URL + "/current-block")

    assert response.status_code == status.HTTP_200_OK
    check_data(response.json())


@pytest.mark.parametrize(
    "username",
    [
        find_username("SALT Astronomer"),
        find_username("SALT Operator"),
        find_username("Administrator"),
    ],
)
def test_get_returns_no_currently_observed_block(
    username: str,
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    authenticate(username, client)

    def mock_tcs_call(url: str):
        class MockResponse:
            text = """
<Cluster>
<Name>salt-tcs-icd.xml</Name>
<NumElts>1</NumElts>
<Cluster>
<Name>tcs obs target info</Name>
<NumElts>0</NumElts>
</Cluster>
</Cluster>
"""

            def __init__(self):
                self.status_code = 200

        return MockResponse

    monkeypatch.setattr(
        requests,
        "get",
        mock_tcs_call,
    )

    response = client.get(BLOCKS_URL + "/current-block")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() is None
