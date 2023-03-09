from starlette import status
from starlette.testclient import TestClient


def test_unauthenticated_users_can_view_list_of_salt_astronomers(
    client: TestClient,
) -> None:
    response = client.get("/users/salt-astronomers")
    assert response.status_code == status.HTTP_200_OK


def test_list_of_astronomers_is_sorted(client: TestClient) -> None:
    response = client.get("/users/salt-astronomers")
    salt_astronomers = response.json()
    for i in range(1, len(salt_astronomers)):
        assert (
            salt_astronomers[i]["family_name"] > salt_astronomers[i - 1]["family_name"]
        )
