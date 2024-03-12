from typing import List

from saltapi.repository.status_repository import (
    StatusRepository,
    SubsystemStatusDetails,
)
from saltapi.web.schema.status import SubsystemStatusUpdate


class StatusService:
    def __init__(self, status_repository: StatusRepository):
        self.status_repository = status_repository

    def get_status(self) -> List[SubsystemStatusDetails]:
        return self.status_repository.get_status()

    def add_status_update(self, subsystem_status_update: SubsystemStatusUpdate) -> None:
        subsystem_status_details: SubsystemStatusDetails = {
            "expected_available_again_at": subsystem_status_update.expected_available_again_at,
            "reason": subsystem_status_update.reason,
            "reporting_user": subsystem_status_update.reporting_user,
            "status": subsystem_status_update.status.value,
            "status_changed_at": subsystem_status_update.status_changed_at,
            "subsystem": subsystem_status_update.subsystem,
        }
        self.status_repository.update_status(subsystem_status_details)
