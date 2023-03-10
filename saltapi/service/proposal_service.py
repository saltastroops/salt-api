import pathlib
import urllib.parse
from io import BytesIO
from typing import Any, Dict, List, Optional, cast

import pdfkit
from fastapi import APIRouter, Request, UploadFile
from PyPDF2 import PdfMerger
from starlette.datastructures import URLPath

from saltapi.exceptions import NotFoundError, AuthorizationError, ValidationError
from saltapi.repository.proposal_repository import ProposalRepository
from saltapi.service.create_proposal_progress_html import (
    create_proposal_progress_html,
)
from saltapi.service.proposal import ProposalListItem
from saltapi.service.user import User
from saltapi.settings import get_settings
from saltapi.util import parse_partner_requested_percentages, semester_start
from saltapi.web.schema.common import ProposalCode, Semester
from saltapi.web.schema.proposal import ProposalProgressInput


def generate_route_url(request: Request, router_path: URLPath) -> str:
    url = urllib.parse.urljoin(str(request.base_url), router_path)
    return url


def generate_pdf_path(
    proposal_code: str, filename: Optional[str]
) -> Optional[pathlib.Path]:
    proposals_dir = get_settings().proposals_dir
    return (
        pathlib.Path(proposals_dir / proposal_code / "Included" / filename).absolute()
        if filename
        else None
    )


class ProposalService:
    def __init__(self, repository: ProposalRepository):
        self.repository = repository

    def list_proposal_summaries(
        self,
        username: str,
        from_semester: str = "2000-1",
        to_semester: str = "2099-2",
        limit: int = 1000,
    ) -> List[ProposalListItem]:
        """
        Return the list of proposals for a semester range.

        The maximum number of proposals to be returned can be set with the limit
        parameter; the default is 1000.
        """
        if semester_start(from_semester) > semester_start(to_semester):
            raise ValueError(
                "The from semester must not be later than the to semester."
            )

        if limit < 0:
            raise ValueError("The limit must not be negative.")

        return self.repository.list(username, from_semester, to_semester, limit)

    def get_phase1_summary(self, proposal_code: str) -> pathlib.Path:
        """
        Return the file path of the latest Phase 1 proposal summary file.

        Parameters
        ----------
        proposal_code: str
            Proposal code.

        Returns
        -------
        `~pathlib.Path`
            The file path of the latest Phase 1 proposal summary file.
        """
        return self.repository.get_phase1_summary(proposal_code)

    def get_proposal_file(self, proposal_code: str) -> pathlib.Path:
        """
        Return the file path of the proposal zip file.

        Parameters
        ----------
        proposal_code: str
            Proposal code.

        Returns
        -------
        `~pathlib.Path`
            The file path of the proposal zip file.
        """
        return self.repository.get_proposal_file(proposal_code)

    def get_proposal(self, proposal_code: str) -> Dict[str, Any]:
        """
        Return the JSON representation of a proposal.

        Parameters
        ----------
        proposal_code: str
            Proposal code.

        Returns
        -------
        Proposal
            The JSON representation of the proposal.
        """
        return cast(Dict[str, Any], self.repository.get(proposal_code))

    def get_observation_comments(self, proposal_code: str) -> List[Dict[str, str]]:
        return self.repository.get_observation_comments(proposal_code)

    def add_observation_comment(
        self, proposal_code: str, comment: str, user: User
    ) -> Dict[str, str]:
        return self.repository.add_observation_comment(proposal_code, comment, user)

    def get_urls_for_proposal_progress_report_pdfs(
        self, proposal_code: ProposalCode, request: Request, router: APIRouter
    ) -> Dict[str, Dict[str, str]]:
        semesters = self.repository.get_progress_report_semesters(proposal_code)

        progress_report_urls = dict()
        for semester in semesters:
            progress_report_pdf_url = router.url_path_for(
                "get_proposal_progress_report_pdf",
                proposal_code=proposal_code,
                semester=semester,
            )
            progress_report_urls[semester] = {
                "proposal_progress_pdf": generate_route_url(
                    request, progress_report_pdf_url
                ),
            }

        return progress_report_urls

    def get_progress_report(
        self,
        proposal_code: ProposalCode,
        semester: Semester,
    ) -> Dict[str, Any]:
        return self.repository.get_progress_report(proposal_code, semester)

    def get_proposal_progress_report_pdfs(
        self,
        proposal_code: ProposalCode,
        semester: Semester,
    ) -> Dict[str, Any]:
        progress_report = self.repository.get_progress_report(proposal_code, semester)

        progress_report_pdfs = {
            "proposal_progress_pdf": generate_pdf_path(
                proposal_code, progress_report["proposal_progress_pdf"]
            ),
            "additional_pdf": generate_pdf_path(
                proposal_code, progress_report["additional_pdf"]
            ),
        }

        return progress_report_pdfs

    async def put_proposal_progress(
        self,
        proposal_progress_report: ProposalProgressInput,
        proposal_code: str,
        semester: str,
        additional_pdf: Optional[UploadFile],
    ) -> None:
        partner_requested_percentages = parse_partner_requested_percentages(
            proposal_progress_report.partner_requested_percentages
        )
        proposal_progress = {
            "semester": semester,
            "requested_time": proposal_progress_report.requested_time,
            "maximum_seeing": proposal_progress_report.maximum_seeing,
            "transparency": proposal_progress_report.transparency,
            # fmt: off
            "description_of_observing_constraints":
                proposal_progress_report.description_of_observing_constraints,
            "change_reason": proposal_progress_report.change_reason,
            # fmt: off
            "summary_of_proposal_status":
                proposal_progress_report.summary_of_proposal_status,
            "strategy_changes": proposal_progress_report.strategy_changes,
            "partner_requested_percentages": partner_requested_percentages,
        }

        # Get the content and filename of the additional pdf, if there is one
        additional_pdf_filename = None
        additional_pdf_content = b""
        if additional_pdf:
            additional_pdf_content = await additional_pdf.read()
            additional_pdf_filename = (
                self.repository.generate_proposal_progress_filename(
                    additional_pdf_content, is_supplementary=True
                )
            )

        # Store the progress report in the database
        filenames = {
            "proposal_progress_filename": None,
            "additional_pdf_filename": additional_pdf_filename,
        }
        self.repository.put_proposal_progress(
            proposal_progress, proposal_code, semester, filenames
        )

        # Save the additional file to disk. This is done last as the file should not be
        # stored if the progress report cannot be stored in the database.
        if additional_pdf_filename:
            additional_pdf_path = (
                ProposalService._included_dir(proposal_code) / additional_pdf_filename
            )
            additional_pdf_path.write_bytes(additional_pdf_content)

    @staticmethod
    def _included_dir(proposal_code: str) -> pathlib.Path:
        base_dir = get_settings().proposals_dir
        return base_dir / proposal_code / "Included"

    def _create_progress_description(
        self, proposal_code: str, semester: str, progress_report: Dict[str, Any]
    ) -> bytes:
        previous_allocated_requested = self.repository.get_allocated_and_requested_time(
            proposal_code
        )
        previous_observed_time = self.repository.get_observed_time(proposal_code)

        previous_requests = []
        for ar in previous_allocated_requested:
            for ot in previous_observed_time:
                if ot["semester"] == ar["semester"]:
                    previous_requests.append(
                        {
                            "semester": ar["semester"],
                            "requested_time": ar["requested_time"],
                            "allocated_time": ar["allocated_time"],
                            "observed_time": ot["observed_time"],
                        }
                    )

        html_content = create_proposal_progress_html(
            proposal_code=proposal_code,
            semester=semester,
            previous_requests=previous_requests,
            previous_conditions=self.repository.get_latest_observing_conditions(
                proposal_code, semester
            ),
            new_request=progress_report,
        )
        options = {
            "page-size": "A4",
            "margin-top": "20mm",
            "margin-right": "20mm",
            "margin-bottom": "20mm",
            "margin-left": "20mm",
            "encoding": "UTF-8",
            "no-outline": None,
        }
        return cast(bytes, pdfkit.from_string(html_content, options=options))

    def generate_proposal_progress_pdf(
        self,
        proposal_code: ProposalCode,
        semester: Semester,
    ) -> BytesIO:
        """
        Generate the proposal progress PDF for a proposal.

        The report is created by joining the progress description, the supplementary
        file (if there is one) and the phase 1 pdf summary. The progress description
        is generated on the fly from the database content.
        """
        progress_report = self.repository.get_progress_report(proposal_code, semester)
        progress_description = self._create_progress_description(
            proposal_code, semester, progress_report
        )

        with PdfMerger(strict=False) as merger:
            merger.append(BytesIO(progress_description))

            if progress_report["additional_pdf"]:
                additional_pdf_path = (
                    ProposalService._included_dir(proposal_code)
                    / progress_report["additional_pdf"]
                )
                merger.append(additional_pdf_path)

            try:
                phase1_summary = self.repository.get_phase1_summary(proposal_code)
                merger.append(phase1_summary)
            except NotFoundError:
                pass

            b = BytesIO()
            merger.write(b)
            b.seek(0)
            return b

    def create_proprietary_period_extension_request(
        self,
        proposal_code: str,
        proprietary_period: int,
        motivation: str,
        username: str,
    ) -> None:
        self.repository.insert_proprietary_period_extension_request(
            proposal_code, proprietary_period, motivation, username
        )

    def update_proprietary_period(
        self, proposal_code: str, proprietary_period: int
    ) -> None:
        self.repository.update_proprietary_period(
            proposal_code=proposal_code, proprietary_period=proprietary_period
        )

    def get_proposal_status(self, proposal_code: str) -> Dict[str, str]:
        """
        Get the proposal status for a proposal code.
        """
        return self.repository.get_proposal_status(proposal_code)

    def update_proposal_status(
        self, proposal_code: str, status: str, status_comment: Optional[str]
    ) -> None:
        """
        Set the proposal status for a proposal code.
        """
        self.repository.update_proposal_status(proposal_code, status, status_comment)

    def update_investigator_proposal_approval_status(
        self, user_id: int, proposal_code: str, approved: bool
    ) -> None:
        """
        Updates the investigator's approval status of the proposal.
        """
        self.repository.update_investigator_proposal_approval_status(
            user_id, proposal_code, approved
        )
