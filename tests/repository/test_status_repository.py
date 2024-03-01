from datetime import datetime, timedelta
from typing import List

import pytest
import pytz
from sqlalchemy.engine import Connection

from saltapi.repository.status_repository import (
    StatusRepository,
    SubsystemStatusDetails,
)


def _default_status_updates() -> List[SubsystemStatusDetails]:
    status: List[SubsystemStatusDetails] = []
    for index, subsystem in enumerate(StatusRepository.ALL_SUBSYSTEMS):
        status_changed_at = pytz.utc.localize(datetime(2024, 2, 28, 12, 0, 0, 0))
        expected_available_again_at = status_changed_at + timedelta(days=1)
        subsystem_status = SubsystemStatusDetails(
            subsystem=subsystem,
            status="Unavailable",
            status_changed_at=status_changed_at,
            reason=f"{subsystem} is not working",
            expected_available_again_at=expected_available_again_at,
            reporting_user=f"{subsystem} User",
        )

        # Make the datetimes unique
        time_shift = timedelta(minutes=index)
        subsystem_status["status_changed_at"] += time_shift  # type: ignore
        subsystem_status["expected_available_again_at"] += time_shift  # type: ignore

        status.append(subsystem_status)

    return status


def _find_subsystem_status(
    status: List[SubsystemStatusDetails], subsystem: str
) -> SubsystemStatusDetails:
    for s in status:
        if s["subsystem"] == subsystem:
            return s
    raise ValueError(f"Unsupported subsystem: {subsystem}")


def test_get_status(db_connection: Connection) -> None:
    # The correct status details are returned.

    # Create status updates which are unique per subsystem
    status_repository = StatusRepository(db_connection)
    status_updates = _default_status_updates()
    for subsystem in StatusRepository.ALL_SUBSYSTEMS:
        status_update = _find_subsystem_status(status_updates, subsystem)
        status_repository.update_status(status_update)

    # Check that we can retrieve the status details
    status = status_repository.get_status()
    assert len(status) == len(status_updates)
    for s in status:
        subsystem = s["subsystem"]
        assert _find_subsystem_status(status, subsystem) == _find_subsystem_status(
            status_updates, subsystem
        )


def test_add_status_update(db_connection: Connection) -> None:
    # A subsystem status update is saved, and other subsystems are unaffected.

    # Add a status update for each subsystem
    status_repository = StatusRepository(db_connection)
    status_updates = _default_status_updates()
    for status_update in status_updates:
        status_repository.update_status(status_update)

    # Add another status update, but this time only for RSS
    timeshift = timedelta(minutes=25)
    original_rss_status_update = _find_subsystem_status(status_updates, "RSS")
    rss_status_update: SubsystemStatusDetails = SubsystemStatusDetails(
        subsystem="RSS",
        status="Available with restrictions",
        status_changed_at=original_rss_status_update["status_changed_at"]  # type:ignore
        + timeshift,
        reason="down for testing",
        expected_available_again_at=original_rss_status_update[  # type: ignore
            "expected_available_again_at"
        ]
        + timeshift,
        reporting_user="Ruben Samehu",
    )
    status_repository.update_status(rss_status_update)

    # The RSS update has been recorded, but the other subsystems have not changed.
    status = status_repository.get_status()
    for s in status:
        if s["subsystem"] == "RSS":
            assert s == rss_status_update
        else:
            assert s == _find_subsystem_status(status_updates, s["subsystem"])


def test_status_update_with_missing_subsystem(db_connection: Connection) -> None:
    # A ValueError is raised if the subsystem is missing in a status update.

    status_updates = _default_status_updates()
    salticam_status_update = _find_subsystem_status(status_updates, "Salticam")
    status_repository = StatusRepository(db_connection)

    # subsystem is missing
    del salticam_status_update["subsystem"]  # type: ignore
    salticam_status_update["subsystem"] = None  # type: ignore
    with pytest.raises(ValueError, match="subsystem"):
        status_repository.update_status(salticam_status_update)

    # subsystem is None
    salticam_status_update["subsystem"] = None  # type: ignore
    with pytest.raises(ValueError, match="subsystem"):
        status_repository.update_status(salticam_status_update)

    # subsystem is an empty string
    salticam_status_update["subsystem"] = ""
    with pytest.raises(ValueError, match="subsystem"):
        status_repository.update_status(salticam_status_update)


def test_status_update_with_missing_status(db_connection: Connection) -> None:
    # A ValueError is raised if the status is missing in a status update.

    status_updates = _default_status_updates()
    salticam_status_update = _find_subsystem_status(status_updates, "Salticam")
    status_repository = StatusRepository(db_connection)

    # status is missing
    del salticam_status_update["status"]  # type: ignore
    salticam_status_update["status"] = None  # type: ignore
    with pytest.raises(ValueError, match="status"):
        status_repository.update_status(salticam_status_update)

    # status is None
    salticam_status_update["status"] = None  # type: ignore
    with pytest.raises(ValueError, match="status"):
        status_repository.update_status(salticam_status_update)

    # status is an empty string
    salticam_status_update["status"] = ""
    with pytest.raises(ValueError, match="status"):
        status_repository.update_status(salticam_status_update)


def test_status_update_with_missing_status_changed_at(
    db_connection: Connection,
) -> None:
    # A ValueError is raised if the status has changed and no time of state change is
    # given.

    status_updates = _default_status_updates()
    salticam_status_update = _find_subsystem_status(status_updates, "Salticam")

    # Start with a known state...
    salticam_status_update["status"] = "Unavailable"
    status_repository = StatusRepository(db_connection)
    status_repository.update_status(salticam_status_update)

    # ... and change it
    salticam_status_update["status"] = "Unavailable with restrictions"

    #  state_changed_at is missing
    del salticam_status_update["status_changed_at"]  # type: ignore
    salticam_status_update["status_changed_at"] = None
    with pytest.raises(ValueError, match="status"):
        status_repository.update_status(salticam_status_update)

    # state_changed_at is None
    salticam_status_update["status_changed_at"] = None
    with pytest.raises(ValueError, match="status"):
        status_repository.update_status(salticam_status_update)


def test_status_update_status_changed_at_not_required(
    db_connection: Connection,
) -> None:
    # The time of the status change is not required if the status has not changed.

    status_updates = _default_status_updates()
    salticam_status_update = _find_subsystem_status(status_updates, "Salticam")

    # Start with a known status...
    salticam_status_update["status"] = "Unavailable"
    status_repository = StatusRepository(db_connection)
    status_repository.update_status(salticam_status_update)

    # and keep it
    salticam_status_update["status_changed_at"] = None
    assert True


def test_status_update_status_changed_at_must_be_timezone_aware(
    db_connection: Connection,
) -> None:
    # The time of the status change must be timezone aware.

    status_updates = _default_status_updates()
    salticam_status_update = _find_subsystem_status(status_updates, "Salticam")
    salticam_status_update["status_changed_at"] = datetime(2024, 2, 29, 13, 30, 5, 0)
    status_repository = StatusRepository(db_connection)
    with pytest.raises(ValueError, match="status.*timezone aware"):
        status_repository.update_status(salticam_status_update)


def test_status_update_expected_available_again_at_must_be_timezone_aware(
    db_connection: Connection,
) -> None:
    # The time of the status change must be timezone aware.

    status_updates = _default_status_updates()
    salticam_status_update = _find_subsystem_status(status_updates, "Salticam")
    salticam_status_update["expected_available_again_at"] = datetime(
        2024, 2, 29, 13, 30, 5, 0
    )
    status_repository = StatusRepository(db_connection)
    with pytest.raises(ValueError, match="expected.*timezone aware"):
        status_repository.update_status(salticam_status_update)


@pytest.mark.parametrize(
    "timeshift", [timedelta(seconds=0), timedelta(microseconds=1), timedelta(days=123)]
)
def test_status_update_incorrect_time_order(
    timeshift: timedelta, db_connection: Connection
) -> None:
    # The time when the subsystem become available again must be later than the time
    # when the status changed.

    status_updates = _default_status_updates()
    salticam_status_update = _find_subsystem_status(status_updates, "Salticam")
    salticam_status_update["expected_available_again_at"] = (
        salticam_status_update["status_changed_at"] - timeshift  # type: ignore
    )
    status_repository = StatusRepository(db_connection)
    with pytest.raises(ValueError, match="later"):
        status_repository.update_status(salticam_status_update)


@pytest.mark.parametrize("reason", ["", "a", "Something is broken"])
def test_status_update_no_reason_allowed_if_status_is_available(
    reason: str, db_connection: Connection
) -> None:
    # No reason must be supplied if the subsystem is available.

    status_updates = _default_status_updates()
    salticam_status_update = _find_subsystem_status(status_updates, "Salticam")
    salticam_status_update["status"] = "Available"
    salticam_status_update["reason"] = reason
    salticam_status_update["expected_available_again_at"] = None
    status_repository = StatusRepository(db_connection)
    with pytest.raises(ValueError, match="reason"):
        status_repository.update_status(salticam_status_update)


def test_status_update_no_expected_available_again_allowed_if_status_is_available(
    db_connection: Connection,
) -> None:
    # No expected time for availability again must be supplied if the subsystem is
    # available.

    status_updates = _default_status_updates()
    salticam_status_update = _find_subsystem_status(status_updates, "Salticam")
    salticam_status_update["status"] = "Available"
    salticam_status_update["reason"] = None
    status_repository = StatusRepository(db_connection)
    with pytest.raises(ValueError, match="expected"):
        status_repository.update_status(salticam_status_update)


def test_status_existing_values_are_reused(db_connection: Connection) -> None:
    # If the status does not change and status change time (reason, estimated return to
    # availability), then the current status change time (reason, estimated return to
    # availability) is reused.

    # Update the status
    status_updates = _default_status_updates()
    salticam_status_update = _find_subsystem_status(status_updates, "Salticam")
    salticam_status_update["status"] = "Unavailable"
    status_repository = StatusRepository(db_connection)
    status_repository.update_status(salticam_status_update)

    # Update the status again, but now without status change time, reason and estimated
    # return to availability
    new_salticam_status_update = salticam_status_update.copy()
    new_salticam_status_update["status_changed_at"] = None
    new_salticam_status_update["expected_available_again_at"] = None
    new_salticam_status_update["reason"] = None
    status_repository.update_status(new_salticam_status_update)

    # Get the updated status
    status = status_repository.get_status()
    salticam_status = _find_subsystem_status(status, "Salticam")
    assert (
        salticam_status["status_changed_at"]
        == salticam_status_update["status_changed_at"]
    )
    assert (
        salticam_status["expected_available_again_at"]
        == salticam_status_update["expected_available_again_at"]
    )
    assert salticam_status["reason"] == salticam_status_update["reason"]
