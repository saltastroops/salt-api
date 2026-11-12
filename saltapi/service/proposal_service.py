import pathlib
import urllib.parse
from html import escape as html_escape
from io import BytesIO
from typing import Any, Dict, List, Optional, Tuple, cast

import requests
from fastapi import APIRouter, Request, UploadFile
from loguru import logger
from PyPDF2 import PdfMerger
from starlette.datastructures import URLPath
from weasyprint import HTML

from saltapi.exceptions import NotFoundError, SSDAError
from saltapi.repository.proposal_repository import ProposalRepository
from saltapi.service.create_proposal_progress_html import (
    create_proposal_progress_html,
)
from saltapi.service.mail_service import MailService
from saltapi.service.proposal import ProposalListItem
from saltapi.service.user import User
from saltapi.settings import get_settings
from saltapi.util import (
    next_semester,
    parse_partner_requested_percentages,
    semester_start,
)
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

    def get_proposal_file(
        self, proposal_code: str, phase: Optional[int] = None
    ) -> pathlib.Path:
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
        return self.repository.get_proposal_file(proposal_code, phase)

    def get_proposal(
        self,
        proposal_code: str,
        semester: Optional[Semester] = None,
        phase: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Return the JSON representation of a proposal.

        Parameters
        ----------
        proposal_code: str
            Proposal code.

        semester: str | None
            Semester.

        phase: int | None
            Phase.

        Returns
        -------
        Proposal
            The JSON representation of the proposal.
        """
        return cast(Dict[str, Any], self.repository.get(proposal_code, semester, phase))

    def get_observation_comments(self, proposal_code: str) -> List[Dict[str, str]]:
        return self.repository.get_observation_comments(proposal_code)

    def add_observation_comment(
        self, proposal_code: str, comment: str, user: User
    ) -> Dict[str, str]:
        return self.repository.add_observation_comment(proposal_code, comment, user)

    def get_urls_for_proposal_progress_report_pdfs(
        self, proposal_code: ProposalCode, request: Request, router: APIRouter
    ) -> List[Dict[str, Any]]:
        semesters = self.repository.get_progress_report_semesters(proposal_code)

        progress_reports: List[Dict[str, Any]] = []
        for semester in semesters:
            progress_report_pdf_url = router.url_path_for(
                "get_proposal_progress_report_pdf",
                proposal_code=proposal_code,
                semester=semester,
            )

            progress_reports.append(
                {
                    "semester": semester,
                    "url": generate_route_url(request, progress_report_pdf_url),
                }
            )

        return progress_reports

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
        proposal_progress = await self.prepare_proposal_progress(
            semester, proposal_progress_report
        )
        (
            additional_pdf_filename,
            additional_pdf_content,
        ) = await self.handle_additional_pdf(additional_pdf)

        filenames = {
            "proposal_progress_filename": None,
            "additional_pdf_filename": additional_pdf_filename,
        }

        self.repository.put_proposal_progress(
            proposal_progress, proposal_code, semester, filenames
        )

        if additional_pdf_filename:
            await self.save_progress_report_file(
                proposal_code, additional_pdf_filename, additional_pdf_content
            )

        (
            progress_pdf_filename,
            progress_pdf_content,
        ) = await self.handle_proposal_progress_pdf(proposal_code, semester)
        await self.save_progress_report_file(
            proposal_code, progress_pdf_filename, progress_pdf_content
        )
        final_filenames = {
            "proposal_progress_filename": progress_pdf_filename,
            "additional_pdf_filename": additional_pdf_filename,
        }
        self.repository.put_proposal_progress(
            proposal_progress, proposal_code, semester, final_filenames
        )

    @staticmethod
    async def prepare_proposal_progress(
        semester: str, proposal_progress_report: ProposalProgressInput
    ) -> Dict[str, Any]:
        partner_requested_percentages = parse_partner_requested_percentages(
            proposal_progress_report.partner_requested_percentages
        )
        return {
            "semester": semester,
            "requested_time": proposal_progress_report.requested_time,
            "maximum_seeing": proposal_progress_report.maximum_seeing,
            "transparency": proposal_progress_report.transparency,
            "description_of_observing_constraints": (
                proposal_progress_report.description_of_observing_constraints
            ),
            "change_reason": proposal_progress_report.change_reason,
            "summary_of_proposal_status": (
                proposal_progress_report.summary_of_proposal_status
            ),
            "strategy_changes": proposal_progress_report.strategy_changes,
            "partner_requested_percentages": partner_requested_percentages,
        }

    async def handle_additional_pdf(
        self, additional_pdf: Optional[UploadFile]
    ) -> Tuple[Optional[str], Optional[bytes]]:
        additional_pdf_filename = None
        additional_pdf_content = b""
        if additional_pdf:
            additional_pdf_content = await additional_pdf.read()
            additional_pdf_filename = (
                self.repository.generate_proposal_progress_filename(
                    additional_pdf_content, is_supplementary=True
                )
            )
        return additional_pdf_filename, additional_pdf_content

    async def handle_proposal_progress_pdf(
        self, proposal_code: str, semester: str
    ) -> Tuple[str, bytes]:
        proposal_progress_byte_io = self.generate_proposal_progress_pdf(
            cast(ProposalCode, proposal_code), cast(Semester, semester)
        )
        progress_pdf_content = proposal_progress_byte_io.read()
        progress_pdf_filename = self.repository.generate_proposal_progress_filename(
            progress_pdf_content
        )
        return progress_pdf_filename, progress_pdf_content

    @staticmethod
    async def save_progress_report_file(
        proposal_code: str, filename: str, content: bytes
    ) -> None:
        file_path = ProposalService._included_dir(proposal_code) / filename
        file_path.write_bytes(content)

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
        previous_observed_times = self.repository.get_observed_p0_to_p3_time(
            proposal_code
        )

        def previous_observed_time(_semester: str) -> int:
            for ot in previous_observed_times:
                if ot["semester"] == _semester:
                    return int(ot["observed_time"])
            return 0

        previous_requests = []
        for ar in previous_allocated_requested:
            previous_requests.append(
                {
                    "semester": ar["semester"],
                    "requested_time": ar["requested_time"],
                    "allocated_time": ar["allocated_time"],
                    "observed_time": previous_observed_time(ar["semester"]),
                }
            )

        html_content = create_proposal_progress_html(
            proposal_code=proposal_code,
            semester=semester,
            previous_requests=previous_requests,
            previous_conditions=self.repository.get_latest_observing_conditions(
                proposal_code, next_semester(semester)
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
        return HTML(string=html_content).write_pdf()

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
        requester: User,
    ) -> None:
        self.repository.insert_proprietary_period_extension_request(
            proposal_code, proprietary_period, motivation, requester.username
        )
        self.send_proprietary_period_extension_notification_to_salt_help(
            proposal_code=proposal_code,
            proprietary_period=proprietary_period,
            motivation=motivation,
            requester=requester,
        )
        self.send_proprietary_period_extension_notification_to_pc_and_pi(
            proposal_code=proposal_code,
            proprietary_period=proprietary_period,
            motivation=motivation,
            requester=requester,
        )

    def send_proprietary_period_extension_notification(
        self,
        proposal_code: str,
        requester: User,
        proprietary_period: int,
        motivation: str,
    ) -> None:
        self.send_proprietary_period_extension_notification_to_salt_help(
            proposal_code=proposal_code,
            proprietary_period=proprietary_period,
            motivation=motivation,
            requester=requester,
        )
        self.send_proprietary_period_extension_notification_to_pc_and_pi(
            proposal_code=proposal_code,
            proprietary_period=proprietary_period,
            motivation=motivation,
            requester=requester,
        )

    def send_proprietary_period_extension_notification_to_salt_help(
        self,
        proposal_code: str,
        requester: User,
        proprietary_period: int,
        motivation: str,
    ) -> None:
        salt_help_email = get_settings().salt_help_email
        user_name = f"{requester.given_name} {requester.family_name}".strip()
        user_email = f"{requester.email}".strip()

        # Notification to salt_help
        salt_help_plain = f"""Dear SALT Help,

{ user_name } <{user_email}> is requesting to change the proprietary period of proposal {proposal_code} to {proprietary_period} months.\n
"""
        if motivation:
            salt_help_plain += (f"""
                \n----------\nMotivation:\n{motivation}\n----------\n
            """)
        salt_help_plain += f"""
The URL for the proposal is: https://www.salt.ac.za/wm/proposal/{proposal_code}\n
Kind regards,\n
Your Friendly Web Manager
"""

        salt_help_html = f"""
<html>
  <head></head>
  <div>
    <p>Dear SALT Help,</p>
    <p>{ user_name } <{user_email}> is requesting to change the proprietary period of proposal {proposal_code} to {proprietary_period} months.\n</p>
"""
        if motivation:
            salt_help_html += (f"""
                <p>----------</p>
                <p><b>Motivation:</b><br>{motivation}</p>
                <p>----------</p>
            """)

        salt_help_html += f"""
    <p>The URL for the proposal is: https://www.salt.ac.za/wm/proposal/{proposal_code}</p>    
    <p>Kind regards,</p>
    <p>Your Friendly Web Manager</p>
  </div>
</html>
"""
        salt_help_message = MailService.generate_email(
            to=salt_help_email,
            subject=f"Proprietary period extension request for {proposal_code}",
            html_body=salt_help_html,
            plain_body=salt_help_plain,
        )
        MailService.send_email(to=[salt_help_email], message=salt_help_message)

    def send_proprietary_period_extension_notification_to_pc_and_pi(
            self,
            proposal_code: str,
            requester: User,
            proprietary_period: int,
            motivation: str,
    ) -> None:
        pc = self.repository.get_principal_contact(proposal_code)
        pi = self.repository.get_principal_investigator(proposal_code)

        pc_name = f"{pc['given_name']} {pc['family_name']}".strip()
        pi_name = f"{pi['given_name']} {pi['family_name']}".strip()

        pc_email = pc["email"].strip()
        pi_email = pi["email"].strip()

        requester_name = f"{requester.given_name} {requester.family_name}".strip()
        requester_email = requester.email.strip()

        recipients = {
            pc_email: {"name": pc_name, "email": pc_email},
            pi_email: {"name": pi_name, "email": pi_email},
        }

        for recipient in recipients.values():
            is_requester = recipient["email"] == requester_email

            salutation = f"Dear {recipient['name']},"

            if is_requester:
                message_intro = (
                    f"Your request to extend the proprietary period for "
                    f"proposal {proposal_code} has been received and is "
                    "awaiting approval."
                )
            else:
                message_intro = (
                    f"{requester_name} has submitted a request to extend the "
                    f"proprietary period for proposal {proposal_code}. "
                    "The request is awaiting approval."
                )

            notification_plain = f"""{salutation}

{message_intro}

Requested proprietary period: {proprietary_period} months

Motivation:
{motivation}

Kind regards,

SALT Team
"""

            notification_html = f"""
<html>
  <body>
    <p>{salutation}</p>
    <p>{message_intro}</p>
    <p><b>Requested proprietary period:</b> {proprietary_period} months</p>
    <p><b>Motivation:</b><br>{motivation}</p>
    <p>Kind regards,</p>
    <p>SALT Team</p>
  </body>
</html>
"""

            notification_message = MailService.generate_email(
                to=f"{recipient['name']} <{recipient['email']}>",
                subject=f"Proprietary period extension request for {proposal_code}",
                html_body=notification_html,
                plain_body=notification_plain,
            )

            MailService.send_email(
                to=[recipient["email"]],
                message=notification_message,
            )

    def notify_pc_and_pi_of_proprietary_period_extension_decision(
        self,
        proposal_code: str,
        granted_period: int,
        reason: Optional[str] = None,
    ) -> None:
        try:
            pc = self.repository.get_principal_contact(proposal_code)
            pi = self.repository.get_principal_investigator(proposal_code)

            pc_name = f"{pc['given_name']} {pc['family_name']}".strip()
            pi_name = f"{pi['given_name']} {pi['family_name']}".strip()

            pc_email = pc["email"].strip()
            pi_email = pi["email"].strip()

            recipients = {
                pc_email: pc_name,
                pi_email: pi_name,
            }
            decision_message = (
                f"The proprietary period extension request for proposal "
                f"{proposal_code} has been considered."
            )
            period_message = (
                f"Granted proprietary period: {granted_period} months"
            )
            if reason:
                period_message += (
                    f"\nReason:\n{reason}"
                )

            for recipient_email, recipient_name in recipients.items():
                salutation = f"Dear {recipient_name},"

                notification_plain = f"""{salutation}

{decision_message}
{period_message}
"""
                notification_html = f"""
<html>
  <body>
    <p>{salutation}</p>
    <p>{decision_message}</p>
    <p>{period_message}</p>
"""
                if reason:
                    notification_plain += f"\nDecision reason:\n{reason}\n"
                    notification_html += (
                        f"    <p><b>Decision reason:</b><br>"
                        f"{html_escape(reason)}</p>\n"
                    )

                notification_plain += """

Kind regards,

SALT Team
"""
                notification_html += """
    <p>Kind regards,</p>
    <p>SALT Team</p>
  </body>
</html>
"""

                notification_message = MailService.generate_email(
                    to=f"{recipient_name} <{recipient_email}>",
                    subject=f"Proprietary period extension decision for {proposal_code}",
                    html_body=notification_html,
                    plain_body=notification_plain,
                )

                MailService.send_email(
                    to=[recipient_email],
                    message=notification_message,
                )
        except Exception as e:
            error_message = (
                f"Failed to send email to PC/PI for proposal {proposal_code}: \n{str(e)}"
            )
            logger.exception(error_message)
            raise RuntimeError(error_message) from e


    def update_proprietary_period_in_ssda(
        self, proposal_code: str, proprietary_period: int
    ) -> None:
        release_date = self.repository.get_release_date(
            proprietary_period, proposal_code
        )
        body = {
            "query": (
                "mutation($proposalCode:String!,$institution:Institution!,$apiKey:String!,$releaseDate:String!){updateReleaseDates(proposalCode:$proposalCode,institution:$institution,apiKey:$apiKey,metadataReleaseDate:$releaseDate,dataReleaseDate:$releaseDate){status}}"
            ),
            "variables": {
                "proposalCode": proposal_code,
                "institution": "SALT",
                "releaseDate": str(release_date),
                "apiKey": get_settings().ssda_api_key,
            },
        }

        try:
            response = requests.post(get_settings().ssda_api_url, json=body)
            response.raise_for_status()
            ssda_response = response.json()
        except Exception as error:
            logger.error(f"SSDA Error start\n{error}\nSSDA error end")
            raise SSDAError(f"Failed to update SAAO SALT Data Archive: {error}") from error

        if ssda_response.get("errors"):
            for err in ssda_response["errors"]:
                error_message = f"SSDA Error start\n{err}\nSSDA error end"
                logger.error(error_message)
            raise SSDAError(f"SSDA errors: {ssda_response['errors']}")

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
        allowed_statuses = {
            1: ["Accepted", "Deleted", "Rejected", "Under scientific review"],
            2: [
                "Active",
                "Completed",
                "Deleted",
                "Expired",
                "Inactive",
                "Under technical review",
            ],
        }
        phase = self.repository.latest_submission_phase(proposal_code)
        if status not in allowed_statuses[phase]:
            raise ValueError(f"Proposal status not allowed for phase {phase}")
        self.repository.update_proposal_status(proposal_code, status, status_comment)

    def update_is_self_activatable(
        self, proposal_code: str, is_self_activatable: bool
    ) -> None:
        self.repository.update_is_self_activatable(proposal_code, is_self_activatable)

    def is_self_activatable(self, proposal_code: str) -> bool:
        return self.repository.is_self_activatable(proposal_code)

    def update_liaison_astronomer(
        self, proposal_code: str, liaison_astronomer_id: Optional[int]
    ) -> None:
        self.repository.update_liaison_astronomer(proposal_code, liaison_astronomer_id)

    def get_liaison_astronomer(self, proposal_code: str) -> Optional[Dict[str, Any]]:
        return self.repository.get_liaison_astronomer(proposal_code)

    def update_investigator_proposal_approval_status(
        self, approval_user_id: int, proposal_code: str, approved: bool
    ) -> None:
        """
        Updates the investigator's approval status of the proposal.
        """
        self.repository.update_investigator_proposal_approval_status(
            approval_user_id, proposal_code, approved
        )

    def get_pools(
        self, proposal_code: str, semester: Optional[Semester] = None
    ) -> List[Dict[str, Any]]:
        return self.repository.get_pools(proposal_code, semester)

    @staticmethod
    def get_proposal_attachments_dir(proposal_code: str) -> pathlib.Path:
        return get_settings().proposals_dir / proposal_code / "Included"

    def proposals_requesting_proprietary_request_extension(self) -> List[Dict[str, Any]]:
        return self.repository.proprietary_period_extension_requests()

    def update_proprietary_period_extension_request(
        self,
        proposal_code: str,
        granted_proprietary_period: int,
        reason: Optional[str] = None,
    ) -> None:
        self.repository.update_proprietary_period_extension_request(
            proposal_code=proposal_code,
            granted_proprietary_period=granted_proprietary_period,
            reason=reason,
        )