import pytest
from starlette import status
from starlette.testclient import TestClient

from tests.conftest import authenticate, find_username, not_authenticated

BASE_URL = "/users/42/"

PROPOSAL_CODE = "2018-2-LSP-001"


def test_unauthenticated_users_cannot_view_proposal_permissions(client: TestClient):
    not_authenticated(client)
    response = client.get(BASE_URL + "proposal-permissions")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize(
    "username",
    [
        # PI of other proposal
        find_username("Principal Investigator", proposal_code="2020-2-DDT-005"),
        # Investigator on the proposal;
        find_username("Investigator", PROPOSAL_CODE),
        # TAC Chair
        find_username("TAC Chair", partner_code="RSA"),
        # TAC member
        find_username("TAC member", partner_code="RSA"),
        # Board member
        find_username("Board member"),
        # SALT Astronomer
        find_username("SALT Astronomer"),
        # SALT Operator
        find_username("SALT Operator"),
    ],
)
def test_unauthorized_users_cannot_view_proposal_permissions(
    username: str, client: TestClient
):
    authenticate(username, client)
    response = client.get(BASE_URL + "proposal-permissions")
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_proposal_permissions_for_unknown_user_are_not_found(
    client: TestClient,
) -> None:
    authenticate(find_username("Administrator"), client)
    response = client.get("/users/-1/proposal-permissions")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "username",
    [
        # Administrator
        find_username("Administrator"),
    ],
)
def test_proposal_permission_can_be_viewed(username: str, client: TestClient):
    authenticate(username, client)
    response = client.get(BASE_URL + "proposal-permissions")

    # Ideally, we should test that the returned permissions are correct. However, these
    # may change in the database, so the test might easily become flakey. We will test
    # this implicitly, though, whe testing granting and revoking permissions.
    assert response.status_code == status.HTTP_200_OK


def test_unauthenticated_users_cannot_grant_proposal_permissions(client: TestClient):
    not_authenticated(client)
    permission = {"proposal_code": PROPOSAL_CODE, "permission_type": "View"}
    response = client.post(BASE_URL + "grant-proposal-permission", json=permission)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize(
    "username",
    [
        # PI of other proposal
        find_username("Principal Investigator", proposal_code="2020-2-DDT-005"),
        # Investigator on the proposal;
        find_username("Investigator", PROPOSAL_CODE),
        # TAC Chair
        find_username("TAC Chair", partner_code="RSA"),
        # TAC member
        find_username("TAC member", partner_code="RSA"),
        # Board member
        find_username("Board member"),
        # SALT Operator
        find_username("SALT Operator"),
    ],
)
def test_unauthorized_users_cannot_grant_proposal_permissions(
    username: str, client: TestClient
):
    authenticate(username, client)
    permission = {"proposal_code": PROPOSAL_CODE, "permission_type": "View"}
    response = client.post(BASE_URL + "grant-proposal-permission", json=permission)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_granting_permission_for_unknown_user_gives_not_found_error(
    client: TestClient,
) -> None:
    authenticate(find_username("Administrator"), client)
    permission = {"proposal_code": PROPOSAL_CODE, "permission_type": "View"}
    response = client.post("/users/-1/grant-proposal-permission", json=permission)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_granting_permission_for_unknown_proposal_code_gives_user_error(
    client: TestClient,
) -> None:
    authenticate(find_username("Administrator"), client)
    permission = {"proposal_code": "2022-2-SCI-099", "permission_type": "View"}
    response = client.post(BASE_URL + "grant-proposal-permission", json=permission)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_granting_permission_for_unknown_permission_type_gives_unprocessable_error(
    client: TestClient,
) -> None:
    authenticate(find_username("Administrator"), client)
    permission = {"proposal_code": "2022-2-SCI-099", "permission_type": "IDontExist"}
    response = client.post(BASE_URL + "grant-proposal-permission", json=permission)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_unauthenticated_users_cannot_revoke_proposal_permissions(client: TestClient):
    not_authenticated(client)
    permission = {"proposal_code": PROPOSAL_CODE, "permission_type": "View"}
    response = client.post(BASE_URL + "revoke-proposal-permission", json=permission)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize(
    "username",
    [
        # PI of other proposal
        find_username("Principal Investigator", proposal_code="2020-2-DDT-005"),
        # Investigator on the proposal;
        find_username("Investigator", PROPOSAL_CODE),
        # TAC Chair
        find_username("TAC Chair", partner_code="RSA"),
        # TAC member
        find_username("TAC member", partner_code="RSA"),
        # Board member
        find_username("Board member"),
        # SALT Operator
        find_username("SALT Operator"),
    ],
)
def test_unauthorized_users_cannot_revoke_proposal_permissions(
    username: str, client: TestClient
):
    authenticate(username, client)
    permission = {"proposal_code": PROPOSAL_CODE, "permission_type": "View"}
    response = client.post(BASE_URL + "revoke-proposal-permission", json=permission)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_revoking_permission_for_unknown_user_gives_not_found_error(
    client: TestClient,
) -> None:
    authenticate(find_username("Administrator"), client)
    permission = {"proposal_code": PROPOSAL_CODE, "permission_type": "View"}
    response = client.post("/users/-1/revoke-proposal-permission", json=permission)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_revoking_permission_for_unknown_proposal_code_gives_user_error(
    client: TestClient,
) -> None:
    authenticate(find_username("Administrator"), client)
    permission = {"proposal_code": "2022-2-SCI-099", "permission_type": "View"}
    response = client.post(BASE_URL + "revoke-proposal-permission", json=permission)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_revoking_permission_for_unknown_permission_type_gives_unprocessable_error(
    client: TestClient,
) -> None:
    authenticate(find_username("Administrator"), client)
    permission = {"proposal_code": "2022-2-SCI-099", "permission_type": "IDontExist"}
    response = client.post(BASE_URL + "revoke-proposal-permission", json=permission)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "username",
    [
        # PI of the proposal
        find_username("Principal Investigator", proposal_code=PROPOSAL_CODE),
        # PC of the proposal
        find_username("Principal Contact", proposal_code=PROPOSAL_CODE),
        # SALT Astronomer
        find_username("SALT Astronomer"),
        # Administrator
        find_username("Administrator"),
    ],
)
def test_proposal_permission_can_be_granted_and_revoked(
    username: str, client: TestClient
):
    admin = find_username("Administrator")

    authenticate(username, client)
    permission = {"proposal_code": PROPOSAL_CODE, "permission_type": "View"}

    # Delete any existing permission
    response = client.post(BASE_URL + "revoke-proposal-permission", json=permission)
    assert response.status_code == status.HTTP_200_OK

    # Check that there is no permission
    # This is done as an admin in order to avoid 403 errors
    authenticate(admin, client)
    response = client.get(BASE_URL + "proposal-permissions")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0
    authenticate(username, client)

    # Grant the permission
    response = client.post(BASE_URL + "grant-proposal-permission", json=permission)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == permission

    # Check the permission has been granted
    # This is done as an admin in order to avoid 403 errors
    authenticate(admin, client)
    response = client.get(BASE_URL + "proposal-permissions")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [permission]
    authenticate(username, client)

    # Revoke the permission again
    response = client.post(BASE_URL + "revoke-proposal-permission", json=permission)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == permission

    # Check the permission has been revoked
    # This is done as an admin in order to avoid 403 errors
    authenticate(admin, client)
    response = client.get(BASE_URL + "proposal-permissions")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0


def test_granting_and_revoking_proposal_permission_is_idempotent(client: TestClient):
    authenticate(find_username("Administrator"), client)
    permission = {"proposal_code": PROPOSAL_CODE, "permission_type": "View"}

    # Delete any existing permission
    response = client.post(BASE_URL + "revoke-proposal-permission", json=permission)
    assert response.status_code == status.HTTP_200_OK

    # Check that there is no permission
    response = client.get(BASE_URL + "proposal-permissions")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0

    # Grant the permission twice
    client.post(BASE_URL + "grant-proposal-permission", json=permission)
    response = client.post(BASE_URL + "grant-proposal-permission", json=permission)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == permission

    # Check the permission has been granted
    response = client.get(BASE_URL + "proposal-permissions")
    assert response.json() == [permission]

    # Revoke the permission again, twice
    client.post(BASE_URL + "revoke-proposal-permission", json=permission)
    response = client.post(BASE_URL + "revoke-proposal-permission", json=permission)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == permission

    # Check the permission has been revoked
    response = client.get(BASE_URL + "proposal-permissions")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0
