from os.path import exists
from typing import List, Optional

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Path,
    Request,
    UploadFile,
)
from fastapi.responses import FileResponse, StreamingResponse
from starlette import status

from saltapi.repository.unit_of_work import UnitOfWork
from saltapi.service.authentication_service import get_current_user
from saltapi.service.proposal import ProposalProgressReport as _ProposalProgressReport
from saltapi.service.proposal_service import generate_pdf_path
from saltapi.service.user import User
from saltapi.web import services
from saltapi.web.schema.common import ProposalCode, Semester
from saltapi.web.schema.proposal import (
    ProposalProgress,
    ProposalProgressInput,
    ProposalProgressReport,
)

router = APIRouter(prefix="/progress", tags=["Proposals"])


@router.get(
    "/{proposal_code}/",
    summary="Get URLs for all proposal progress report pdfs",
    response_model=List[ProposalProgressReport],
)
def get_urls_for_proposal_progress_report_pdfs(
    request: Request,
    proposal_code: ProposalCode = Path(
        ...,
        title="Proposal code",
        description=(
            "Proposal code of the proposal whose progress report pdf URLs are"
            " requested."
        ),
    ),
    user: User = Depends(get_current_user),
) -> List[_ProposalProgressReport]:
    """
    Return URLs for all proposal progress report pdfs of a given proposal.
    """
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_view_proposal(user, proposal_code)

        proposal_service = services.proposal_service(unit_of_work.connection)

        progress_reports = proposal_service.get_urls_for_proposal_progress_report_pdfs(
            proposal_code, request, router
        )

        return progress_reports


@router.get(
    "/{proposal_code}/{semester}",
    summary="Get a proposal progress report",
    response_model=ProposalProgress,
    responses={200: {"content": {"application/pdf": {}}}},
)
def get_proposal_progress_report(
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
    semester, and its requested time for the 2021-2 semester.

    The proposal progress report is returned as a JSON string, and it does include the
    progress report and the supplementary files URLs uploaded by the user when creating
    the report. There is another endpoint for returning the report as a pdf, including
    the supplementary file and the original scientific justification.
    """
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_view_proposal(user, proposal_code)

        proposal_service = services.proposal_service(unit_of_work.connection)
        proposal_progress_report = proposal_service.get_progress_report(
            proposal_code, semester
        )
        return ProposalProgress(**proposal_progress_report)


@router.put(
    "/{proposal_code}/{semester}",
    summary="Create or update a progress report",
    response_model=ProposalProgress,
    responses={200: {"content": {"application/pdf": {}}}},
)
async def put_proposal_progress_report(
    proposal_code: ProposalCode = Path(
        ...,
        title="Proposal code",
        description=(
            "Proposal code of the proposal whose progress report is created or updated."
        ),
    ),
    semester: Semester = Path(..., title="Semester", description="Semester"),
    proposal_progress: ProposalProgressInput = Depends(ProposalProgressInput.as_form),  # type: ignore # noqa: E501
    additional_pdf: Optional[UploadFile] = File(default=None),
    user: User = Depends(get_current_user),
) -> ProposalProgress:
    """
    Creates or updates the progress report for a proposal and semester. The semester
    is the semester for which the progress is reported. For example, if the semester
    is 2021-1, the report covers the observations up to and including the 2021-1
    semester and, it requests time for the 2021-2 semester.

    The optional pdf file is intended for additional details regarding the progress with
    the proposal.
    """
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_update_proposal_progress(
            user, proposal_code
        )
        proposal_service = services.proposal_service(unit_of_work.connection)
        await proposal_service.put_proposal_progress(
            proposal_progress, proposal_code, semester, additional_pdf
        )
        unit_of_work.commit()

        proposal_progress_report = proposal_service.get_progress_report(
            proposal_code,
            semester,
        )
        return ProposalProgress(**proposal_progress_report)


@router.get(
    "/{proposal_code}/{semester}/report.pdf",
    summary="Get a proposal progress report pdf",
    responses={200: {"content": {"application/pdf": {}}}},
)
async def get_proposal_progress_report_pdf(
    proposal_code: ProposalCode = Path(
        ...,
        title="Proposal code",
        description="Proposal code of the proposal whose progress report is requested.",
    ),
    semester: Semester = Path(..., title="Semester", description="Semester"),
    user: User = Depends(get_current_user),
) -> StreamingResponse:
    """
    Returns the progress report pdf for a proposal and semester.
    """
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_view_proposal(user, proposal_code)

        proposal_service = services.proposal_service(unit_of_work.connection)
        proposal_progress_byte_io = proposal_service.generate_proposal_progress_pdf(
            proposal_code, semester
        )
        try:
            return StreamingResponse(
                proposal_progress_byte_io,
                headers={
                    "Content-Disposition": (
                        f"inline; filename=ProposalProgressReport-{semester}.pdf"
                    )
                },
                media_type="application/pdf",
            )
        except FileNotFoundError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get(
    "/{proposal_code}/{semester}/supplementary-file.pdf",
    summary="Get an additional proposal progress report pdf",
    responses={200: {"content": {"application/pdf": {}}}},
)
def get_supplementary_proposal_progress_report_pdf(
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
        progress_report_pdfs = proposal_service.get_progress_report(
            proposal_code, semester
        )

        additional_pdf_path = generate_pdf_path(
            proposal_code, progress_report_pdfs["additional_pdf"]
        )

        filename = "ProgressReportSupplement_{}.pdf".format(semester)

        if not additional_pdf_path:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if exists(additional_pdf_path):
            return FileResponse(
                additional_pdf_path, media_type="application/pdf", filename=filename
            )
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
