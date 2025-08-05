from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, Path, Query

from saltapi.exceptions import NotFoundError
from saltapi.repository.unit_of_work import UnitOfWork
from saltapi.service.authentication_service import get_current_user
from saltapi.service.user import User
from saltapi.web import services
from saltapi.web.schema.common import ProposalCode, Semester
from saltapi.web.schema.pipt import (
    PiptNewsItem,
    PiptProposalInfo,
    PiptUserInfo,
    ProposalConstraint,
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
    user: User = Depends(get_current_user),
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
    summary="Get NIRWALS flat calibration details",
    response_model=dict,
)
def get_nirwals_flat_details(
    only_checksum: bool = Query(False, description="If true, only return the checksum")
) -> dict:
    """
    Returns NIRWALS flat calibration details or just the checksum.
    """
    with UnitOfWork() as unit_of_work:
        service = services.pipt_service(unit_of_work.connection)
        return service.get_nir_flat_details(only_checksum=only_checksum)


@router.get(
    "/nirwals/arc_details",
    summary="Get NIRWALS arc lamp calibration details",
    response_model=dict,
)
def get_nirwals_arc_details(
    only_checksum: bool = Query(False, description="If true, only return the checksum.")
) -> dict:
    """
    Returns NIRWALS arc lamp calibration details or just the checksum.
    """
    with UnitOfWork() as unit_of_work:
        service = services.pipt_service(unit_of_work.connection)
        return service.get_nir_arc_details(only_checksum=only_checksum)
