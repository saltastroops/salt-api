import pytest
from fastapi.testclient import TestClient
from starlette import status

from tests.conftest import authenticate, find_username, not_authenticated

PROPOSALS_URL = "/proposals"


def test_investigator_approval_proposal_status_update_requires_authentication(
    client: TestClient,
) -> None:
    proposal_code = "2021-2-LSP-001"
    user_id = 1006
    data = {"approved": False}
    not_authenticated(client)
    response = client.put(
        f"{PROPOSALS_URL}/{proposal_code}/approvals/{user_id}",
        json=data,
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_investigator_approval_proposal_status_update_requires_an_existing_proposal_code(
    client: TestClient,
) -> None:
    proposal_code = "2099-1-SCI-001"
    user_id = 1006
    username = find_username("administrator")
    data = {"approved": True}

    authenticate(username, client)

    response = client.put(
        f"{PROPOSALS_URL}/{proposal_code}/approvals/{user_id}",
        json=data,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_investigator_approval_proposal_status_update_requires_an_existing_user_id(
    client: TestClient,
) -> None:
    proposal_code = "2021-2-LSP-001"
    user_id = 100000000
    username = find_username("administrator")
    data = {"approved": False}

    authenticate(username, client)

    response = client.put(
        f"{PROPOSALS_URL}/{proposal_code}/approvals/{user_id}",
        json=data,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_investigator_approval_proposal_status_update_requires_approval_status(
    client: TestClient,
) -> None:
    proposal_code = "2021-2-LSP-001"
    username = find_username("administrator")
    user_id = 10

    authenticate(username, client)

    response = client.put(
        f"{PROPOSALS_URL}/{proposal_code}/approvals/{user_id}",
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_investigator_approval_proposal_status_update_requires_valid_approval_status(
    client: TestClient,
) -> None:
    proposal_code = "2019-2-SCI-006"
    username = find_username("Investigator", proposal_code="2019-2-SCI-006")
    user_id = 656  # user id of the above user
    data = {"approved": "Wrong status"}

    authenticate(username, client)

    response = client.put(
        f"{PROPOSALS_URL}/{proposal_code}/approvals/{user_id}",
        json=data,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "username",
    [
        find_username("SALT Astronomer"),
        find_username("TAC Member", partner_code="RSA"),
        find_username("TAC Chair", partner_code="RSA"),
    ],
)
def test_investigator_approval_proposal_status_update_requires_permissions(
    username: str,
    client: TestClient,
) -> None:
    proposal_code = "2019-2-SCI-006"
    user_id = 656  # user id for investigator in proposal 2019-2-SCI-006
    data = {"approved": False}
    authenticate(username, client)

    response = client.put(
        f"{PROPOSALS_URL}/{proposal_code}/approvals/{user_id}",
        json=data,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_investigator_approval_proposal_status_update_forbids_a_permitted_user_from_updating_for_another_user(
    client: TestClient,
) -> None:
    proposal_code = "2019-2-SCI-006"
    username = find_username("Principal Contact", proposal_code="2019-2-SCI-006")
    authenticate(username, client)

    pc_user_id = 656  # user id for investigator in proposal 2019-2-SCI-006
    data = {"approved": False}
    authenticate(username, client)

    response = client.put(
        f"{PROPOSALS_URL}/{proposal_code}/approvals/{pc_user_id}",
        json=data,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize(
    "username, user_id, approved",
    [
        (find_username("Administrator"), 1413, True),
        (find_username("Investigator", proposal_code="2019-2-SCI-006"), 656, False),
    ],
)
def test_investigator_approval_proposal_status_update(
    username: str,
    user_id: int,
    approved: bool,
    client: TestClient,
) -> None:
    proposal_code = "2019-2-SCI-006"
    authenticate(username, client)

    # First status update
    first_update_data = {"approved": approved}

    first_update_response = client.put(
        f"{PROPOSALS_URL}/{proposal_code}/approvals/{user_id}",
        json=first_update_data,
    )
    assert first_update_response.status_code == status.HTTP_200_OK

    resp = client.get(f"{PROPOSALS_URL}/{proposal_code}")

    assert resp.status_code == status.HTTP_200_OK

    proposal = resp.json()

    investigators = [i for i in proposal["investigators"] if i["id"] == user_id]

    has_approved_proposal = investigators[0]["has_approved_proposal"]

    assert has_approved_proposal if approved else not has_approved_proposal

    # Second status update
    second_update_data = {"approved": not approved}

    second_update_response = client.put(
        f"{PROPOSALS_URL}/{proposal_code}/approvals/{user_id}",
        json=second_update_data,
    )
    assert second_update_response.status_code == status.HTTP_200_OK

    resp = client.get(f"{PROPOSALS_URL}/{proposal_code}")

    assert resp.status_code == status.HTTP_200_OK

    proposal = resp.json()

    investigators = [i for i in proposal["investigators"] if i["id"] == user_id]

    has_approved_proposal = investigators[0]["has_approved_proposal"]

    assert has_approved_proposal if not approved else not has_approved_proposal


