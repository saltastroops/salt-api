import pathlib
import urllib.parse
from datetime import datetime
from typing import Any, Dict, List

import pytz

from saltapi.exceptions import NotFoundError
from saltapi.repository.proposal_repository import ProposalRepository
from saltapi.service.proposal import Proposal, ProposalListItem
from saltapi.service.user import User
from saltapi.settings import get_settings
from saltapi.util import next_semester, semester_of_datetime, semester_start
from saltapi.web.schema.common import ProposalCode, Semester

proposals_dir = pathlib.Path(get_settings().proposals_dir)


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

    def insert_proposal_progress(
        self, proposal_code: ProposalCode, progress_report_data: Dict[str, Any]
    ) -> None:
        semester = next_semester()
        self.repository.insert_proposal_progress(
            progress_report_data, proposal_code, semester
        )

        requested_time = progress_report_data["requested_time"]
        for rp in progress_report_data["requested_percentages"]:
            partner_code = rp["partner_code"]
            partner_percentage = rp["partner_percentage"]
            time_requested_per_partner = requested_time * (partner_percentage / 100)
            self.repository._insert_progress_report_requested_time(
                proposal_code=proposal_code,
                semester=semester,
                partner_code=partner_code,
                requested_time_percent=partner_percentage,
                requested_time_amount=time_requested_per_partner,
            )
        self.repository._insert_observing_conditions(
            proposal_code=proposal_code,
            semester=semester,
            seeing=progress_report_data["maximum_seeing"],
            transparency=progress_report_data["transparency"],
            observing_conditions_description=progress_report_data[
                "observing_constraints"
            ],
        )

    def list_of_progress_reports_pdfs(
        self, proposal_code: ProposalCode
    ) -> Dict[str, Any]:
        progress_reports_list = self.repository.list_of_progress_reports_pdfs(
            proposal_code
        )

        current_semester = Semester(semester_of_datetime(datetime.now(tz=pytz.utc)))

        if current_semester in progress_reports_list:
            del progress_reports_list[current_semester]

        progress_reports_list = {
            k: v for k, v in progress_reports_list.items() if v != "NULL"
        }

        progress_reports_list = {
            key: urllib.parse.quote(
                pathlib.Path(
                    proposals_dir
                    / proposal_code
                    / "Included"
                    / progress_reports_list[key]
                )
                .resolve()
                .as_posix(),
                safe="",
            )
            for key in progress_reports_list
        }

        return progress_reports_list

    def get_progress_report_pdf(
        self, proposal_code: ProposalCode, semester: Semester
    ) -> str:
        progress_report_pdf = self.repository.get_progress_report_pdf(
            proposal_code, semester
        )

        progress_report_pdf_path = (
            urllib.parse.quote(
                pathlib.Path(
                    proposals_dir / proposal_code / "Included" / progress_report_pdf
                )
                .resolve()
                .as_posix(),
                safe="",
            )
            if progress_report_pdf
            else None
        )

        return progress_report_pdf_path

    def get_supplementary_progress_report_pdf(
        self, proposal_code: ProposalCode, semester: Semester
    ) -> str:
        supplementary_progress_report_pdf = (
            self.repository.get_supplementary_progress_report_pdf(
                proposal_code, semester
            )
        )

        progress_report_pdf_path = (
            urllib.parse.quote(
                pathlib.Path(
                    proposals_dir
                    / proposal_code
                    / "Included"
                    / supplementary_progress_report_pdf
                )
                .resolve()
                .as_posix(),
                safe="",
            )
            if supplementary_progress_report_pdf
            else None
        )

        return progress_report_pdf_path

    def get_progress_report(
        self, proposal_code: ProposalCode, semester: Semester
    ) -> Dict[str, Any]:
        progress_report = self.repository.get_progress_report(proposal_code, semester)

        progress_report_pdf_path = (
            urllib.parse.quote(
                pathlib.Path(
                    proposals_dir
                    / proposal_code
                    / "Included"
                    / progress_report["proposal_progress_pdf"]
                )
                .resolve()
                .as_posix(),
                safe="",
            )
            if progress_report["proposal_progress_pdf"]
            else None
        )
        additional_progress_report_pdf_path = (
            urllib.parse.quote(
                pathlib.Path(
                    proposals_dir
                    / proposal_code
                    / "Included"
                    / progress_report["additional_pdf"]
                )
                .resolve()
                .as_posix(),
                safe="",
            )
            if progress_report["additional_pdf"]
            else None
        )

        progress_report["proposal_progress_pdf"] = progress_report_pdf_path

        progress_report["additional_pdf"] = additional_progress_report_pdf_path

        return progress_report
