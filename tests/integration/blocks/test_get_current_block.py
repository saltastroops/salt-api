from typing import Any, Callable

import pytest
import responses
from fastapi.testclient import TestClient
from starlette import status

from saltapi.settings import get_settings
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


def test_get_currently_observed_block(
    client: TestClient,
    check_data: Callable[[Any], None],
) -> None:
    username = find_username("Administrator")
    authenticate(username, client)

    with responses.RequestsMock() as rsp:
        text = """
<String>
<Name>block id</Name>
<Val>1</Val>
</String>
"""
        rsp.add(
            responses.GET,
            get_settings().tcs_icd_url,
            body=text,
            status=200,
            content_type="application/json",
        )
        response = client.get(BLOCKS_URL + "/current-block")

        assert response.status_code == status.HTTP_200_OK
        check_data(response.json())


def test_get_returns_no_currently_observed_block(
    client: TestClient,
) -> None:
    username = find_username("SALT Astronomer")
    authenticate(username, client)

    with responses.RequestsMock() as rsp:
        text = """
<Name>tcs obs target info</Name>
"""
        rsp.add(
            responses.GET,
            get_settings().tcs_icd_url,
            body=text,
            status=404,
            content_type="application/json",
        )
        response = client.get(BLOCKS_URL + "/current-block")

        assert response.status_code == status.HTTP_404_NOT_FOUND
