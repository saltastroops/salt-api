import pathlib
from typing import Any, Dict, List, Optional, Union

from fastapi import APIRouter, Request
from starlette.routing import URLPath

from saltapi.exceptions import NotFoundError
from saltapi.repository.proposal_repository import ProposalRepository
from saltapi.service.proposal import Proposal, ProposalListItem
from saltapi.service.user import User
from saltapi.settings import get_settings
from saltapi.util import next_semester, semester_start
from saltapi.web.schema.common import ProposalCode, Semester




def generate_route_url(request: Request, router_path: URLPath) -> str:

    url = "{}://{}:{}{}".format(
        request.url.scheme, request.client.host, request.client.port, router_path
    )
    return url


def generate_pdf_path(
    proposal_code: str, filename: str = None
) -> Union[pathlib.Path, None]:
    proposals_dir = get_settings().proposals_dir
    return (
        pathlib.Path(proposals_dir / proposal_code / "Included" / filename)
        .resolve()
        .as_uri()
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
        proposals_dir = get_settings().proposals_dir
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

    def get_urls_for_proposal_progress_report_pdfs(
        self, proposal_code: ProposalCode, request: Request, router: APIRouter
    ) -> Dict[str, Dict[str, str]]:
        semesters = self.repository.list_of_semesters(proposal_code)

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
        request: Request,
        router: APIRouter,
    ) -> Dict[str, Any]:
        progress_report = self.repository.get_progress_report(proposal_code, semester)

        if not progress_report:
            raise NotFoundError(f"No progress report for proposal {proposal_code}")

        progress_pdf_url = router.url_path_for(
            "get_proposal_progress_report_pdf",
            proposal_code=proposal_code,
            semester=semester,
        )

        progress_report["proposal_progress_pdf"] = (
            generate_route_url(request, progress_pdf_url)
            if progress_report["proposal_progress_pdf"]
            else None
        )

        additional_progress_pdf_url = router.url_path_for(
            "get_supplementary_proposal_progress_report_pdf",
            proposal_code=proposal_code,
            semester=semester,
        )
        progress_report["additional_pdf"] = (
            generate_route_url(request, additional_progress_pdf_url)
            if progress_report["additional_pdf"]
            else None
        )
        return progress_report

    def get_proposal_progress_report_pdf(
        self,
        proposal_code: ProposalCode,
        semester: Semester,
    ) -> Optional[Dict[str, Any]]:
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
