import pathlib
import urllib.parse
from typing import Dict, Optional, cast

from fastapi import (
    APIRouter,
    Body,
    Depends,
    File,
    HTTPException,
    Path,
    Request,
    UploadFile,
    status,
)
from fastapi.responses import FileResponse
from pydantic.networks import AnyUrl

from saltapi.repository.unit_of_work import UnitOfWork
from saltapi.service.authentication_service import get_current_user
from saltapi.service.user import User
from saltapi.settings import get_settings
from saltapi.web import services
from saltapi.web.schema.common import ProposalCode, Semester
from saltapi.web.schema.proposal import ProposalProgress

proposals_dir = pathlib.Path(get_settings().proposals_dir)

router = APIRouter(prefix="/progress", tags=["Proposals"])


@router.get(
    "/{proposal_code}/",
    summary="Get URLs for all proposal progress report pdfs",
    response_model=Dict[str, Dict[str, AnyUrl]],
)
def get_urls_for_proposal_progress_report_pdfs(
    request: Request,
    proposal_code: ProposalCode = Path(
        ...,
        title="Proposal code",
        description="Proposal code of the proposal whose progress reports pdfs are requested.",
    ),
    user: User = Depends(get_current_user),
) -> Dict[str, Dict[str, AnyUrl]]:
    """
    Return URLs for all proposal progress report pdfs of a given proposal.
    """
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_view_proposal(user, proposal_code)

        proposal_service = services.proposal_service(unit_of_work.connection)

        progress_report_urls = (
            proposal_service.get_urls_for_proposal_progress_report_pdfs(
                proposal_code, request, router
            )
        )
        progress_report_pdfs = dict()
        for semester in progress_report_urls:
            progress_report_pdfs[semester] = {
                "proposal_progress_pdf": cast(
                    AnyUrl, progress_report_urls[semester]["proposal_progress_pdf"]
                )
            }

        return progress_report_pdfs


@router.get(
    "/{proposal_code}/{semester}",
    summary="Get a proposal progress report",
    response_model=ProposalProgress,
)
def get_proposal_progress_report(
    request: Request,
    proposal_code: ProposalCode = Path(
        ...,
        title="Proposal code",
        description="Proposal code of the proposal whose progress report is requested.",
    ),
    semester: Semester = Path(..., title="Semester", description="Semester"),
    user: User = Depends(get_current_user),
) -> ProposalProgress:
    """
    Returns the progress report for a proposal and semester. The semester is the
    semester for which the progress is reported. For example, if the semester is
    2021-1, the report covers the observations up to and including the 2021-1
    semester, and it requests time for the 2021-2 semester.

    The proposal progress report is returned as a JSON string, and it does not include the
    additional file uploaded by the user when creating the report. There is another
    endpoint for returning the report as a pdf, including the additional file and the
    original scientific justification.
    """
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_view_proposal(user, proposal_code)

        proposal_service = services.proposal_service(unit_of_work.connection)
        progress_report = proposal_service.get_progress_report(
            proposal_code, semester, request, router
        )

        return ProposalProgress(**progress_report)


@router.put(
    "/{proposal_code}/{semester}",
    summary="Create or update a progress report",
)
def put_progress_report(
    proposal_code: ProposalCode = Path(
        ...,
        title="Proposal code",
        description="Proposal code of the proposal whose progress report is created or"
        " updated.",
    ),
    semester: Semester = Path(..., title="Semester", description="Semester"),
    proposal_progress: ProposalProgress = Body(
        ..., title="Progress report", description="Progress report for a proposal."
    ),
    file: Optional[UploadFile] = File(...),
    user: User = Depends(get_current_user),
) -> ProposalProgress:
    """
    Creates or updates the progress report for a proposal and semester. The semester
    is the semester for which the progress is reported. For example, if the semester
    is 2021-1, the report covers the observations up to and including the 2021-1
    semester and it requests time for the 2021-2 semester.

    The optional pdf file is intended for additional details regarding the progress with
    the proposal.
    """
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_view_proposal(user, proposal_code)

    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.get(
    "/{proposal_code}/{semester}/report.pdf",
    summary="Get a proposal progress report pdf",
    responses={200: {"content": {"application/pdf": {}}}},
)
def get_proposal_progress_report_pdf(
    request: Request,
    proposal_code: ProposalCode = Path(
        ...,
        title="Proposal code",
        description="Proposal code of the proposal whose progress report is requested.",
    ),
    semester: Semester = Path(..., title="Semester", description="Semester"),
    user: User = Depends(get_current_user),
) -> FileResponse:
    """
    Returns the progress report pdf for a proposal and semester.
    """
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_view_proposal(user, proposal_code)

        proposal_service = services.proposal_service(unit_of_work.connection)
        progress_report_pdf_path = proposal_service.get_proposal_progress_report_pdf(
            proposal_code, semester
        )
        pdf_path = urllib.parse.urlparse(progress_report_pdf_path).path

        filename = "ProgressReport_{}.pdf".format(semester)

        return FileResponse(pdf_path, media_type="application/pdf", filename=filename)


@router.get(
    "/{proposal_code}/{semester}/supplementary-file.pdf",
    summary="Get a proposal progress report pdf",
    responses={200: {"content": {"application/pdf": {}}}},
)
def get_supplementary_proposal_progress_report_pdf(
    request: Request,
    proposal_code: ProposalCode = Path(
        ...,
        title="Proposal code",
        description="Proposal code of the proposal whose progress report is requested.",
    ),
    semester: Semester = Path(..., title="Semester", description="Semester"),
    user: User = Depends(get_current_user),
) -> FileResponse:
    """
    Returns the supplementary progress report pdf for a proposal and semester.
    """
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_view_proposal(user, proposal_code)

        proposal_service = services.proposal_service(unit_of_work.connection)
        supplementary_progress_report_pdf_path = (
            proposal_service.get_supplementary_proposal_progress_report_pdf(
                proposal_code, semester
            )
        )

        pdf_path = urllib.parse.urlparse(supplementary_progress_report_pdf_path).path

        filename = "ProgressReportSupplement_{}.pdf".format(semester)

        return FileResponse(pdf_path, media_type="application/pdf", filename=filename)
