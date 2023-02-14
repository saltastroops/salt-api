import pytest
from fastapi.testclient import TestClient
from starlette import status

from tests.conftest import authenticate, find_username, not_authenticated

PROPOSALS_URL = "/proposals"


def test_proposal_status_update_requires_authentication(
    client: TestClient,
) -> None:
    proposal_code = "2021-2-LSP-001"
    proposal_status_value = "Active"

    not_authenticated(client)
    response = client.put(
        PROPOSALS_URL + "/" + proposal_code + "/status",
        json={"value": proposal_status_value, "reason": None},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_proposal_status_update_requires_proposal_status(
    client: TestClient,
) -> None:
    proposal_code = "2021-2-LSP-001"
    username = find_username("administrator")
    authenticate(username, client)

    response = client.put(
        PROPOSALS_URL + "/" + proposal_code + "/status",
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_proposal_status_update_requires_valid_proposal_status_value(
    client: TestClient,
) -> None:
    proposal_code = "2023-1-MLT-006"
    username = find_username("administrator")
    authenticate(username, client)

    proposal_status_value = "Wrong status"

    response = client.put(
        PROPOSALS_URL + "/" + proposal_code + "/status",
        json={ "value": proposal_status_value, "reason": None},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "username",
    [
        find_username("Investigator", proposal_code="2019-2-SCI-006"),
        find_username("Principal Contact", proposal_code="2019-2-SCI-006"),
        find_username("Principal Investigator", proposal_code="2019-2-SCI-006"),
        find_username("TAC Member", partner_code="RSA"),
        find_username("TAC Chair", partner_code="RSA"),
    ],
)
def test_proposal_status_update_requires_permissions(
    username: str,
    client: TestClient,
) -> None:
    proposal_code = "2019-2-SCI-006"
    authenticate(username, client)

    proposal_status_value = "Under scientific review"

    response = client.put(
        PROPOSALS_URL + "/" + proposal_code + "/status",
        json={"value": proposal_status_value, "reason": None},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.parametrize(
    "username",
    [
        find_username("Principal Contact", proposal_code="2019-2-SCI-006"),
        find_username("Principal Investigator", proposal_code="2019-2-SCI-006")
    ],
)
def test_pi_and_pc_can_set_proposal_status_to_inactive(
        username: str,
        client: TestClient,
) -> None:
    proposal_code = "2019-2-SCI-006"
    authenticate(username, client)

    proposal_status_value = "Inactive"

    response = client.put(
        PROPOSALS_URL + "/" + proposal_code + "/status",
        json={"value": proposal_status_value, "reason": None},
        )
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.parametrize(
    "username",
    [
        find_username("Principal Contact", proposal_code="2019-2-SCI-006"),
        find_username("Principal Investigator", proposal_code="2019-2-SCI-006")
    ],
)
def test_pi_and_pc_can_not_set_proposal_status_to_active(
        username: str,
        client: TestClient,
) -> None:
    proposal_code = "2019-2-SCI-006"
    authenticate(username, client)

    proposal_status_value = "Active"

    response = client.put(
        PROPOSALS_URL + "/" + proposal_code + "/status",
        json={"value": proposal_status_value, "reason": None},
        )
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.parametrize(
    "username",
    [
        find_username("Principal Contact", proposal_code="2018-2-LSP-001"),
        find_username("Principal Investigator", proposal_code="2018-2-LSP-001")
    ],
)
def  test_pi_and_pc_can_activate_self_activatable_proposal(
        username: str,
        client: TestClient,
) -> None:
    proposal_code = "2018-2-LSP-001"
    authenticate(username, client)

    proposal_status_value = "Active"

    response = client.put(
        PROPOSALS_URL + "/" + proposal_code + "/status",
        json={"value": proposal_status_value, "reason": None},
        )
    assert response.status_code == status.HTTP_200_OK

def test_proposal_status_update_requires_valid_proposal_inactive_reason(
    client: TestClient,
) -> None:
    proposal_code = "2023-1-MLT-006"
    username = find_username("administrator")
    authenticate(username, client)

    proposal_status_value = "Under scientific review"
    proposal_inactive_reason = "Wrong inactive reason"

    response = client.put(
        PROPOSALS_URL + "/" + proposal_code + "/status",
        json={"value": proposal_status_value, "reason": proposal_inactive_reason},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "user_role, proposal_status_value",
    [
        ("administrator", "Active"),
        ("administrator", "Completed"),
        ("administrator", "Superseded"),
        ("administrator", "In preparation"),
        ("salt_astronomer", "In preparation"),
        ("salt_astronomer", "Rejected"),
        ("salt_astronomer", "Under technical review"),
        ("salt_astronomer", "Under scientific review"),
    ],
)
def test_sa_and_admins_may_make_any_status_change(
    user_role: str,
    proposal_status_value: str,
    client: TestClient,
) -> None:
    username = find_username(user_role)
    authenticate(username, client)
    proposal_inactive_reason = None

    proposal_code = "2023-1-MLT-006"
    response = client.put(
        PROPOSALS_URL + "/" + proposal_code + "/status",
        json={"value": proposal_status_value, "reason": proposal_inactive_reason},
    )
    assert response.status_code == status.HTTP_200_OK

    proposal_status = response.json()
    assert proposal_status["value"] == proposal_status_value
    assert proposal_status["reason"] == proposal_inactive_reason

    resp = client.get(PROPOSALS_URL + "/" + proposal_code + "/status")
    assert resp.status_code == status.HTTP_200_OK

    new_block_status = resp.json()

    assert new_block_status["value"] == proposal_status_value
    assert new_block_status["reason"] == proposal_inactive_reason


def test_proposal_status_update_with_inactive_reason(
    client: TestClient,
) -> None:
    proposal_code = "2022-2-SCI-007"
    username = find_username("administrator")
    authenticate(username, client)

    proposal_status_value = "Inactive"
    proposal_inactive_reason = "Undoable"

    response = client.put(
        PROPOSALS_URL + "/" + proposal_code + "/status",
        json={"value": proposal_status_value, "reason": proposal_inactive_reason},
    )
    assert response.status_code == status.HTTP_200_OK

    proposal_status = response.json()

    assert proposal_status["value"] == proposal_status_value
    assert proposal_status["reason"] == proposal_inactive_reason

    resp = client.get(PROPOSALS_URL + "/" + proposal_code + "/status")
    assert resp.status_code == status.HTTP_200_OK

    new_block_status = resp.json()

    assert new_block_status["value"] == proposal_status_value
    assert new_block_status["reason"] == proposal_inactive_reason
