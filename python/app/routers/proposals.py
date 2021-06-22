from typing import List, Optional

from fastapi import APIRouter, Depends, Query

from app.dependencies import get_current_user
from app.models.general import User
from app.models.proposal import ProposalListItem, SemesterString

router = APIRouter(prefix="/proposals", tags=["Proposals"])


@router.get(
    "/",
    summary="List proposals",
    responses={
        200: {
            "model": ProposalListItem,
            "example": {"proposal_code": "2021-1-SCI-067"},
        },
    },
)
def get_proposals(
    from_semester: Optional[SemesterString] = Query(
        "2005-2",
        alias="from",
        description="The first semester for which proposals are included.",
    ),
    to_semester: Optional[SemesterString] = Query(
        "2099-2",
        alias="to",
        description="The last semester for which proposals are included.",
        title="To semester",
    ),
    user: User = Depends(get_current_user),
) -> List[ProposalListItem]:
    """
    List all proposals the user may view. The proposals returned can be limited to those
    with submissions within a semester range by supplying a from or a to semester (or
    both).
    """

    raise NotImplementedError()
