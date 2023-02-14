import pytest
from starlette import status
from starlette.testclient import TestClient

from tests.conftest import authenticate, find_username, not_authenticated

SWITCH_USER_URL = "/switch-user"


@pytest.mark.parametrize("switched_username", ["techops", "non-existing-user"])
def test_switch_user_fails_for_non_authenticated_user(
    switched_username: str, client: TestClient
) -> None:
    # A non-authenticated user should get a 401 error when trying to switch the user.
    # As otherwise the endpoint might be used for guessing usernames, this is true even
    # if the username does not exist.
    not_authenticated(client)
    response = client.post(
        SWITCH_USER_URL,
        json={"username": switched_username},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize(
    "username,switched_username",
    [
        (find_username("Board Member"), "techops"),
        (find_username("TAC Chair", partner_code="UW"), "non-existing-user"),
        (find_username("TAC Member", partner_code="UW"), "non-existing-user"),
        (find_username("SALT Astronomer"), "techops"),
        (
            find_username("Investigator", proposal_code="2018-2-LSP-001"),
            "non-existing-user",
        ),
        (find_username("Principal Contact", proposal_code="2018-2-LSP-001"), "techops"),
        (
            find_username("Principal Investigator", proposal_code="2018-2-LSP-001"),
            "non-existing-user",
        ),
    ],
)
def test_switch_user_fails_for_non_administrators(
    username: str, switched_username: str, client: TestClient
) -> None:
    authenticate(username, client)
    response = client.post(
        SWITCH_USER_URL,
        json={
            "username": find_username("Investigator", proposal_code="2020-2-SCI-018")
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_switch_user_is_successful(client: TestClient) -> None:
    switched_username = "techops"

    # Login as an administrator
    authenticate(find_username("Administrator"), client)
    response = client.get("/user")
    assert response.json()["username"] != switched_username

    # Switch the user
    response = client.post(SWITCH_USER_URL, json={"username": switched_username})
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # The client by default uses a token authentication. Now that we have a cookie for
    # the new user, we have to remove that token.
    del client.headers["Authorization"]

    # Check that you are logged in as the other user now
    response = client.get("/user")
    assert response.json()["username"] == switched_username


def test_switch_user_fails_for_unknown_username(client: TestClient) -> None:
    # Login as an administrator
    authenticate(find_username("Administrator"), client)
    response = client.get("/user")
    admin_username = response.json()["username"]

    # Try to switch the user and check it fails
    response = client.post(SWITCH_USER_URL, json={"username": "non-existing-user"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "username" in response.json()["message"]

    # Check that you are still logged in as the original user
    response = client.get("/user")
    assert response.json()["username"] == admin_username
