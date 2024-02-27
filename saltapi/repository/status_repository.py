from datetime import datetime
from typing import Any, Dict, Literal, Optional

from sqlalchemy import text
from sqlalchemy.engine import Connection


class StatusRepository:
    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def update_status(
        self,
        subsystem: str,
        status: Literal["Available", "Available with restrictions", "Unavailable"],
        status_change_time: Optional[datetime],
        reason: str,
        expected_available_again_at: Optional[datetime],
        reporting_user: str,
    ) -> Dict[str, Any]:
        stmt = text(
            """
INSERT INTO SaltSubsystemStatusUpdate (SaltSubsystem_Id, SaltSubsystemStatus_Id, StatusChangeTime, Reason, ExpectedAvailableAgainAt, ReportingUser)
VALUES (
    (SELECT SaltSubsystem_Id FROM SaltSubsystem WHERE SaltSubsystem = :subsystem),
    (SELECT SaltSubsystemStatus_Id FROM SaltSubsystemStatus WHERE SaltSubsystemStatus = :status),
    :status_change_time,
    :reason,
    :expected_available_again_at,
    :reporting_user
)
        """
        )
        self.connection.execute(
            stmt,
            {
                "subsystem": subsystem,
                "status": status,
                "status_change_time": status_change_time,
                "reason": reason,
                "expected_available_again_at": expected_available_again_at,
                "reporting_user": reporting_user,
            },
        )
