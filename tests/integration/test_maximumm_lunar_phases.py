import pytest
from fastapi.testclient import TestClient
from starlette import status

from tests.conftest import authenticate, find_username, not_authenticated

MAX_LUNAR_PHASE_URL = "/maximum-lunar-phases"


def test_maximum_lunar_phases_requires_authentication(client: TestClient) -> None:
    not_authenticated(client)
    response = client.get(MAX_LUNAR_PHASE_URL + "/2025-1-SCI-001")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_maximum_lunar_phases_empty_list(client: TestClient) -> None:
    username = find_username("Administrator")
    authenticate(username, client)

    proposal_code = "2025-1-SCI-001"
    response = client.get(f"{MAX_LUNAR_PHASE_URL}/{proposal_code}")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["proposal_code"] == proposal_code
    assert "phases" in data
    assert isinstance(data["phases"], list)
    assert len(data["phases"]) == 0
