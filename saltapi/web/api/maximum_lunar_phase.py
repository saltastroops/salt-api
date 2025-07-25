from fastapi import APIRouter, Depends, Path

from saltapi.repository.unit_of_work import UnitOfWork
from saltapi.service.authentication_service import get_current_user
from saltapi.service.user import User
from saltapi.web import services
from saltapi.web.schema.common import ProposalCode
from saltapi.web.schema.lunar_phase import LunarPhaseList

router = APIRouter(prefix="/maximum-lunar-phases", tags=["Lunar Phase"])


@router.get(
    "/{proposal_code}",
    summary="Get maximum lunar phases for all targets in the proposal",
    response_model=LunarPhaseList,
)
def get_maximum_lunar_phases(
    proposal_code: ProposalCode = Path(
        ...,
        title="Proposal code",
        description="Proposal code for which to retrieve maximum lunar phases.",
    ),
    user: User = Depends(get_current_user),
) -> LunarPhaseList:
    """
    Returns the maximum lunar phases for all targets in the given proposal.
    """
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_view_proposal(user, proposal_code)
        lunar_phase_service = services.maximum_lunar_phase_service(
            unit_of_work.connection
        )
        result = lunar_phase_service.get_maximum_lunar_phases(proposal_code)
        return LunarPhaseList(proposal_code=proposal_code, phases=result["phases"])
