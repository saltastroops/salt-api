from datetime import datetime, timedelta
from typing import Literal, Optional

from sqlalchemy.engine import Connection

from saltapi.repository.status_repository import StatusRepository


def _status_details(
    subsystem: str = "Telescope",
    status: Literal[
        "Available", "Available with restrictions", "Unavailable"
    ] = "Available",
    status_change_time: datetime = None,  # noqa
    reason: str = None,
    expected_available_again_at: Optional[datetime] = None,
    reporting_user: str = "John Doe",
):
    return {
        "subsystem": subsystem,
        "status": status,
        "status_change_time": status_change_time,
        "reason": reason,
        "expected_available_again_at": expected_available_again_at,
        "reporting_user": reporting_user,
    }


def test_add_status_update(db_connection: Connection) -> None:
    status_repository = StatusRepository(db_connection)
    status_repository.update_status(**_status_details())
