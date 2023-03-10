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
    approve = False
    not_authenticated(client)
    response = client.put(
        f"{PROPOSALS_URL}/{proposal_code}/approvals/{user_id}",
        json=approve,
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_investigator_approval_proposal_status_update_requires_an_existing_proposal_code(
    client: TestClient,
) -> None:
    proposal_code = "2099-1-SCI-001"
    user_id = 1006
    username = find_username("administrator")
    approve = True

    authenticate(username, client)

    response = client.put(
        f"{PROPOSALS_URL}/{proposal_code}/approvals/{user_id}",
        json=approve,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_investigator_approval_proposal_status_update_requires_an_existing_user_id(
    client: TestClient,
) -> None:
    proposal_code = "2021-2-LSP-001"
    user_id = 100000000
    username = find_username("administrator")
    approve = False

    authenticate(username, client)

    response = client.put(
        f"{PROPOSALS_URL}/{proposal_code}/approvals/{user_id}",
        json=approve,
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
    approve = "Wrong status"

    authenticate(username, client)

    response = client.put(
        f"{PROPOSALS_URL}/{proposal_code}/approvals/{user_id}",
        json=approve,
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
    approve = False
    authenticate(username, client)

    response = client.put(
        f"{PROPOSALS_URL}/{proposal_code}/approvals/{user_id}",
        json=approve,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_investigator_approval_proposal_status_update_forbids_a_permitted_user_from_updating_for_another_user(
    client: TestClient,
) -> None:
    proposal_code = "2019-2-SCI-006"
    username = find_username("Investigator", proposal_code="2019-2-SCI-006")
    authenticate(username, client)

    pc_user_id = (
        1413  # user id for the Principal Contact user in proposal 2019-2-SCI-006
    )
    approve = False
    authenticate(username, client)

    response = client.put(
        f"{PROPOSALS_URL}/{proposal_code}/approvals/{pc_user_id}",
        json=approve,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_investigator_approval_proposal_status_update_for_an_administrator(
    client: TestClient,
) -> None:
    proposal_code = "2019-2-SCI-006"
    username = find_username("Administrator")
    authenticate(username, client)

    user_id = 1413  # user id for the Principal Contact user in proposal 2019-2-SCI-006
    approve = True

    response = client.put(
        f"{PROPOSALS_URL}/{proposal_code}/approvals/{user_id}",
        json=approve,
    )
    assert response.status_code == status.HTTP_200_OK

    resp = client.get(f"{PROPOSALS_URL}/{proposal_code}")

    assert resp.status_code == status.HTTP_200_OK

    proposal = resp.json()

    investigator = [i for i in proposal["investigators"] if i["id"] == user_id]

    assert investigator[0]["has_approved_proposal"] == 1


def test_investigator_approval_proposal_status_update_for_pc(
    client: TestClient,
) -> None:
    proposal_code = "2019-2-SCI-006"
    username = find_username("Principal Contact", proposal_code="2019-2-SCI-006")
    authenticate(username, client)

    user_id = 1413  # user id of the Principal Contact user
    approve = False

    response = client.put(
        f"{PROPOSALS_URL}/{proposal_code}/approvals/{user_id}",
        json=approve,
    )
    assert response.status_code == status.HTTP_200_OK

    resp = client.get(f"{PROPOSALS_URL}/{proposal_code}")

    assert resp.status_code == status.HTTP_200_OK

    proposal = resp.json()

    investigator = [i for i in proposal["investigators"] if i["id"] == user_id]

    assert investigator[0]["has_approved_proposal"] == 0


def test_investigator_approval_proposal_status_update_for_an_investigator(
    client: TestClient,
) -> None:
    proposal_code = "2019-2-SCI-006"
    username = find_username("Investigator", proposal_code="2019-2-SCI-006")
    authenticate(username, client)

    user_id = 656  # user id for investigator in proposal 2019-2-SCI-006
    approve = False

    response = client.put(
        f"{PROPOSALS_URL}/{proposal_code}/approvals/{user_id}",
        json=approve,
    )
    assert response.status_code == status.HTTP_200_OK

    resp = client.get(f"{PROPOSALS_URL}/{proposal_code}")

    assert resp.status_code == status.HTTP_200_OK

    proposal = resp.json()

    investigator = [i for i in proposal["investigators"] if i["id"] == user_id]

    assert investigator[0]["has_approved_proposal"] == 0
