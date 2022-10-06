from typing import Any, Callable

import pytest
from fastapi.testclient import TestClient
from starlette import status

from tests.conftest import authenticate, misauthenticate, find_username

USER_URL = "/user"
USER_DATA = "integration/user.yaml"


def test_should_return_401_if_user_is_not_authenticated(client: TestClient) -> None:
    response = client.get(USER_URL)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_should_return_401_if_user_uses_invalid_token(client: TestClient) -> None:
    misauthenticate(client)
    response = client.get(USER_URL)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize("username", [
    find_username("SALT Astronomer"),
    find_username("Board Member"),
    find_username("TAC Member", partner_code="RSA"),
    find_username("TAC Chair", partner_code="RSA"),
    find_username("Investigator", proposal_code="2019-2-SCI-006"),
    find_username("Administrator")
])
def test_should_return_the_correct_user_details(
        username: str,
    client: TestClient,
    check_data: Callable[[Any], None],
) -> None:
    authenticate(username, client)

    response = client.get(USER_URL)
    user_details = response.json()
    user_details["roles"] = set(user_details["roles"])

    check_data(user_details)
