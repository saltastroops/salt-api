import mimetypes
import os
import tempfile
from datetime import date
from typing import Any, Dict, List, Optional, Union

from fastapi import (
    APIRouter,
    Body,
    Depends,
    Form,
    HTTPException,
    Path,
    Query,
    Response,
    status,
)
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse

from saltapi.exceptions import NotFoundError, SSDAError, ValidationError
from saltapi.repository.unit_of_work import UnitOfWork
from saltapi.service.authentication_service import get_current_user
from saltapi.service.proposal import Proposal as _Proposal
from saltapi.service.proposal import ProposalListItem as _ProposalListItem
from saltapi.service.proposal import ProposalStatus as _ProposalStatus
from saltapi.service.user import LiaisonAstronomer, User
from saltapi.util import semester_start, remove_file
from saltapi.web import services
from saltapi.web.schema.common import Message, ProposalCode, Semester
from saltapi.web.schema.p1_proposal import P1Proposal
from saltapi.web.schema.p2_proposal import P2Proposal
from saltapi.web.schema.pool import Pool
from saltapi.web.schema.proposal import (
    Comment,
    DataReleaseDate,
    DataRequest,
    ObservationComment,
    ProposalApprovalStatus,
    ProposalListItem,
    ProposalStatus,
    ProprietaryPeriodUpdateRequest,
    SelfActivation,
    UpdateStatus,
)
from saltapi.web.schema.user import UserId

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
    phase: Optional[int] = Query(
        None, title="Phase", description="Phase of the returned proposal zip file"
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
        path = proposal_service.get_proposal_file(proposal_code, phase)
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
) -> _Proposal:
    """
    Returns a JSON representation of the proposal with a given proposal code, semester and phase.
    The default values are those chosen during the latest submission.

    The JSON representation does not contain the full proposal information. Most
    importantly, while it includes a list of block ids and names, it does not include
    any further block details. You can use the endpoint `/blocks/{id}` to get a JSON
    representation of a specific block.
    """

    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_view_proposal(user, proposal_code)

        proposal_service = services.proposal_service(unit_of_work.connection)
        proposal = proposal_service.get_proposal(proposal_code, semester, phase)
        if proposal["phase"] == 1:
            return P1Proposal(**proposal)
        if proposal["phase"] == 2:
            return P2Proposal(**proposal)


@router.get(
    "/{proposal_code}/pools",
    summary="Get the pools in a proposal",
    response_model=List[Pool],
)
def get_pools(
    proposal_code: ProposalCode = Path(
        ...,
        title="Proposal code",
        description="Proposal code of the proposal whose pools are requested.",
    ),
    semester: Optional[Semester] = Query(
        None,
        description="Semester of the returned pools.",
        title="Semester",
    ),
    user: User = Depends(get_current_user),
) -> List[Pool]:
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_view_proposal(user, proposal_code)
        proposal_service = services.proposal_service(unit_of_work.connection)
        pools = proposal_service.get_pools(proposal_code, semester)
        return [Pool(**pool) for pool in pools]


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
            unit_of_work.commit()
        else:
            proposal_service.update_proprietary_period(
                proposal_code=proposal_code,
                proprietary_period=proprietary_period_update_request.proprietary_period,
            )
            proposal = proposal_service.get_proposal(proposal_code)
            status_code = status.HTTP_200_OK
            update_status = UpdateStatus.SUCCESSFUL
            try:
                proposal_service.update_proprietary_period_in_ssda(
                    proposal_code=proposal_code,
                    proprietary_period=proprietary_period_update_request.proprietary_period,
                )
                unit_of_work.commit()
            except SSDAError:
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return JSONResponse(
            status_code=status_code,
            content={
                **proposal["general_info"]["proprietary_period"],
                "start_date": f"{proposal['general_info']['proprietary_period']['start_date']:%Y-%m-%d}",
                "status": update_status,
                "status_code": status_code,
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
) -> Dict[str, Any]:
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
        return proposal_service.get_proposal_status(proposal_code)


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
) -> List[Dict[str, Any]]:
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
            dict(row)
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
) -> Dict[str, Any]:
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
        return observation_comment


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
    summary=(
        "Change the status whether the proposal may be activated by the Principal"
        " Investigator and Principal Contact"
    ),
    response_model=SelfActivation,
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
            "is the Principal Investigator or Principal Contact allowed to activate the"
            " proposal."
        ),
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
            allowed=proposal_service.is_self_activatable(proposal_code)
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
    liaison_astronomer_id: UserId = Body(
        ...,
        title="Liaison astronomer id",
        description="The user id of the liaison astronomer.",
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


@router.post(
    "/{proposal_code}/request-data",
    summary="Request data for observations.",
    response_model=Optional[Message],
    status_code=200,
)
def request_data(
    proposal_code: ProposalCode = Path(
        ...,
        title="Proposal code",
        description="Proposal code of the proposal which the block visits belong to.",
    ),
    data_request: DataRequest = Body(
        ...,
        title="Data request",
        description="The data request.",
    ),
    user: User = Depends(get_current_user),
) -> Message:
    """
    Create an observation data request.
    """
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_request_data(
            user, proposal_code, data_request.observation_ids
        )
        data_service = services.data_service(unit_of_work.connection)
        data_service.request_data(
            user_id=user.id,
            proposal_code=proposal_code,
            block_visit_ids=data_request.observation_ids,
            data_formats=[
                str(data_format.value) for data_format in data_request.data_formats
            ],
        )
        unit_of_work.commit()

        return Message(message="Successful")


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

        if user.id == approval_user_id:
            user_details = user
        else:
            user_details = user_service.get_user(approval_user_id)
            if user_details is None:
                raise NotFoundError("Unknown user.")

        proposal_service = services.proposal_service(unit_of_work.connection)
        proposal_service.update_investigator_proposal_approval_status(
            user_details.id, proposal_code, approval_status.approved
        )

        unit_of_work.commit()


@router.get(
    "/{proposal_code}/attachments/{filename}",
    summary="Download the attached files of a proposal",
)
async def serve_attachment(
    proposal_code: str = Path(
        ...,
        title="Proposal code",
        description="The proposal code",
    ),
    filename: str = Path(
        ...,
        title="Filename",
        description="Name of the file to download.",
    ),
    user: User = Depends(get_current_user),
) -> FileResponse:
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_view_proposal(user, proposal_code)

        proposal_services = services.ProposalService(unit_of_work.connection)
        file_path = (
            proposal_services.get_proposal_attachments_dir(proposal_code) / filename
        )

        # Check if the file exists
        if not os.path.isfile(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        media_type, _ = mimetypes.guess_type(filename)

        if not media_type:
            raise HTTPException(status_code=400, detail="Unsupported file format")

        # Serve the file
        return FileResponse(file_path, media_type=media_type)


@router.post(
    "/{proposal_code}/slitmasks/{barcode}/gcode",
    summary="Generate GCode for a slit mask",
)
async def generate_slitmask_gcode(
    proposal_code: str = Path(
        ...,
        title="Proposal code",
        description="The proposal code",
    ),
    barcode: str = Path(..., title="Barcode", description="Slitmask barcode"),
    using_boxes_for_refstars: bool = Form(
        True,
        title="Cut boxes for reference stars",
        description="Whether to cut boxes for reference stars",
    ),
    refstar_boxsize: int = Form(
        5, title="Reference star box size", description="Size of reference star boxes"
    ),
    slow_cutting_power: float = Form(
        19.1,
        title="Slow cutting power",
        description="Cutting power for laser cutter in slow mode",
    ),
    user: User = Depends(get_current_user),
):
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_view_proposal(user, proposal_code)
        proposal_service = services.ProposalService(unit_of_work.connection)
        instrument_service = services.instrument_service(unit_of_work.connection)
        filename = instrument_service.get_rss_mask_filename(barcode)
        xml_file = (
            proposal_service.get_proposal_attachments_dir(proposal_code) / filename
        )

        if not xml_file.exists():
            raise HTTPException(
                status_code=404, detail=f"Slit mask XML not found: {filename}"
            )

        tmp_file = tempfile.mktemp(suffix=".nc")

        instrument_service.generate_slitmask_gcode(
            barcode=barcode,
            xml_file=xml_file,
            tmp_file=tmp_file,
            using_boxes_for_refstars=using_boxes_for_refstars,
            refstar_boxsize=refstar_boxsize,
            slow_cutting_power=slow_cutting_power,
        )

        return FileResponse(
            tmp_file,
            filename=f"{barcode}.nc",
            media_type="text/plain",
            background=BackgroundTask(remove_file, tmp_file),
        )
