from datetime import datetime
from typing import List, Optional, TypedDict

import pytz
from sqlalchemy import text
from sqlalchemy.engine import Connection

from saltapi.exceptions import ValidationError
from saltapi.util import is_timezone_aware

SubsystemStatusDetails = TypedDict(
    "SubsystemStatusDetails",
    {
        "subsystem": str,
        "status": str,
        "status_changed_at": Optional[datetime],
        "reason": Optional[str],
        "expected_available_again_at": Optional[datetime],
        "reporting_user": str,
    },
)


class StatusRepository:
    ALL_SUBSYSTEMS = [
        "HRS",
        "NIRWALS",
        "RSS",
        "RSS MOS",
        "RSS Polarimetry",
        "RSS Spectroscopy",
        "Salticam",
        "Telescope",
    ]

    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def get_status(self) -> List[SubsystemStatusDetails]:
        """
        Get the current status of the telescope and its subsystems.

        Returns
        -------
        StatusUpdate
            The current status.
        """
        status_updates: List[SubsystemStatusDetails] = []
        for subsystem in StatusRepository.ALL_SUBSYSTEMS:
            status_updates.append(self._get_status_for_subsystem(subsystem))
        return status_updates

    def update_status(self, subsystem_status_update: SubsystemStatusDetails) -> None:
        """
        Update the status of a subsystem.

        Parameters
        ----------
        subsystem_status_update
            Details for the updated status.

        """
        self._validate(subsystem_status_update)

        subsystem_status_update = self._use_current_values(subsystem_status_update)

        stmt = text(
            """
INSERT INTO SaltSubsystemStatusUpdate (SaltSubsystem_Id, SaltSubsystemStatus_Id,
                                       StatusChangedAt, Reason,
                                       ExpectedAvailableAgainAt, ReportingUser)
VALUES ((SELECT SaltSubsystem_Id FROM SaltSubsystem WHERE SaltSubsystem = :subsystem),
        (SELECT SaltSubsystemStatus_Id
         FROM SaltSubsystemStatus
         WHERE SaltSubsystemStatus = :status),
        :status_changed_at,
        :reason,
        :expected_available_again_at,
        :reporting_user)
        """
        )
        self.connection.execute(
            stmt,
            {
                "subsystem": subsystem_status_update["subsystem"],
                "status": subsystem_status_update["status"],
                "status_changed_at": subsystem_status_update["status_changed_at"],
                "reason": subsystem_status_update["reason"],
                "expected_available_again_at": subsystem_status_update[
                    "expected_available_again_at"
                ],
                "reporting_user": subsystem_status_update["reporting_user"],
            },
        )

    def _get_status_for_subsystem(self, subsystem: str) -> SubsystemStatusDetails:
        stmt = text(
            """
SELECT sss.SaltSubsystemStatus       AS status,
       sssu.StatusChangedAt          AS status_changed_at,
       sssu.Reason                   AS reason,
       sssu.ExpectedAvailableAgainAt AS expected_available_again_at,
       sssu.ReportingUser            AS reporting_user
FROM SaltSubsystemStatusUpdate sssu
         JOIN SaltSubsystemStatus sss
              ON sssu.SaltSubsystemStatus_Id = sss.SaltSubsystemStatus_Id
WHERE sssu.SaltSubsystem_Id =
      (SELECT SaltSubsystem_Id FROM SaltSubsystem WHERE SaltSubsystem = :subsystem)
ORDER BY sssu.CreatedAt DESC, sssu.SaltSubsystemStatusUpdate_Id DESC
LIMIT 1
        """
        )

        result = self.connection.execute(stmt, {"subsystem": subsystem})
        row = result.fetchone()
        status_changed_at = (
            pytz.utc.localize(row["status_changed_at"])
            if row["status_changed_at"]
            else None
        )
        expected_available_again_at = (
            pytz.utc.localize(row["expected_available_again_at"])
            if row["expected_available_again_at"]
            else None
        )
        return {
            "subsystem": subsystem,
            "status": row["status"],
            "status_changed_at": status_changed_at,
            "reason": row["reason"],
            "expected_available_again_at": expected_available_again_at,
            "reporting_user": row["reporting_user"],
        }

    def _validate(self, subsystem_status_update: SubsystemStatusDetails) -> None:
        # subsystem is required
        subsystem = subsystem_status_update.get("subsystem")
        if not subsystem:
            raise ValidationError("The subsystem is missing.")

        # status is required
        status = subsystem_status_update.get("status")
        if not status:
            raise ValidationError("The status is missing.")

        # status_changed_at is required if the status has changed
        current_status = self._get_status_for_subsystem(subsystem)["status"]
        if status != current_status and not subsystem_status_update.get(
            "status_changed_at"
        ):
            raise ValidationError(
                "The time when the status has changed is required if the status has changed. "
            )

        # status_changed_at must be timezone aware
        status_changed_at = subsystem_status_update["status_changed_at"]
        if status_changed_at and not is_timezone_aware(status_changed_at):
            raise ValidationError(
                "status_changed_at must be a timezone aware datetime."
            )

        # no expected time of availability is allowed if the subsystem is available
        expected_available_again_at = subsystem_status_update[
            "expected_available_again_at"
        ]
        if status == "Available" and expected_available_again_at is not None:
            raise ValidationError(
                "The expected time of availability again must be None if the subsystem is available."
            )

        # expected_available_again_at must be timezone aware
        if expected_available_again_at and not is_timezone_aware(
            expected_available_again_at
        ):
            raise ValidationError(
                "expected_available_again_at must be a timezone aware datetime"
            )

        # the expected time of availability must be later than the status change
        if (
            expected_available_again_at
            and status_changed_at
            and expected_available_again_at <= status_changed_at
        ):
            raise ValidationError(
                "The time when the subsystem is expected to be available again must be "
                "later then the time when the status changed."
            )

        # no reason is allowed if the subsystem is available
        if status == "Available" and subsystem_status_update["reason"] is not None:
            raise ValidationError(
                "The reason must be None if the subsystem is available"
            )

    def _use_current_values(
        self, subsystem_status: SubsystemStatusDetails
    ) -> SubsystemStatusDetails:
        # Use the current value for the status change time, the expected time of
        # availability again and the reason if they are missing and if the new and
        # current status are the same.

        subsystem = subsystem_status["subsystem"]
        current_status = self.get_status()
        current_subsystem_status = [
            s for s in current_status if s["subsystem"] == subsystem
        ][0]

        updated: SubsystemStatusDetails = SubsystemStatusDetails(**subsystem_status)  # type: ignore

        if current_subsystem_status["status"] != subsystem_status["status"]:
            return updated

        if not updated["status_changed_at"]:
            updated["status_changed_at"] = current_subsystem_status["status_changed_at"]
        if not updated["expected_available_again_at"]:
            updated["expected_available_again_at"] = current_subsystem_status[
                "expected_available_again_at"
            ]
        if not updated["reason"]:
            updated["reason"] = current_subsystem_status["reason"]
        return updated
