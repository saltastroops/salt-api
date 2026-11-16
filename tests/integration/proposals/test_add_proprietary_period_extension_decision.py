from typing import Any, Dict
from unittest.mock import patch

from fastapi.testclient import TestClient
from starlette import status

from saltapi.repository.proposal_repository import ProposalRepository
from tests.conftest import authenticate, find_username, not_authenticated

URL = "/proposals/proprietary-period-extension-decision"


def test_add_proprietary_period_extension_decision_returns_401_for_unauthenticated_user(
    client: TestClient,
) -> None:
    not_authenticated(client)
    decision = {
        "request_id": 1,
        "granted_period": 24,
        "reason": "Approved",
    }
    response = client.post(URL, json=decision)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_add_proprietary_period_extension_decision_returns_403_for_non_admin_user(
    client: TestClient,
) -> None:
    investigator = find_username("Investigator", "2020-2-SCI-043")
    authenticate(investigator, client)
    decision = {
        "request_id": 1,
        "granted_period": 24,
        "reason": "Approved",
    }
    response = client.post(URL, json=decision)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_add_proprietary_period_extension_decision_returns_404_for_non_existent_request(
    client: TestClient,
) -> None:
    admin = find_username("Administrator")
    authenticate(admin, client)
    decision = {
        "request_id": 99999999,
        "granted_period": 24,
        "reason": "Approved",
    }
    response = client.post(URL, json=decision)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_add_proprietary_period_extension_decision_success(
    client: TestClient,
    db_connection: Any,
) -> None:
    proposal_code = "2020-2-SCI-043"
    username = find_username("Principal Investigator", proposal_code=proposal_code)
    proposal_repository = ProposalRepository(db_connection)
    proposal_repository.insert_proprietary_period_extension_request(
        proposal_code=proposal_code,
        proprietary_period=36,
        motivation="Requesting extra time for testing decision endpoint",
        username=username,
    )
    from datetime import datetime
    results = proposal_repository.proprietary_period_extension_requests(
        datetime(2000, 1, 1)
    )
    matching = [r for r in results if r["proposal_code"] == proposal_code]
    request_id = matching[-1]["id"]

    admin = find_username("Administrator")
    authenticate(admin, client)
    decision = {
        "request_id": request_id,
        "granted_period": 36,
        "reason": "Approved by TAC / Admin",
    }

    with patch(
        "saltapi.service.proposal_service.ProposalService.update_proprietary_period_in_ssda"
    ) as mock_ssda:
        response = client.post(URL, json=decision)
        assert response.status_code == status.HTTP_200_OK
        mock_ssda.assert_called_once_with(
            proposal_code=proposal_code,
            proprietary_period=36,
        )

    updated_results = proposal_repository.proprietary_period_extension_requests(
        datetime(2000, 1, 1)
    )
    updated_req = [r for r in updated_results if r["id"] == request_id][0]
    assert updated_req["granted_period"] == 36
    assert updated_req["grant_reason"] == "Approved by TAC / Admin"