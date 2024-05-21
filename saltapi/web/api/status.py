from typing import List

from fastapi import APIRouter, Request

from saltapi.repository.status_repository import (
    StatusRepository,
    SubsystemStatusDetails,
)
from saltapi.repository.unit_of_work import UnitOfWork
from saltapi.service.status_service import StatusService
from saltapi.web import services
from saltapi.web.schema.status import SubsystemStatus, SubsystemStatusUpdate

router = APIRouter(prefix="", tags=["Status"])


@router.get(
    "/status", summary="Get the SALT status", response_model=List[SubsystemStatus]
)
def get_status() -> List[SubsystemStatusDetails]:
    """
    Returns the SALT status.
    """
    with UnitOfWork() as unit_of_work:
        status_repository = StatusRepository(unit_of_work.connection)
        status_service = StatusService(status_repository)

        return status_service.get_status()


@router.patch(
    "/status", summary="Update the SALT status", response_model=List[SubsystemStatus]
)
def update_status(
    status_update: SubsystemStatusUpdate, request: Request
) -> List[SubsystemStatusDetails]:
    """
    Updates the SALT status for one of the subsystems. The updated status (for all  the
    subsystems) is returned.
    """
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_update_telescope_status(request)

        status_repository = StatusRepository(unit_of_work.connection)
        status_service = StatusService(status_repository)
        status_service.add_status_update(status_update)
        status_service.send_status_update_email(status_update)

        unit_of_work.commit()

        return status_service.get_status()
