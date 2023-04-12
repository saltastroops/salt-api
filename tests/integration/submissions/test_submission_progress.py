import copy
from datetime import datetime
from typing import Any, Callable, Dict, List, Tuple

import pytest
import pytz
from fastapi.testclient import TestClient
from sqlalchemy.engine import Connection
from starlette.websockets import WebSocketDisconnect

import saltapi.web.api.submissions
from saltapi.repository.submission_repository import SubmissionRepository
from saltapi.service.submission import SubmissionMessageType, SubmissionStatus
from saltapi.service.user import User
from tests.conftest import find_username
from tests.markers import noserver


class MockSubmissionRepository:
    def __init__(self, submitter_id: int, details_sequence: List[Dict[str, Any]]):
        self.submitter_id = submitter_id
        self.details_sequence = details_sequence
        self.counter = 0

    def get(self, identifier: str) -> Dict[str, Any]:
        return {"submitter_id": self.submitter_id}

    def get_progress(self, identifier: str, from_entry_number: str) -> Any:
        details = self.details_sequence[self.counter]
        self.counter += 1
        details["log_entries"] = [
            log_entry
            for log_entry in details["log_entries"]
            if log_entry["entry_number"] >= from_entry_number
        ]
        return details

    def __call__(self, *args: Any, **kwargs: Any) -> "MockSubmissionRepository":
        # This method is needed as we are mocking a class with a class instance. So the
        # code will try to call a constructor, and we must handle this.
        return self


def _full_details_sequence(
    details_sequence: List[Any],
) -> List[Dict[str, Any]]:
    sequence = []
    for d in details_sequence:
        full_details = {
            "status": d[0].value,
            "log_entries": [
                {
                    "entry_number": dd[0],
                    "message_type": dd[1].value,
                    "message": f"Message {dd[0]}",
                    "logged_at": pytz.utc.localize(datetime(2022, 5, 6, 0, 9, 13, 0)),
                }
                for dd in d[1]
            ],
        }
        if len(d) > 2:
            full_details["proposal_code"] = d[2]
        sequence.append(full_details)

    return sequence


def _dummy_user(id: int, username: str) -> User:
    return User(
        id=id,
        given_name="John",
        family_name="Doe",
        email="john@example,com",
        alternative_emails=[],
        username=username,
        password_hash="1234",
        affiliations=[],
        roles=[],
    )


def _mock_find_user_from_token(id: int, username: str) -> Callable[[str], User]:
    def f(token: str) -> User:
        if token != "secret":
            raise ValueError("Invalid token")
        return _dummy_user(id, username)

    return f


def _serialize_logged_at(submission_progress: Dict[str, Any]) -> Dict[str, Any]:
    sp = copy.deepcopy(submission_progress)
    for log_entry in sp["log_entries"]:
        log_entry["logged_at"] = log_entry["logged_at"].isoformat()
    return sp


@noserver
def test_submission_log_requires_authentication(
    db_connection: Connection, client: TestClient
) -> None:
    """Test that you have to be authenticated to view a submission log."""
    submission_repository = SubmissionRepository(db_connection)
    username = find_username("administrator")
    submission_identifier = submission_repository.create(
        _dummy_user(42, username), "2021-2-SCI-003"
    )

    with client.websocket_connect(
        f"/submissions/{submission_identifier}/progress/ws"
    ) as websocket:
        with pytest.raises(WebSocketDisconnect) as excinfo:
            websocket.send_text("abc")
            websocket.receive_text()
        assert "authenticated" in str(excinfo.value) and "/token" in str(excinfo.value)


@noserver
def test_submission_log_requires_existing_identifier(
    db_connection: Connection, client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test that the submission identifier must exist."""
    submission_identifier = "idontexist"
    username = find_username("administrator")
    monkeypatch.setattr(
        saltapi.web.api.submissions,
        "find_user_from_token",
        _mock_find_user_from_token(42, username),
    )

    with client.websocket_connect(
        f"/submissions/{submission_identifier}/progress/ws"
    ) as websocket:
        with pytest.raises(WebSocketDisconnect) as excinfo:
            websocket.send_text("secret")
            websocket.receive_text()
        assert submission_identifier in str(excinfo.value)


def test_submission_log_can_only_be_accessed_by_submitter(
    db_connection: Connection, client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test that only the user who made a submission can view its log."""
    submission_repository = SubmissionRepository(db_connection)
    proposal_code = "2022-1-SCI-006"
    submission_identifier = submission_repository.create(
        _dummy_user(1, "someone"), proposal_code
    )

    monkeypatch.setattr(
        saltapi.web.api.submissions,
        "find_user_from_token",
        _mock_find_user_from_token(42, "someone_else"),
    )

    with client.websocket_connect(
        f"/submissions/{submission_identifier}/progress/ws"
    ) as websocket:
        with pytest.raises(WebSocketDisconnect) as excinfo:
            websocket.send_text("secret")
            websocket.receive_text()
        assert "someone else" in str(excinfo.value)


@pytest.mark.parametrize(
    "details_sequence",
    [
        [
            (SubmissionStatus.IN_PROGRESS, [(1, SubmissionMessageType.INFO)]),
            (SubmissionStatus.SUCCESSFUL, []),
        ],
        [
            (SubmissionStatus.IN_PROGRESS, [(1, SubmissionMessageType.INFO)]),
            (
                SubmissionStatus.IN_PROGRESS,
                [(2, SubmissionMessageType.WARNING), (3, SubmissionMessageType.INFO)],
            ),
            (SubmissionStatus.FAILED, [(4, SubmissionMessageType.INFO)]),
        ],
        [
            (SubmissionStatus.IN_PROGRESS, [(1, SubmissionMessageType.INFO)]),
            (SubmissionStatus.IN_PROGRESS, []),
            (
                SubmissionStatus.IN_PROGRESS,
                [(2, SubmissionMessageType.WARNING), (3, SubmissionMessageType.INFO)],
            ),
            (SubmissionStatus.IN_PROGRESS, []),
            (SubmissionStatus.FAILED, [(4, SubmissionMessageType.INFO)]),
        ],
    ],
)
def test_status_and_log_entry_changes_are_returned(
    details_sequence: List[
        Tuple[SubmissionStatus, List[Tuple[int, SubmissionMessageType]]]
    ],
    db_connection: Connection,
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test that the correct submission status and log entries are returned."""
    submission_repository = SubmissionRepository(db_connection)
    proposal_code = "2022-1-SCI-006"
    submission_identifier = submission_repository.create(
        _dummy_user(1, "someone"), proposal_code
    )

    monkeypatch.setattr(
        saltapi.web.api.submissions,
        "find_user_from_token",
        _mock_find_user_from_token(1, "someone"),
    )

    full_details_sequence = _full_details_sequence(details_sequence)
    expected_details_sequence = _full_details_sequence(details_sequence)
    monkeypatch.setattr(
        saltapi.web.api.submissions,
        "SubmissionRepository",
        MockSubmissionRepository(1, full_details_sequence),
    )
    monkeypatch.setattr(saltapi.web.api.submissions, "TIME_BETWEEN_DB_QUERIES", 0)

    with client.websocket_connect(
        f"/submissions/{submission_identifier}/progress/ws"
    ) as websocket:
        websocket.send_text("secret")
        for details in expected_details_sequence:
            message = websocket.receive_json()
            assert message == _serialize_logged_at(details)


def test_proposal_code_is_included_if_sent(
    db_connection: Connection, client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    details_sequence = [
        (SubmissionStatus.IN_PROGRESS, [(1, SubmissionMessageType.INFO)]),
        (
            SubmissionStatus.SUCCESSFUL,
            [(2, SubmissionMessageType.INFO)],
            "2022-1-SCI-014",
        ),
    ]
    submission_repository = SubmissionRepository(db_connection)
    proposal_code = "2022-1-SCI-006"
    submission_identifier = submission_repository.create(
        _dummy_user(1, "someone"), proposal_code
    )

    monkeypatch.setattr(
        saltapi.web.api.submissions,
        "find_user_from_token",
        _mock_find_user_from_token(1, "someone"),
    )

    full_details_sequence = _full_details_sequence(details_sequence)
    expected_details_sequence = _full_details_sequence(details_sequence)
    monkeypatch.setattr(
        saltapi.web.api.submissions,
        "SubmissionRepository",
        MockSubmissionRepository(1, full_details_sequence),
    )
    monkeypatch.setattr(saltapi.web.api.submissions, "TIME_BETWEEN_DB_QUERIES", 0)

    with client.websocket_connect(
        f"/submissions/{submission_identifier}/progress/ws"
    ) as websocket:
        websocket.send_text("secret")
        for details in expected_details_sequence:
            message = websocket.receive_json()
            assert message == _serialize_logged_at(details)


@pytest.mark.parametrize(
    "from_entry_number,received_details_sequence",
    [
        (
            1,
            [
                (SubmissionStatus.IN_PROGRESS, [(1, SubmissionMessageType.INFO)]),
                (SubmissionStatus.IN_PROGRESS, []),
                (
                    SubmissionStatus.IN_PROGRESS,
                    [
                        (2, SubmissionMessageType.WARNING),
                        (3, SubmissionMessageType.INFO),
                    ],
                ),
                (SubmissionStatus.IN_PROGRESS, []),
                (SubmissionStatus.FAILED, [(4, SubmissionMessageType.INFO)]),
            ],
        ),
        (
            2,
            [
                (SubmissionStatus.IN_PROGRESS, []),
                (SubmissionStatus.IN_PROGRESS, []),
                (
                    SubmissionStatus.IN_PROGRESS,
                    [
                        (2, SubmissionMessageType.WARNING),
                        (3, SubmissionMessageType.INFO),
                    ],
                ),
                (SubmissionStatus.IN_PROGRESS, []),
                (SubmissionStatus.FAILED, [(4, SubmissionMessageType.INFO)]),
            ],
        ),
        (
            3,
            [
                (SubmissionStatus.IN_PROGRESS, []),
                (SubmissionStatus.IN_PROGRESS, []),
                (SubmissionStatus.IN_PROGRESS, [(3, SubmissionMessageType.INFO)]),
                (SubmissionStatus.IN_PROGRESS, []),
                (SubmissionStatus.FAILED, [(4, SubmissionMessageType.INFO)]),
            ],
        ),
        (
            1000,
            [
                (SubmissionStatus.IN_PROGRESS, []),
                (SubmissionStatus.IN_PROGRESS, []),
                (SubmissionStatus.IN_PROGRESS, []),
                (SubmissionStatus.IN_PROGRESS, []),
                (SubmissionStatus.FAILED, []),
            ],
        ),
    ],
)
def test_submission_log_entries_can_be_skipped(
    from_entry_number: int,
    db_connection: Connection,
    received_details_sequence: List[
        Tuple[SubmissionStatus, List[Tuple[int, SubmissionMessageType]]]
    ],
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    submission_repository = SubmissionRepository(db_connection)
    proposal_code = "2022-1-SCI-006"
    submission_identifier = submission_repository.create(
        _dummy_user(1, "someone"), proposal_code
    )

    details_sequence: List[Any] = [
        (SubmissionStatus.IN_PROGRESS, [(1, SubmissionMessageType.INFO)]),
        (SubmissionStatus.IN_PROGRESS, []),
        (
            SubmissionStatus.IN_PROGRESS,
            [(2, SubmissionMessageType.WARNING), (3, SubmissionMessageType.INFO)],
        ),
        (SubmissionStatus.IN_PROGRESS, []),
        (SubmissionStatus.FAILED, [(4, SubmissionMessageType.INFO)]),
    ]

    monkeypatch.setattr(
        saltapi.web.api.submissions,
        "find_user_from_token",
        _mock_find_user_from_token(1, "someone"),
    )

    full_details_sequence = _full_details_sequence(details_sequence)
    expected_details_sequence = _full_details_sequence(received_details_sequence)
    monkeypatch.setattr(
        saltapi.web.api.submissions,
        "SubmissionRepository",
        MockSubmissionRepository(1, full_details_sequence),
    )
    monkeypatch.setattr(saltapi.web.api.submissions, "TIME_BETWEEN_DB_QUERIES", 0)

    with client.websocket_connect(
        (
            f"/submissions/{submission_identifier}/progress/ws"
            f"?from-entry-number={from_entry_number}"
        ),
    ) as websocket:
        websocket.send_text("secret")
        for details in expected_details_sequence:
            message = websocket.receive_json()
            assert message == _serialize_logged_at(details)
