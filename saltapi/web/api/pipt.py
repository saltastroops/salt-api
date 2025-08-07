from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, Query

from saltapi.exceptions import NotFoundError
from saltapi.repository.unit_of_work import UnitOfWork
from saltapi.service.authentication_service import get_current_user
from saltapi.service.user import User
from saltapi.web import services
from saltapi.web.schema.common import ProposalCode, Semester
from saltapi.web.schema.pipt import (
    NirwalsArcDetailsResponse,
    NirwalsFlatDetailsResponse,
    PiptNewsItem,
    PiptProposalInfo,
    PiptUserInfo,
    ProposalConstraint,
    RssArcDetailsResponse,
    SmiArcDetailsResponse,
    SmiFlatDetailsResponse,
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
    response_model=List[ProposalConstraint],
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
) -> List[ProposalConstraint]:
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
    "/nirwals/flat_details",
    summary="Get NIRWALS flat field calibration details",
    response_model=NirwalsFlatDetailsResponse,
)
def get_nirwals_flat_details() -> NirwalsFlatDetailsResponse:
    """
    Returns NIRWALS flat field calibration details.
    """
    with UnitOfWork() as unit_of_work:
        service = services.pipt_service(unit_of_work.connection)
        return service.get_nir_flat_details()


@router.get(
    "/nirwals/arc_details",
    summary="Get NIRWALS arc lamp calibration details",
    response_model=NirwalsArcDetailsResponse,
)
def get_nirwals_arc_details() -> NirwalsArcDetailsResponse:
    """
    Returns NIRWALS arc lamp calibration details.
    """
    with UnitOfWork() as unit_of_work:
        service = services.pipt_service(unit_of_work.connection)
        return service.get_nir_arc_details()


@router.get(
    "/rss/details",
    summary="Get RSS arc calibration details",
    response_model=RssArcDetailsResponse,
)
def get_rss_arc_details() -> RssArcDetailsResponse:
    with UnitOfWork() as unit_of_work:
        service = services.pipt_service(unit_of_work.connection)
        return service.get_rss_arc_details()


@router.get(
    "/rss/ring-details",
    summary="Get RSS ring calibration details",
)
def get_rss_ring_details(version: str = "1") -> Dict[str, list[dict]]:
    with UnitOfWork() as unit_of_work:
        service = services.pipt_service(unit_of_work.connection)
        return service.get_rss_ring_details(version)


@router.get(
    "/smi-flat-details",
    summary="Get SMI flat-field calibration details",
    response_model=SmiFlatDetailsResponse,
)
def get_smi_flat_details() -> SmiFlatDetailsResponse:
    """
    Returns full flat-field calibration details for SMI.
    """
    with UnitOfWork() as unit_of_work:
        service = services.pipt_service(unit_of_work.connection)
        return service.get_smi_flat_details()


@router.get(
    "/smi-arc-details",
    summary="Get SMI arc calibration details",
    response_model=SmiArcDetailsResponse,
)
def get_smi_arc_details() -> SmiArcDetailsResponse:
    """
    Returns full arc calibration details for SMI.
    """
    with UnitOfWork() as unit_of_work:
        service = services.pipt_service(unit_of_work.connection)
        return service.get_smi_arc_details()
