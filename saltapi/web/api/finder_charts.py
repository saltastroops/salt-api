from fastapi import APIRouter, Depends, Path
from fastapi.responses import FileResponse

from saltapi.repository.unit_of_work import UnitOfWork
from saltapi.service.authentication_service import get_current_user
from saltapi.service.user import User as _User
from saltapi.web import services

router = APIRouter(prefix="/finder-charts", tags=["Finding charts"])


@router.get("/{finder_chart_file}", summary="Get a finding chart")
def get_finding_charts(
    finder_chart_file: str = Path(
        ...,
        title="Finder chart file",
        description=(
            "Name of the finder chart file, as a unique identifier and a "
            "suffix, such as 1234.png."
        ),
    ),
    user: _User = Depends(get_current_user),
) -> FileResponse:
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        finding_chart_service = services.finder_chart_service(unit_of_work.connection)

        proposal_code, finder_chart_path = finding_chart_service.get_finder_chart(
            finder_chart_file
        )

        permission_service.check_permission_to_view_proposal(user, proposal_code)

        return FileResponse(finder_chart_path)
