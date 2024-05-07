from datetime import datetime
from typing import Any, Dict, List, Tuple

from saltapi.repository.status_repository import (
    StatusRepository,
    SubsystemStatusDetails,
)
from saltapi.service.mail_service import MailService
from saltapi.settings import get_settings
from saltapi.web.schema.status import SubsystemStatusUpdate


class StatusService:
    def __init__(self, status_repository: StatusRepository):
        self.status_repository = status_repository

    def get_status(self) -> List[SubsystemStatusDetails]:
        return self.status_repository.get_status()

    def add_status_update(self, subsystem_status_update: SubsystemStatusUpdate) -> None:
        subsystem_status_details: SubsystemStatusDetails = {
            "expected_available_again_at": subsystem_status_update.expected_available_again_at,
            "reason": subsystem_status_update.reason,
            "reporting_user": subsystem_status_update.reporting_user,
            "status": subsystem_status_update.status.value,
            "status_changed_at": subsystem_status_update.status_changed_at,
            "subsystem": subsystem_status_update.subsystem,
        }
        self.status_repository.update_status(subsystem_status_details)

        self._send_email_notification(subsystem_status_details)

    @staticmethod
    def _send_email_notification(status_details: Dict[str, Any]):
        # Get the list of recipients
        recipients_string = get_settings().status_update_email_recipients
        recipients = [r.strip() for r in recipients_string.split(",")]

        # Generate the email text
        plain, html = StatusService._status_email_text(status_details)

        # Send an email to all the recipients
        for recipient in recipients:
            message = MailService.generate_email(
                to=recipient,
                subject="SALT status update",
                html_body=html,
                plain_body=plain,
            )
            MailService.send_email(message=message, to=[recipient])

    @staticmethod
    def _status_email_text(status_details: Dict[str, Any]) -> Tuple[str, str]:
        if status_details["subsystem"].lower() == "telescope":
            subsystem = "The telescope"
        else:
            subsystem = status_details["subsystem"]
        html = f"""\
<p>Good day,</p>

<p>The status of SALT has changed as follows:</p>

<p>{subsystem} is {status_details["status"].lower()}.
"""
        if status_details["reason"]:
            html += f"""\
<br>Reason: {status_details["reason"]}            
        """
        html += "</p>"
        eta: datetime = status_details["expected_available_again_at"]
        if eta:
            day = eta.strftime("%d").lstrip("0")
            html += f"""\

<p>{subsystem} is expected to be available again on {day} {eta.strftime("%B %Y")} at {eta.strftime("%X")} UTC.</p>
                    """
        html += """\

<p>Kind regards,</p>

<p>SALT Astronomy Operations</p>
"""

        plain = html.replace("<p>", "").replace("</p>", "").replace("<br>", "")

        return plain, html
