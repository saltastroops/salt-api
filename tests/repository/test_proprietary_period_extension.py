from datetime import date, datetime
from types import SimpleNamespace
from unittest.mock import MagicMock

from saltapi.repository.proposal_repository import ProposalRepository


def test_proposals_requesting_more_time_returns_latest_with_history() -> None:
    connection = MagicMock()
    connection.execute.return_value = [
        SimpleNamespace(
            id=6,
            proposal_code="P-3",
            request_reason="No history",
            made_at=datetime(2026, 4, 1, 9),
            grant_reason=None,
            granted_period=None,
            requester_name="Ada Lovelace",
            requester_email="ada@example.com",
            current_period=18,
            requested_period=24,
        ),
        SimpleNamespace(
            id=4,
            proposal_code="P-2",
            request_reason="Only recent request",
            made_at=datetime(2026, 3, 1, 9),
            grant_reason=None,
            granted_period=None,
            requester_name="Ada Lovelace",
            requester_email="ada@example.com",
            current_period=12,
            requested_period=18,
        ),
        SimpleNamespace(
            id=3,
            proposal_code="P-1",
            request_reason="Latest request",
            made_at=datetime(2026, 2, 1, 9),
            grant_reason="Latest grant",
            granted_period=36,
            requester_name="Ada Lovelace",
            requester_email="ada@example.com",
            current_period=24,
            requested_period=36,
        ),
        SimpleNamespace(
            id=2,
            proposal_code="P-1",
            request_reason="Latest timestamp tie, lower id",
            made_at=datetime(2026, 2, 1, 9),
            grant_reason=None,
            granted_period=None,
            requester_name="Ada Lovelace",
            requester_email="ada@example.com",
            current_period=24,
            requested_period=24,
        ),
        SimpleNamespace(
            id=5,
            proposal_code="P-2",
            request_reason="Older request",
            made_at=datetime(2025, 1, 1, 9),
            grant_reason=None,
            granted_period=None,
            requester_name="Ada Lovelace",
            requester_email="ada@example.com",
            current_period=12,
            requested_period=6,
        ),
        SimpleNamespace(
            id=1,
            proposal_code="P-1",
            request_reason="Older request",
            made_at=datetime(2025, 1, 1, 9),
            grant_reason="Earlier grant",
            granted_period=12,
            requester_name="Ada Lovelace",
            requester_email="ada@example.com",
            current_period=24,
            requested_period=12,
        ),
    ]
    repository = ProposalRepository(connection)
    release_date_calls = []

    def get_release_date(period: int, proposal_code: str) -> date:
        release_date_calls.append(proposal_code)
        return date(2030, 1, 1)

    repository.get_release_date = get_release_date
    requests = repository.proprietary_period_extension_requests(datetime(2026, 1, 1))

    assert [request["proposal_code"] for request in requests] == ["P-3", "P-2", "P-1"]
    assert [request["id"] for request in requests] == [6, 4, 3]
    assert requests[0]["previous_requests"] == []
    assert requests[0]["current_request"]["request_motivation"] == "No history"
    assert requests[1]["current_request"]["request_motivation"] == "Only recent request"
    assert requests[1]["previous_requests"][0]["made_at"] == datetime(2025, 1, 1, 9)
    assert requests[1]["previous_requests"][0]["request_motivation"] == "Older request"
    assert requests[1]["granted_period"] is None
    assert requests[2]["current_request"]["request_motivation"] == "Latest request"
    assert requests[2]["previous_requests"][0]["request_motivation"] == (
        "Latest timestamp tie, lower id"
    )
    assert requests[2]["previous_requests"][1]["request_motivation"] == "Older request"
    assert requests[2]["grant_reason"] == "Latest grant"
    assert requests[2]["granted_period"] == 36
    assert requests[2]["current_request"]["requested_period"] == 36
    assert all(request["release_date"] == date(2030, 1, 1) for request in requests)
    assert release_date_calls == ["P-3", "P-2", "P-1"]

    statement, parameters = connection.execute.call_args.args
    normalized_statement = " ".join(str(statement).split())
    assert parameters == {"start_date": datetime(2026, 1, 1).date()}
    assert "WHERE RecentPPER.MadeAt >= :start_date" in normalized_statement
    assert "ORDER BY PPER.MadeAt DESC, PPER.ProprietaryPeriodExtensionRequest_Id DESC" in (
        normalized_statement
    )


def test_proposals_requesting_more_time_returns_empty_result() -> None:
    connection = MagicMock()
    connection.execute.return_value = []
    repository = ProposalRepository(connection)

    assert repository.proprietary_period_extension_requests(datetime(2026, 1, 1)) == []

    _, parameters = connection.execute.call_args.args
    assert parameters == {"start_date": datetime(2026, 1, 1).date()}