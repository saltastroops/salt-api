from typing import Any, Dict, List, Literal, Optional

from fastapi import APIRouter, Depends, Query

from saltapi.exceptions import AuthorizationError, NotFoundError
from saltapi.repository.unit_of_work import UnitOfWork
from saltapi.service.authentication_service import get_current_user
from saltapi.service.user import User
from saltapi.web import services
from saltapi.web.schema.common import ProposalCode, Semester
from saltapi.web.schema.pipt import (
    NirwalsArcDetailsSetup,
    NirwalsFlatDetailsSetup,
    PiptBlockVisit,
    PiptNewsItem,
    PiptPartner,
    PiptProposal,
    PiptProposalInfo,
    PiptTimeAllocation,
    PiptUserInfo,
    PreviousProposalListItem,
    RssArcDetailsSetup,
    RssRingDetailsSetup,
    SmiArcDetailsSetup,
    SmiFlatDetailsSetup,
)

router = APIRouter(prefix="/pipt", tags=["PIPT"])


@router.get(
    "/news",
    summary="Get the PIPT news entries from the last N days",
    response_model=List[PiptNewsItem],
)
def get_pipt_news(
    days: int = Query(30, ge=1, description="Number of days to look back")
) -> List[Dict[str, Any]]:
    with UnitOfWork() as unit_of_work:
        service = services.pipt_service(unit_of_work.connection)
        return service.get_pipt_news_for_days(days)


@router.get(
    "/user",
    summary="Get basic user info by email",
    response_model=PiptUserInfo,
)
def get_basic_user_info_by_email(
    email: str = Query(..., title="Email", description="User email address"),
) -> PiptUserInfo:
    with UnitOfWork() as unit_of_work:
        user_service = services.user_service(unit_of_work.connection)
        pipt_user = user_service.get_user_by_email(email)

        if pipt_user is None:
            raise NotFoundError("Unknown user.")

        matching_affiliation = [
            affiliation
            for affiliation in pipt_user.affiliations
            if "contact" in affiliation and affiliation["contact"] == email
        ]

        return PiptUserInfo(
            given_name=pipt_user.given_name,
            family_name=pipt_user.family_name,
            email=pipt_user.email,
            affiliation=matching_affiliation[0],
        )


@router.get(
    "/proposal-info",
    summary="Get proposal info for PIPT",
    response_model=PiptProposalInfo,
)
def get_pipt_proposal_info(
    proposal_code: ProposalCode = Query(
        ...,
        title="Proposal code",
        description="Proposal code of the returned proposal.",
    ),
    semester: Optional[Semester] = Query(
        None,
        description="Semester of the returned proposal.",
        title="Semester",
    ),
    phase: Optional[int] = Query(
        None,
        description="Phase of the returned proposal.",
        title="Phase",
    ),
    user: User = Depends(get_current_user),
) -> PiptProposalInfo:
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_view_proposal(user, proposal_code)

        proposal_service = services.proposal_service(unit_of_work.connection)
        proposal = proposal_service.get_proposal(proposal_code, semester, phase)

        return PiptProposalInfo(
            proposal_code=proposal["proposal_code"],
            title=proposal["general_info"]["title"],
            phase=proposal["phase"],
            status=proposal["general_info"]["status"],
            proposal_file=proposal["proposal_file"],
            time_allocations=proposal["time_allocations"],
        )


@router.get(
    "/proposal-constraints",
    summary="Get proposal constraints",
    response_model=List[PiptTimeAllocation],
)
def get_constraints(
    proposal_code: ProposalCode = Query(
        ...,
        title="Proposal code",
        description="Proposal code of the returned constraints.",
    ),
    year: Optional[int] = Query(None, description="Optional year"),
    semester: Optional[int] = Query(None, description="Optional semester"),
    user: User = Depends(get_current_user),
) -> List[PiptTimeAllocation]:
    """
    Returns proposal constraints for a given proposal code.
    Optional filters include year and semester.
    """
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_view_proposal(user, proposal_code)
        pipt_service = services.pipt_service(unit_of_work.connection)

        return pipt_service.get_proposal_constraints(proposal_code, year, semester)


@router.get(
    "/nirwals/flat-details",
    summary="Get NIRWALS flat field calibration details",
    response_model=NirwalsFlatDetailsSetup,
)
def get_nirwals_flat_details() -> NirwalsFlatDetailsSetup:
    """
    Returns NIRWALS flat field calibration details.
    """
    with UnitOfWork() as unit_of_work:
        service = services.pipt_service(unit_of_work.connection)
        return service.get_nir_flat_details()


@router.get(
    "/nirwals/arc-details",
    summary="Get NIRWALS arc lamp calibration details",
    response_model=NirwalsArcDetailsSetup,
)
def get_nirwals_arc_details() -> NirwalsArcDetailsSetup:
    """
    Return the arc calibration details for NIRWALS setups.
    """
    with UnitOfWork() as unit_of_work:
        service = services.pipt_service(unit_of_work.connection)
        return service.get_nir_arc_details()


@router.get(
    "/rss/arc-details",
    summary="Get RSS arc calibration details",
    response_model=RssArcDetailsSetup,
)
def get_rss_arc_details() -> RssArcDetailsSetup:
    """
    Get the arc calibration details for non-SMI RSS setups.
    """
    with UnitOfWork() as unit_of_work:
        service = services.pipt_service(unit_of_work.connection)
        return service.get_rss_arc_details()


@router.get(
    "/rss/ring-details",
    summary="Get RSS ring calibration details",
    response_model=RssRingDetailsSetup,
)
def get_rss_ring_details() -> RssRingDetailsSetup:
    with UnitOfWork() as unit_of_work:
        """Get calibration regions and plus lines for non-SMI RSS setups."""
        service = services.pipt_service(unit_of_work.connection)
        return service.get_rss_ring_details()


@router.get(
    "/rss/smi-flat-details",
    summary="Get SMI flat field calibration details",
    response_model=SmiFlatDetailsSetup,
)
def get_smi_flat_details() -> SmiFlatDetailsSetup:
    """
    Get the flat-field calibration details for non-SMI RSS setups.
    """
    with UnitOfWork() as unit_of_work:
        service = services.pipt_service(unit_of_work.connection)
        return service.get_smi_flat_details()


@router.get(
    "/rss/smi-arc-details",
    summary="Get SMI arc calibration details",
    response_model=SmiArcDetailsSetup,
)
def get_smi_arc_details() -> SmiArcDetailsSetup:
    """
    Get the arc calibration details for SMI RSS setups.
    """
    with UnitOfWork() as unit_of_work:
        service = services.pipt_service(unit_of_work.connection)
        return service.get_smi_arc_details()


@router.get(
    "/previous-proposals",
    summary="Get previous proposals for a user",
    response_model=List[PreviousProposalListItem],
)
def get_previous_proposals_info(
    user: User = Depends(get_current_user),
    from_semester: Optional[str] = Query(
        None,
        description="Semester from which onwards to include proposals, e.g., '2023-2'",
    ),
) -> List[PreviousProposalListItem]:
    """
    Return previous proposals for the given user, starting from the specified year and semester.
    If from_year and from_semester are not provided, defaults to 3 semesters ago.
    """
    with UnitOfWork() as unit_of_work:
        service = services.pipt_service(unit_of_work.connection)
        proposals = service.get_previous_proposals_info(
            user_id=user.id,
            from_semester=from_semester,
        )

    return proposals


@router.get(
    "/block-visits",
    summary="Get block visits for a given proposal code",
    response_model=List[PiptBlockVisit],
)
def get_block_visits(
    proposal_code: ProposalCode = Query(
        ...,
        title="Proposal code",
        description="Proposal code of the returned constraints.",
    ),
    user: User = Depends(get_current_user),
) -> List[PiptBlockVisit]:
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_view_proposal(user, proposal_code)

        service = services.pipt_service(unit_of_work.connection)
        block_visits = service.get_block_visits(proposal_code)
        return block_visits


@router.get(
    "/proposals",
    summary="Get proposals",
    response_model=List[PiptProposal],
)
def get_pipt_proposals(
    phase: Literal[1, 2] = Query(..., description="Proposal phase"),
    limit: Optional[int] = Query(None, description="Max number of proposals"),
    descending: bool = Query(True, description="Sort in descending order"),
    user: User = Depends(get_current_user),
):
    with UnitOfWork() as unit_of_work:
        pipt_service = services.pipt_service(unit_of_work.connection)
        proposals = pipt_service.get_proposals(
            phase=phase, limit=limit, descending=descending, user=user
        )

        return proposals


@router.get("/partners", summary="Get partners", response_model=List[PiptPartner])
def get_partners(
    user: User = Depends(get_current_user),
):
    """
        Get the partner details.

        For every partner the name and the list of institutes are included. The list is
        sorted by partner name, and for each partner the institutes are sorted by
        institute name and department.
    ="""
    with UnitOfWork() as unit_of_work:
        pipt_service = services.pipt_service(unit_of_work.connection)
        return pipt_service.get_partners()
