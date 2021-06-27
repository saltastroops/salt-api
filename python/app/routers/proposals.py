from typing import List, Optional

from fastapi import (
    APIRouter,
    Body,
    Depends,
    File,
    Header,
    Path,
    Query,
    Response,
    UploadFile,
    status,
)
from fastapi.responses import FileResponse

from app.dependencies import get_current_user
from app.models.general import User
from app.models.proposal import (
    ProposalCode,
    ProposalContent,
    ProposalContentType,
    ProposalListItem,
    ProposalStatusContent,
    SemesterString,
    SubmissionAcknowledgment,
)

router = APIRouter(prefix="/proposals", tags=["Proposals"])


class PDFResponse(Response):
    media_type = "application/pdf"


@router.get("/", summary="List proposals", response_model=ProposalListItem)
def get_proposals(
    from_semester: Optional[SemesterString] = Query(
        "2005-2",
        alias="from",
        description="Only include proposals for this semester and later.",
    ),
    to_semester: Optional[SemesterString] = Query(
        "2099-2",
        alias="to",
        description="Only include proposals for this semester and earlier.",
        title="To semester",
    ),
    user: User = Depends(get_current_user),
) -> List[ProposalListItem]:
    """
    Lists all proposals the user may view. The proposals returned can be limited to those
    with submissions within a semester range by supplying a from or a to semester (or
    both).
    """

    raise NotImplementedError()


@router.get(
    "/proposals/{proposal_code}",
    summary="Get a proposal",
    response_model=ProposalContent,
    responses={200: {"content": {"application/pdf": {}, "application/zip": {}}}},
)
def get_proposal(
    proposal_code: ProposalCode = Path(
        ProposalCode,
        title="Proposal code",
        description="Proposal code of the returned proposal.",
    ),
    submission: Optional[int] = Query(
        None,
        title="Submission",
        description="Return the proposal version for a specific submission. By default "
        "the latest version is returned.",
        ge=1,
    ),
    accept: Optional[ProposalContentType] = Header(
        ProposalContentType.JSON,
        title="Accepted content type",
        description="Content type that should be returned.",
    ),
) -> ProposalContent:
    """
    Returns the proposal with a given proposal code. The proposal can be requested in
    either of three formats:

    1. As a JSON string. This the default.
    2. As a zip file, which can be imported into the PIPT.
    3. As a PDF file. This is only available for Phase 1 proposals.

    You can choose the format by supplying its content type in the `Accept` HTTP header:

    Returned object | `Accept` HTTP header value
    --- | ---
    JSON string | application/json
    zip file | application/zip
    pdf file | application/pdf

    A JSON string is returned if no `Accept` header is included in the request. In the
    case of the zip and the pdf file the response contains an `Content-Disposition` HTTP
    header with an appropriate filename (with the proposal code and the correct file
    extension).

    An error with status code 406 (Not Acceptable) is returned if an unsupported value
    is given in the `Accept` header.

    The `submission` query parameter lets you request a specific version of the
    proposal. By default the latest submission is returned.

    The different formats do not contain the same information. Most importantly, while
    JSON string includes a list of block ids and names, it does not include any further
    block details. You can use the endpoint `/blocks/{id}` to get a JSON representation
    of a specific block.
    """
    raise NotImplementedError()


@router.post(
    "/proposals",
    summary="Submit a new proposal",
    response_model=SubmissionAcknowledgment,
    status_code=status.HTTP_202_ACCEPTED,
)
def submit_new_proposal(
    proposal: UploadFile = File(
        ...,
        title="Proposal file",
        description="Zip file containing the whole proposal content, including all "
        "required file attachments.",
    )
) -> SubmissionAcknowledgment:
    """
    Submits a new proposal. The proposal must be submitted as a zip file containing the
    proposal as well as any attachments such as the scientific justification and finder
    charts. You can generate such a file by exporting a proposal as zip file from the
    SALT's Principal Investigator Proposal Tool (PIPT).

    The request does not wait for the submission to finish. Instead it returns an
    acknowledgment with a submission id, which you can use to track the submission (by
    calling the `/submissions/{submission_id}` endpoint).

    You can only use this endpoint to submit a new proposal. If you try to resubmit an
    existing proposal, the request fails with an error. Use the endpoint
    `/proposals/{proposal_code}` for resubmissions.
    """
    raise NotImplementedError()


@router.patch(
    "/proposals/{proposal_code}",
    summary="Resubmit a proposal",
    response_model=SubmissionAcknowledgment,
    status_code=status.HTTP_202_ACCEPTED,
)
def resubmit_proposal(
    proposal_code: ProposalCode = Path(
        ...,
        title="Proposal code",
        description="Proposal code of the resubmitted proposal.",
    ),
    proposal: UploadFile = File(
        ...,
        title="Proposal file",
        description="File containing the whole proposal content, including all "
        "required file attachments.",
    ),
) -> SubmissionAcknowledgment:
    """
    Resubmits an existing proposal. The proposal must be submitted as a file in either
    of the following forms.

    * As zip file containing the whole proposal, including all required file attachments
    such as the scientific justification and finder charts. In this case the whole
    proposal is replaced.
    * As a zip file containing one or multiple blocks, including all required file
    attachments such as finder charts. In this case the submitted blocks will be added
    (if they don't exist yet), or they will replace their existing version (if they
    exist already). All blocks not contained in the file (and all the other proposal
    content) will remain unchanged.
    * As an XML file containing one or multiple blocks. In this case the submitted
    blocks will be added (if they don't exist yet), or they will replace their existing
    version (if they exist already). All blocks not contained in the file (and all the
    other proposal content) will remain unchanged. The blocks in the submitted file must
    not reference any other files. In practical terms this means that all finder charts
    must be auto-generated on the server and that there may be no MOS masks. Submit a
    zip file if these conditions aren't met for your resubmission.

    If you resubmit a whole proposal (rather than just blocks), the proposal must
    contain the same proposal code as the one specified as path parameter. Otherwise
    the request will fail with an error.

    The request does not wait for the submission to finish. Instead it returns an
    acknowledgment with a submission id, which you can use to track the submission (
    by calling the `/submissions/{submission_id}` endpoint).
    """
    raise NotImplementedError()


@router.get(
    "/proposal/{proposal_code}/scientific-justification",
    summary="Get the scientific justification",
    responses={200: {"content": {"application/pdf": {}}}},
    response_class=PDFResponse,
)
def get_scientific_justification(
    proposal_code: ProposalCode = Path(
        ProposalCode,
        title="Proposal code",
        description="Proposal code of the proposal whose scientific justification is "
        "requested.",
    ),
    submission: Optional[int] = Query(
        None,
        title="Submission",
        description="Return the latest version of the scientific justification in this "
        "or an earlier submission. By default the latest version of the "
        "scientific justification is returned.",
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
    raise NotImplementedError()


@router.get(
    "/proposals/{proposal_code}/status",
    summary="Get the proposal status",
    response_model=ProposalStatusContent,
)
def get_proposal_status(
    proposal_code: ProposalCode = Path(
        ProposalCode,
        title="Proposal code",
        description="Proposal code of the proposal whose status is requested.",
    )
) -> ProposalStatusContent:
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
    raise NotImplementedError()


@router.put(
    "/proposals/{proposal_code}/status",
    summary="Update the proposal status",
    status_code=status.HTTP_204_NO_CONTENT,
)
def update_proposal_status(
    proposal_code: ProposalCode = Path(
        ...,
        title="Proposal code",
        description="Proposal code of the proposal whose status is requested.",
    ),
    status: ProposalStatusContent = Body(
        ..., title="Proposal status", description="New proposal status."
    ),
) -> None:
    """
    Updates the status of the proposal with the given proposal code. See the
    corresponding GET request for a description of the available status values.
    """
    raise NotImplementedError()
