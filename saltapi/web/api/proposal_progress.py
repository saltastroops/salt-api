import pathlib
import urllib.parse
from typing import Any, Optional

from fastapi import (
    APIRouter,
    Body,
    Depends,
    File,
    HTTPException,
    Path,
    UploadFile,
    status,
)
from fastapi.responses import FileResponse

from saltapi.repository.unit_of_work import UnitOfWork
from saltapi.service.authentication_service import get_current_user
from saltapi.service.user import User
from saltapi.settings import get_settings
from saltapi.web import services
from saltapi.web.schema.common import ProposalCode, Semester
from saltapi.web.schema.proposal import ProposalProgress

proposals_dir = pathlib.Path(get_settings().proposals_dir)

router = APIRouter(prefix="/progress", tags=["Proposals"])


# @router.get(
#     "/{proposal_code}/",
#     summary="Get a list proposal progress reports pdfs",
# )
# def get_list_of_proposal_progress_reports_pdfs(
#         proposal_code: ProposalCode = Path(
#             ...,
#             title="Proposal code",
#             description="Proposal code of the proposal whose progress reports pdfs are requested.",
#         ),
#         user: User = Depends(get_current_user),
# ) -> Dict[str, Any]:
#     """
#     Returns a list of progress reports pdf for a proposal.
#     """
#     with UnitOfWork() as unit_of_work:
#         permission_service = services.permission_service(unit_of_work.connection)
#         permission_service.check_permission_to_view_proposal(user, proposal_code)
#
#         proposal_service = services.proposal_service(unit_of_work.connection)
#
#         progress_reports_pdfs = proposal_service.list_of_progress_reports_pdfs(
#             proposal_code
#         )
#         for key in progress_reports_pdfs:
#             progress_reports_pdfs[key] = router.url_path_for(
#                 "get_proposal_progress_report_pdf",
#                 proposal_code=proposal_code,
#                 progress_report_pdf_path=progress_reports_pdfs[key],
#             )
#
#         return progress_reports_pdfs


@router.get(
    "/{proposal_code}/{semester}",
    summary="Get a proposal progress report",
)
def get_proposal_progress_report(
    proposal_code: ProposalCode = Path(
        ...,
        title="Proposal code",
        description="Proposal code of the proposal whose progress report is requested.",
    ),
    semester: Semester = Path(..., title="Semester", description="Semester"),
    user: User = Depends(get_current_user),
) -> Any:
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
        progress_report = proposal_service.get_progress_report(proposal_code, semester)

        progress_report["proposal_progress_pdf"] = (
            router.url_path_for(
                "get_proposal_progress_report_pdf",
                proposal_code=proposal_code,
                semester=semester,
            )
            if progress_report["proposal_progress_pdf"]
            else None
        )

        progress_report["additional_pdf"] = (
            router.url_path_for(
                "get_supplementary_proposal_progress_report_pdf",
                proposal_code=proposal_code,
                semester=semester,
            )
            if progress_report["additional_pdf"]
            else None
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
)
def get_proposal_progress_report_pdf(
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

        progress_report_pdf_path = proposal_service.get_progress_report_pdf(
            proposal_code, semester
        )

        pdf_path = urllib.parse.unquote(urllib.parse.unquote(progress_report_pdf_path))

        return FileResponse(
            pdf_path, media_type="application/pdf", filename=pathlib.Path(pdf_path).name
        )


@router.get(
    "/{proposal_code}/{semester}/supplementary-report.pdf",
    summary="Get a proposal progress report pdf",
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

        progress_report_pdf_path = (
            proposal_service.get_supplementary_progress_report_pdf(
                proposal_code, semester
            )
        )

        pdf_path = urllib.parse.unquote(urllib.parse.unquote(progress_report_pdf_path))

        return FileResponse(
            pdf_path, media_type="application/pdf", filename=pathlib.Path(pdf_path).name
        )
