from datetime import datetime
from typing import Any, List, Optional

import pytest
import pytz
from freezegun import freeze_time
from sqlalchemy.engine import Connection

# TODO: Add more tests
from saltapi.exceptions import NotFoundError
from saltapi.repository.submission_repository import SubmissionRepository
from saltapi.service.submission import SubmissionMessageType, SubmissionStatus
from saltapi.service.user import User

FROZEN_NOW = "2022-08-26T21:23:55"


def _dummy_user() -> User:
    return User(
        id=4,
        username="john",
        given_name="John",
        family_name="Doe",
        email="john@example.com",
        alternative_emails=[],
        password_hash="abc",
        affiliations=[],
        roles=[],
    )


def test_get_submission(db_connection: Connection) -> None:
    """Test that submission details are returned."""
    submission_repository = SubmissionRepository(db_connection)
    submission = submission_repository.get("a63e548d-ffa5-4213-ad8a-b44b1ec8a01c")
    assert submission["proposal_code"] is None
    assert submission["submitter_id"] == 1243
    assert submission["status"] == SubmissionStatus.FAILED
    assert submission["started_at"] == datetime(
        2022, 4, 25, 10, 7, 37, 0, tzinfo=pytz.utc
    )
    assert submission["finished_at"] == datetime(
        2022, 4, 25, 10, 10, 10, 0, tzinfo=pytz.utc
    )


def test_get_submission_fails_for_non_existing_identifier(
    db_connection: Connection,
) -> None:
    """Test that an error is raised for a non-existing identifier."""
    submission_repository = SubmissionRepository(db_connection)
    with pytest.raises(NotFoundError):
        submission_repository.get("idontexist")


def test_get_log_entries_for_existing_identifier(db_connection: Connection) -> None:
    """Test that log entries are returned."""
    submission_repository = SubmissionRepository(db_connection)
    log_entries = submission_repository.get_log_entries(
        "a63e548d-ffa5-4213-ad8a-b44b1ec8a01c"
    )

    assert len(log_entries) == 1
    assert log_entries[0]["entry_number"] == 1
    assert log_entries[0]["message_type"] == SubmissionMessageType.INFO
    assert log_entries[0]["message"] == "Starting submission."
    assert log_entries[0]["logged_at"] == datetime(
        2022, 4, 25, 12, 7, 38, 0, tzinfo=pytz.utc
    )


def test_get_log_entries_for_non_existing_identifier(db_connection: Connection) -> None:
    """Test that an empty list is returned for a non-existing identifier."""
    submission_repository = SubmissionRepository(db_connection)
    log_entries = submission_repository.get_log_entries("idontexist")

    assert len(log_entries) == 0


def test_get_log_entries_from_entry_number(db_connection: Connection) -> None:
    """Test that the returned log entries can be limited."""
    submission_repository = SubmissionRepository(db_connection)
    user = _dummy_user()
    identifier = submission_repository.create(user=user, proposal_code=None)

    submission_repository.create_log_entry(
        identifier, SubmissionMessageType.INFO, "Message 1"
    )
    submission_repository.create_log_entry(
        identifier, SubmissionMessageType.ERROR, "Message 2"
    )
    submission_repository.create_log_entry(
        identifier, SubmissionMessageType.WARNING, "Message 3"
    )

    log_entries = submission_repository.get_log_entries(identifier, from_entry_number=2)

    assert len(log_entries) == 2
    assert log_entries[0]["entry_number"] == 2
    assert log_entries[1]["entry_number"] == 3


@pytest.mark.parametrize("from_entry_number", [1, 2, 3])
@freeze_time(FROZEN_NOW)
def test_get_progress(from_entry_number: int, db_connection: Connection) -> None:
    """Test that the correct progress details are returned."""
    submission_repository = SubmissionRepository(db_connection)
    user = _dummy_user()
    identifier = submission_repository.create(user=user, proposal_code=None)

    all_log_entries: List[Any] = [
        {
            "entry_number": 1,
            "message_type": SubmissionMessageType.INFO,
            "message": "Message 1",
        },
        {
            "entry_number": 2,
            "message_type": SubmissionMessageType.ERROR,
            "message": "Message 2",
        },
        {
            "entry_number": 3,
            "message_type": SubmissionMessageType.WARNING,
            "message": "Message 3",
        },
    ]
    for log_entry in all_log_entries:
        submission_repository.create_log_entry(
            identifier, log_entry["message_type"], log_entry["message"]
        )

    submission_repository.finish(identifier, SubmissionStatus.SUCCESSFUL)
    progress = submission_repository.get_progress(identifier, from_entry_number)

    # Check the dates and remove them to facilitate comparison
    now = pytz.utc.localize(datetime.utcnow())
    for log_entry in progress["log_entries"]:
        assert abs((log_entry["logged_at"] - now).total_seconds()) < 5
        del log_entry["logged_at"]

    assert progress["status"] == SubmissionStatus.SUCCESSFUL
    assert progress["log_entries"] == all_log_entries[from_entry_number - 1 :]  # noqa


@pytest.mark.parametrize("proposal_code", [None, "2021-2-SCI-004"])
@freeze_time(FROZEN_NOW)
def test_create_submission(
    proposal_code: Optional[str], db_connection: Connection
) -> None:
    """Test that a submission is created."""
    now = pytz.utc.localize(datetime.utcnow())

    submission_repository = SubmissionRepository(db_connection)
    user = _dummy_user()
    identifier = submission_repository.create(user=user, proposal_code=proposal_code)
    submission = submission_repository.get(identifier)
    assert submission["submitter_id"] == user.id
    assert submission["proposal_code"] == proposal_code
    assert submission["status"] == SubmissionStatus.IN_PROGRESS
    assert abs((submission["started_at"] - now).total_seconds()) < 5
    assert submission["finished_at"] is None


def test_create_submission_fails_for_unknown_proposal_code(
    db_connection: Connection,
) -> None:
    """Test that a submission cannot be created for a non-existing proposal code."""
    submission_repository = SubmissionRepository(db_connection)
    user = _dummy_user()
    with pytest.raises(NotFoundError) as excinfo:
        submission_repository.create(user=user, proposal_code="idontexist")
    assert "idontexist" in str(excinfo.value)


def test_create_log_entry(db_connection: Connection) -> None:
    """Test creating a log entry."""
    submission_repository = SubmissionRepository(db_connection)
    user = _dummy_user()
    identifier = submission_repository.create(user=user, proposal_code=None)

    submission_repository.create_log_entry(
        identifier, SubmissionMessageType.INFO, "Checking exposure times."
    )
    submission_repository.create_log_entry(
        identifier, SubmissionMessageType.ERROR, "An exposure time cannot be negative."
    )

    log_entries = submission_repository.get_log_entries(identifier)

    assert len(log_entries) == 2

    assert log_entries[0]["entry_number"] == 1
    assert log_entries[0]["message_type"] == SubmissionMessageType.INFO
    assert log_entries[0]["message"] == "Checking exposure times."

    assert log_entries[1]["entry_number"] == 2
    assert log_entries[1]["message_type"] == SubmissionMessageType.ERROR
    assert log_entries[1]["message"] == "An exposure time cannot be negative."


def test_create_log_entry_fails_for_non_existing_submission_identifier(
    db_connection: Connection,
) -> None:
    """Test no log entry can be created for a non-existing submission identifier."""
    submission_repository = SubmissionRepository(db_connection)
    with pytest.raises(NotFoundError) as excinfo:
        submission_repository.create_log_entry(
            "idontexist", SubmissionMessageType.INFO, "Checking exposure times."
        )

    assert "idontexist" in str(excinfo.value)


@pytest.mark.parametrize(
    "status",
    [
        SubmissionStatus.FAILED,
        SubmissionStatus.IN_PROGRESS,
        SubmissionStatus.SUCCESSFUL,
    ],
)
@freeze_time(FROZEN_NOW)
def test_finish_submission(status: SubmissionStatus, db_connection: Connection) -> None:
    """Test finishing a submission."""
    submission_repository = SubmissionRepository(db_connection)
    user = _dummy_user()
    identifier = submission_repository.create(user=user, proposal_code=None)

    submission_repository.finish(identifier, status)

    submission = submission_repository.get(identifier)

    now = pytz.utc.localize(datetime.utcnow())
    assert submission["status"] == status
    assert abs((submission["finished_at"] - now).total_seconds()) < 5


def test_finish_submission_fails_for_non_existing_submission_identifier(
    db_connection: Connection,
) -> None:
    """Test finishing a submission fails for a non-existing submission identifier."""
    submission_repository = SubmissionRepository(db_connection)
    with pytest.raises(NotFoundError) as excinfo:
        submission_repository.finish("idontexist", SubmissionStatus.SUCCESSFUL)
    assert "dontexist" in str(excinfo.value)
