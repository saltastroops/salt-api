import pathlib
from typing import Any, Dict, List, Optional
from fastapi import UploadFile
import pdfkit

from saltapi.exceptions import NotFoundError
from saltapi.repository.proposal_repository import ProposalRepository
from saltapi.service.create_proposal_progress_html import create_proposal_progress_html
from saltapi.service.proposal import Proposal, ProposalListItem
from saltapi.service.user import User
from saltapi.settings import get_settings
from saltapi.util import semester_start
from saltapi.web.schema.common import ProposalCode, Semester
from saltapi.web.schema.proposal import ProposalProgressReport


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

    def get_proposal_zip(self, proposal_code: str) -> pathlib.Path:
        """
        Return the file path of proposal zip file.

        Parameters
        ----------
        proposal_code: str
            Proposal code.

        Returns
        -------
        `~pathlib.Path`
            The file path of the proposal zip file.
        """
        proposals_dir = pathlib.Path(get_settings().proposals_dir)
        version = self.repository.get_current_version(proposal_code)
        path = proposals_dir / proposal_code / str(version) / f"{proposal_code}.zip"
        if not path.exists():
            raise NotFoundError("Proposal file not found")
        return path

    def get_proposal(self, proposal_code: str) -> Proposal:
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
        return self.repository.get(proposal_code)

    def get_observation_comments(self, proposal_code: str) -> List[Dict[str, str]]:
        return self.repository.get_observation_comments(proposal_code)

    def add_observation_comment(
        self, proposal_code: str, comment: str, user: User
    ) -> Dict[str, str]:
        return self.repository.add_observation_comment(proposal_code, comment, user)

    def get_progress_report(
        self, proposal_code: ProposalCode, semester: Semester
    ) -> Dict[str, Any]:
        return self.repository.get_progress_report(proposal_code, semester)

    async def post_proposal_progress(
        self,
        proposal_progress_report: ProposalProgressReport,
        proposal_code: str,
        semester: str,
        additional_pdf: Optional[UploadFile]
    ) -> None:
        partner_requested_percentages = []
        for p in proposal_progress_report.partner_requested_percentages.split(";"):
            prp = p.split(":")
            partner_requested_percentages.append({
                "partner_code": prp[0],
                "requested_percentage": prp[1]
            })
        proposal_progress = {
            "semester": semester,
            "requested_time": proposal_progress_report.requested_time,
            "maximum_seeing": proposal_progress_report.maximum_seeing,
            "transparency": proposal_progress_report.transparency,
            "description_of_observing_constraints": proposal_progress_report.description_of_observing_constraints,
            "change_reason": proposal_progress_report.change_reason,
            "summary_of_proposal_status": proposal_progress_report.summary_of_proposal_status,
            "strategy_changes": proposal_progress_report.strategy_changes,
            "partner_requested_percentages": partner_requested_percentages
        }
        filenames = await self.create_progress_report_pdf(proposal_code, semester, proposal_progress, additional_pdf)
        self.repository.post_proposal_progress(
            proposal_progress, proposal_code, semester, filenames
        )

    async def create_progress_report_pdf(
        self,
        proposal_code: str,
        semester: str,
        new_request: Dict[str, Any],
        additional_pdf: Optional[UploadFile]
    ) -> Dict[str, str or None]:

        previous_allocated_requested = self.repository.get_allocated_and_requested_time(proposal_code)
        previous_observed_time = self.repository.get_observed_time(proposal_code)

        previous_requests = []
        for ar in previous_allocated_requested:
            for ot in previous_observed_time:
                if ot["semester"] == ar["semester"]:
                    previous_requests.append({
                        "semester": ar["semester"],
                        "requested_time": ar["requested_time"],
                        "allocated_time": ar["allocated_time"],
                        "observed_time": ot["observed_time"]
                    })
        html_content = create_proposal_progress_html(
            proposal_code=proposal_code,
            semester=semester,
            previous_requests=previous_requests,
            previous_conditions=self.repository.get_latest_observing_conditions(proposal_code, semester),
            new_request=new_request
        )
        base_dir = f"{get_settings().proposals_dir}/{proposal_code}/Included/"
        proposal_progress_filename = self.repository.generate_proposal_progress_filename(html_content)
        additional_pdf_filename = None
        options = {
            'page-size': 'A4',
            'margin-top': '20mm',
            'margin-right': '20mm',
            'margin-bottom': '20mm',
            'margin-left': '20mm',
            'encoding': "UTF-8",
            'no-outline': None
        }
        pdfkit.from_string(html_content, base_dir + proposal_progress_filename, options=options)
        if additional_pdf:
            additional_pdf_filename = self.repository.generate_proposal_progress_filename(
                additional_pdf.file.read(), is_supplementary=True
            )
            with open(base_dir + additional_pdf_filename, "wb") as f:
                f.write(additional_pdf.file.read())

        return {
            "proposal_progress_filename": proposal_progress_filename,
            "additional_pdf_filename": additional_pdf_filename
        }
