from fastapi.testclient import TestClient
from starlette import status

from tests.conftest import authenticate, find_username, not_authenticated


def _url(semester: str) -> str:
    return f"/proposals/requesting_more_time/{semester}"


def test_proposals_requesting_more_time_should_return_401_for_unauthenticated_user(
    client: TestClient,
) -> None:
    not_authenticated(client)
    response = client.get(_url("2026-1"))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_proposals_requesting_more_time_should_return_403_for_non_admin_user(
    client: TestClient,
) -> None:
    investigator = find_username("Investigator", "2020-2-SCI-043")
    authenticate(investigator, client)
    response = client.get(_url("2026-1"))
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_proposals_requesting_more_time_should_return_200_for_admin_user(
    client: TestClient,
) -> None:
    admin = find_username("Administrator")
    authenticate(admin, client)
    response = client.get(_url("2020-1"))
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)