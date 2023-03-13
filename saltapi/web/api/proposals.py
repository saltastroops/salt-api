from datetime import date
from typing import Dict, List, Optional, Union

from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
    Path,
    Query,
    Response,
    status,
)
from fastapi.responses import FileResponse
from starlette.responses import JSONResponse

from saltapi.exceptions import ValidationError
from saltapi.repository.unit_of_work import UnitOfWork
from saltapi.service.authentication_service import get_current_user
from saltapi.service.proposal import Proposal as _Proposal
from saltapi.service.proposal import ProposalListItem as _ProposalListItem
from saltapi.service.proposal import ProposalStatus as _ProposalStatus
from saltapi.service.user import User
from saltapi.util import semester_start
from saltapi.web import services
from saltapi.web.schema.common import ProposalCode, Semester
from saltapi.web.schema.p1_proposal import P1Proposal
from saltapi.web.schema.p2_proposal import P2Proposal
from saltapi.web.schema.proposal import (
    Comment,
    DataReleaseDate,
    ObservationComment,
    ProposalListItem,
    ProposalStatus,
    ProprietaryPeriodUpdateRequest,
    UpdateStatus,
    ProposalApprovalStatus,
)

router = APIRouter(prefix="/proposals", tags=["Proposals"])


class PDFResponse(Response):
    media_type = "application/pdf"


@router.get("/", summary="List proposals", response_model=List[ProposalListItem])
def get_proposals(
    user: User = Depends(get_current_user),
    from_semester: Semester = Query(
        "2000-1",
        alias="from",
        description="Only include proposals for this semester and later.",
        title="From semester",
    ),
    to_semester: Semester = Query(
        "2099-2",
        alias="to",
        description="Only include proposals for this semester and earlier.",
        title="To semester",
    ),
    limit: int = Query(
        1000, description="Maximum number of results to return.", title="Limit", ge=0
    ),
) -> List[_ProposalListItem]:
    """
    Lists all proposals the user may view. The proposals returned can be limited to
    those with submissions within a semester range by supplying a from or to a
    semester (or both). The maximum number of results can be set with the limit
    parameter; the default is 1000.

    A proposal is included for a semester if there exists a submission for that
    semester. For multi-semester proposals this implies that a proposal may not be
    included for a semester even though time has been requested for that semester.
    """

    with UnitOfWork() as unit_of_work:
        if semester_start(from_semester) > semester_start(to_semester):
            raise HTTPException(
                status_code=400,
                detail="The from semester must not be later than the to semester.",
            )

        proposal_service = services.proposal_service(unit_of_work.connection)
        return proposal_service.list_proposal_summaries(
            username=user.username,
            from_semester=from_semester,
            to_semester=to_semester,
            limit=limit,
        )


@router.get(
    "/{proposal_code}-phase1-summary.pdf",
    summary="Get the latest Phase 1 summary file",
    responses={200: {"content": {"application/pdf": {}}}},
)
def get_phase1_summary(
    proposal_code: ProposalCode = Path(
        ProposalCode,
        title="Proposal code",
        description="Proposal code of the returned Phase 1 proposal summary file.",
    ),
    user: User = Depends(get_current_user),
) -> FileResponse:
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_view_proposal(user, proposal_code)

        proposal_service = services.proposal_service(unit_of_work.connection)
        path = proposal_service.get_phase1_summary(proposal_code)
        filename = f"{proposal_code}-phase1-summary.pdf"
        return FileResponse(
            path,
            media_type="application/pdf",
            headers={"Content-Disposition": f'inline; filename="{filename}"'},
        )


@router.get(
    "/{proposal_code}.zip",
    summary="Get a proposal zip file",
    responses={200: {"content": {"application/zip": {}}}},
)
def get_proposal_zip(
    proposal_code: ProposalCode = Path(
        ProposalCode,
        title="Proposal code",
        description="Proposal code of the returned proposal zip file.",
    ),
    user: User = Depends(get_current_user),
) -> FileResponse:
    """
    Returns the proposal zip file.

    You can import the file into SALT's Principal Investigator Proposal Tool.
    """
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_view_proposal(user, proposal_code)

        proposal_service = services.proposal_service(unit_of_work.connection)
        path = proposal_service.get_proposal_file(proposal_code)
        return FileResponse(
            path, media_type="application/zip", filename=f"{proposal_code}.zip"
        )


@router.get(
    "/{proposal_code}",
    summary="Get a proposal",
    response_model=Union[P1Proposal, P2Proposal],
)
def get_proposal(
    proposal_code: ProposalCode = Path(
        ProposalCode,
        title="Proposal code",
        description="Proposal code of the returned proposal.",
    ),
    user: User = Depends(get_current_user),
) -> _Proposal:
    """
    Returns a JSON representation of the proposal with a given proposal code.

    The JSON representation does not contain the full proposal information. Most
    importantly, while it includes a list of block ids and names, it does not include
    any further block details. You can use the endpoint `/blocks/{id}` to get a JSON
    representation of a specific block.
    """

    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_view_proposal(user, proposal_code)

        proposal_service = services.proposal_service(unit_of_work.connection)
        proposal = proposal_service.get_proposal(proposal_code)
        if proposal["phase"] == 1:
            return P1Proposal(**proposal)
        if proposal["phase"] == 2:
            return P2Proposal(**proposal)


@router.get(
    "/{proposal_code}/scientific-justification",
    summary="Get the scientific justification",
    responses={200: {"content": {"application/pdf": {}}}},
    response_class=PDFResponse,
)
def get_scientific_justification(
    proposal_code: ProposalCode = Path(
        ProposalCode,
        title="Proposal code",
        description=(
            "Proposal code of the proposal whose scientific justification is requested."
        ),
    ),
    submission: Optional[int] = Query(
        None,
        title="Submission",
        description=(
            "Return the latest version of the scientific justification in this "
            "or an earlier submission. By default the latest version of the "
            "scientific justification is returned."
        ),
        ge=1,
    ),
) -> FileResponse:
    """
    Returns the scientific justification for a proposal with a given proposal code. The
    `submission` query parameter lets you choose the submission for which you want to
    request the scientific justification. If no scientific justification exists for this
    version, the latest version prior to this submission is returned.

    There are proposals (such as Director's Discretionary Time proposals) for which no
    scientific justification is submitted. In this case a dummy PDF file is returned.
    """
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.get(
    "/{proposal_code}/status",
    summary="Get the proposal status",
    response_model=ProposalStatus,
)
def get_proposal_status(
    proposal_code: ProposalCode = Path(
        ProposalCode,
        title="Proposal code",
        description="Proposal code of the proposal whose status is requested.",
    ),
    user: User = Depends(get_current_user),
) -> _ProposalStatus:
    """
    Returns the current status of the proposal with a given proposal code.

    The following status values are possible.

    Status | Description
    --- | ---
    Accepted | The proposal has been accepted by the TAC(s), but no Phase 2 submission has been made yet.
    Active | The proposal is in the queue.
    Completed | The proposal has been completed.
    Deleted | The proposal has been deleted.
    Expired | The proposal was submitted in a previous semester and will not be observed any longer.
    In preparation | The proposal submission was preliminary only. This is a legacy status that should not be used any longer.
    Inactive | The proposal currently is not in the queue and will not be observed.
    Rejected | The proposal has been rejected by the TAC(s).
    Superseded | The proposal has been superseded. This is a legacy status that should not be used any longer.
    Under scientific review | The (Phase 1) proposal is being evaluated by the TAC(s).
    Under technical review | The (Phase 2) proposal is being checked by the PI and is not in the queue yet.
    """
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_view_proposal(user, proposal_code)
        proposal_service = services.proposal_service(unit_of_work.connection)

        return proposal_service.get_proposal_status(proposal_code)


@router.put(
    "/{proposal_code}/proprietary-period",
    summary="Request a new proprietary period",
)
def update_proprietary_period(
    proposal_code: ProposalCode = Path(
        ...,
        title="Proposal code",
        description=(
            "Proposal code of the proposal for which a new data release date is"
            " requested."
        ),
    ),
    proprietary_period_update_request: ProprietaryPeriodUpdateRequest = Body(
        ...,
        title="The details for the proprietary period update.",
        description=(
            "The requested proprietary period in months and a motivation. The"
            " motivation is only required if the requested proprietary period is longer"
            " than the maximum proprietary period for the proposal."
        ),
    ),
    user: User = Depends(get_current_user),
) -> JSONResponse:
    """
    Request an update of the propriety period after which the observation data can become public. It depends on the
    requested proprietary period and the proposal whether the request is granted immediately.
    Otherwise, the request needs to be approved based on the requested proprietary period and the submitted motivation.

    The request returns the requested new period and the request status. The latter is "Pending" or "Successful",
    depending on whether the request needs prior approval.
    """
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_update_proprietary_period(
            user, proposal_code
        )
        proposal_service = services.proposal_service(unit_of_work.connection)
        proposal = proposal_service.get_proposal(proposal_code)
        if permission_service.is_motivation_needed_to_update_proprietary_period(
            proposal, proprietary_period_update_request, user.username
        ):
            if not proprietary_period_update_request.motivation:
                raise ValidationError("A motivation is required.")
            proposal_service.create_proprietary_period_extension_request(
                proposal_code=proposal_code,
                proprietary_period=proprietary_period_update_request.proprietary_period,
                motivation=proprietary_period_update_request.motivation,
                username=user.username,
            )
            status_code = status.HTTP_202_ACCEPTED
            update_status = UpdateStatus.PENDING
        else:
            proposal_service.update_proprietary_period(
                proposal_code=proposal_code,
                proprietary_period=proprietary_period_update_request.proprietary_period,
            )
            proposal = proposal_service.get_proposal(proposal_code)
            status_code = status.HTTP_200_OK
            update_status = UpdateStatus.SUCCESSFUL
        unit_of_work.commit()
        return JSONResponse(
            status_code=status_code,
            content={
                **proposal["general_info"]["proprietary_period"],
                "start_date": f"{proposal['general_info']['proprietary_period']['start_date']:%Y-%m-%d}",
                "status": update_status,
            },
        )


@router.put(
    "/{proposal_code}/status",
    summary="Update the proposal status",
    response_model=ProposalStatus,
    status_code=status.HTTP_200_OK,
)
def update_proposal_status(
    proposal_code: ProposalCode = Path(
        ...,
        title="Proposal code",
        description="Proposal code of the proposal whose status is updated.",
    ),
    proposal_status: ProposalStatus = Body(
        ...,
        alias="status",
        title="Proposal status and (optional) status comment",
        description="New proposal status and (optional) status comment.",
    ),
    user: User = Depends(get_current_user),
) -> ProposalStatus:
    """
    Updates the status of the proposal with the given proposal code. See the
    corresponding GET request for a description of the available status values.
    """
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_update_proposal_status(
            user, proposal_code, proposal_status.value
        )
        proposal_service = services.proposal_service(unit_of_work.connection)
        proposal_service.update_proposal_status(
            proposal_code, proposal_status.value, proposal_status.comment
        )

        unit_of_work.commit()
        return ProposalStatus(**proposal_service.get_proposal_status(proposal_code))


@router.get(
    "/{proposal_code}/observation-comments",
    summary="List the observation comments",
    response_model=List[ObservationComment],
)
def get_observation_comments(
    proposal_code: ProposalCode = Path(
        ...,
        title="Proposal code",
        description=(
            "Proposal code of the proposal whose observation comments are requested."
        ),
    ),
    user: User = Depends(get_current_user),
) -> List[ObservationComment]:
    """
    Lists all observation comments for a given proposal code.
    """
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_view_observation_comments(
            user, proposal_code
        )

        proposal_service = services.proposal_service(unit_of_work.connection)
        return [
            ObservationComment(**dict(row))
            for row in proposal_service.get_observation_comments(proposal_code)
        ]


@router.post(
    "/{proposal_code}/observation-comments",
    summary="Create an observation comment",
    response_model=ObservationComment,
    status_code=201,
)
def post_observation_comment(
    proposal_code: ProposalCode = Path(
        ...,
        title="Proposal code",
        description=(
            "Proposal code of the proposal for which an observation comment is added."
        ),
    ),
    comment: Comment = Body(..., title="Comment", description="Text of the comment."),
    user: User = Depends(get_current_user),
) -> ObservationComment:
    """
    Adds a new comment related to an observation. The user submitting the request is
    recorded as the comment author.
    """
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_add_observation_comment(
            user, proposal_code
        )

        proposal_service = services.proposal_service(unit_of_work.connection)
        observation_comment = proposal_service.add_observation_comment(
            proposal_code=proposal_code, comment=comment.comment, user=user
        )
        unit_of_work.commit()
        return ObservationComment(**observation_comment)


@router.get(
    "/{proposal_code}/data-release-date",
    summary="Get the data release date",
    response_model=DataReleaseDate,
)
def get_data_release_date(
    proposal_code: ProposalCode = Path(
        ...,
        title="Proposal code",
        description=(
            "Proposal code of the proposal whose data release date is requested."
        ),
    ),
    from_date: Optional[date] = Query(
        date(2000, 1, 1),
        alias="from",
        title="From date",
        description="Only include observations for this night and later.",
    ),
    to_date: Optional[date] = Query(
        date(2099, 12, 31),
        alias="to",
        title="From date",
        description="Only include observations for this night and earlier.",
    ),
) -> date:
    """
    Returns the date when the observation data for the proposal is scheduled to become
    public.
    """
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.put(
    "/{proposal_code}/self-activation",
    summary="Change the status whether the proposal may be activated by the Principal Investigator and Principal Contact",
    response_model=SelfActivation
)
def put_is_self_activatable(
        proposal_code: ProposalCode = Path(
            ...,
            title="Proposal code",
            description=(
                    "Proposal code of the proposal for which an observation comment is added."
            ),
        ),
        self_activation: SelfActivation = Body(
            ...,
            title="Allowed to self-activate",
            description=(
                    "is the Principal Investigator or Principal Contact allowed to activate the proposal."
            )
        ),
        user: User = Depends(get_current_user),
) -> SelfActivation:
    """
    Change the self-activation status of the proposal.

    A proposal is self-activatable if the Principal Investigator or Principal Contact are allowed to activate it.
    """
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_change_self_activatable(user)

        proposal_service = services.proposal_service(unit_of_work.connection)
        proposal_service.update_is_self_activatable(
            proposal_code=proposal_code, is_self_activatable=self_activation.allowed
        )
        unit_of_work.commit()
        return SelfActivation(
            allowed = proposal_service.is_self_activatable(proposal_code)
        )

@router.put(
    "/{proposal_code}/liaison-astronomer",
    summary="Set the liaison astronomer for the proposal",
    response_model=Optional[LiaisonAstronomer],
    status_code=200,
)
def update_liaison_astronomer(
        proposal_code: ProposalCode = Path(
            ...,
            title="Proposal code",
            description=(
                    "Proposal code of the proposal for which the liaison astronomer is updated."
            ),
        ),
        liaison_astronomer_id: Optional[UserId] = Body(
            ...,
            title="Liaison astronomer id",
            description="The user id of the liaison astronomer."
        ),
        user: User = Depends(get_current_user),
) -> Optional[LiaisonAstronomer]:
    """
    Update the liaison astronomer of the proposal.
    """
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_update_liaison_astronomer(user)

        proposal_service = services.proposal_service(unit_of_work.connection)
        proposal_service.update_liaison_astronomer(
            proposal_code=proposal_code, liaison_astronomer_id=liaison_astronomer_id.id
        )
        unit_of_work.commit()
        liaison_salt_astronomer = proposal_service.get_liaison_astronomer(proposal_code)
        if liaison_salt_astronomer:
            return LiaisonAstronomer(**liaison_salt_astronomer)
        return None


@router.put(
    "/{proposal_code}/approvals/{approval_user_id}",
    summary="Update the proposal status",
    status_code=status.HTTP_200_OK,
)
def update_investigator_proposal_approval_status(
    proposal_code: ProposalCode = Path(
        ...,
        title="Proposal code",
        description=(
            "Proposal code of the proposal for which an investigator approval status is"
            " updated."
        ),
    ),
    approval_user_id: int = Path(
        ...,
        title="User id",
        description="Id of the user",
    ),
    approval_status: ProposalApprovalStatus = Body(
        ...,
        alias="status",
        title="Proposal approval status",
        description="Proposal approval status.",
    ),
    user: User = Depends(get_current_user),
) -> None:
    """
    Updates an investigator's approval status of the proposal.
    """
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        user_service = services.user_service(unit_of_work.connection)

        permission_service.check_permission_to_update_investigator_proposal_approval_status(
            user, approval_user_id, proposal_code
        )

        user_details = (
            user
            if user.id == approval_user_id
            else user_service.get_user(approval_user_id)
        )

        proposal_service = services.proposal_service(unit_of_work.connection)
        proposal_service.update_investigator_proposal_approval_status(
            user_details.id, proposal_code, approval_status.approved
        )

        unit_of_work.commit()
