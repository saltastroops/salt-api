from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from saltapi.service.mail_service import MailService
from saltapi.service.proposal_service import ProposalService
from saltapi.web.api import proposals as proposals_api
from saltapi.web.schema.proposal import ProprietaryPeriodExtensionDecision


def _create_proposal_service(pc: dict, pi: dict) -> ProposalService:
    repository = MagicMock()
    repository.get_principal_contact.return_value = pc
    repository.get_principal_investigator.return_value = pi
    return ProposalService(repository)


def test_decision_notification_sends_grant_to_pc_and_pi_and_escapes_reason() -> None:
    proposal_code = "2020-1-SCI-005"
    service = _create_proposal_service(
        {"given_name": "Alice", "family_name": "Smith", "email": "alice@example.com"},
        {"given_name": "Bob", "family_name": "Jones", "email": "bob@example.com"},
    )
    reason = "Approved <script>alert('x')</script>"

    with patch.object(MailService, "send_email") as send_email, patch.object(
        MailService, "generate_email", wraps=MailService.generate_email
    ) as generate_email:
        service.notify_pc_and_pi_of_proprietary_period_extension_decision(
            proposal_code=proposal_code,
            granted_period=36,
            reason=reason,
        )

    assert send_email.call_count == 2
    assert generate_email.call_count == 2
    assert [call.kwargs["to"] for call in send_email.call_args_list] == [
        ["alice@example.com"],
        ["bob@example.com"],
    ]
    for call in generate_email.call_args_list:
        assert call.kwargs["subject"] == (
            f"Proprietary period extension decision for {proposal_code}"
        )
        assert "has been granted" in call.kwargs["plain_body"]
        assert "Granted proprietary period: 36 months" in call.kwargs["plain_body"]
        assert reason in call.kwargs["plain_body"]
        assert "&lt;script&gt;" in call.kwargs["html_body"]
        assert "<script>" not in call.kwargs["html_body"]


def test_decline_notification_omits_empty_reason_and_deduplicates_recipients() -> None:
    proposal_code = "2020-1-SCI-005"
    contact = {
        "given_name": "Alice",
        "family_name": "Smith",
        "email": "alice@example.com",
    }
    service = _create_proposal_service(contact, contact)

    with patch.object(MailService, "send_email") as send_email, patch.object(
        MailService, "generate_email", wraps=MailService.generate_email
    ) as generate_email:
        service.notify_pc_and_pi_of_proprietary_period_extension_decision(
            proposal_code=proposal_code,
            granted_period=0,
        )

    send_email.assert_called_once()
    generate_email.assert_called_once()
    email = generate_email.call_args.kwargs
    assert "has been declined" in email["plain_body"]
    assert "No additional proprietary period was granted." in email["plain_body"]
    assert "Decision reason:" not in email["plain_body"]
    assert "Decision reason:" not in email["html_body"]


def _mock_decision_endpoint(monkeypatch, request_proposal_code: str):
    unit_of_work = MagicMock()
    unit_of_work.__enter__.return_value = unit_of_work

    def exit_unit_of_work(exc_type, *_):
        if exc_type:
            unit_of_work.rollback()
        return False

    unit_of_work.__exit__.side_effect = exit_unit_of_work

    repository = MagicMock()
    repository.update_proprietary_period_extension_request.return_value = (
        request_proposal_code
    )
    repository.get_principal_contact.return_value = {
        "given_name": "Alice",
        "family_name": "Smith",
        "email": "alice@example.com",
    }
    repository.get_principal_investigator.return_value = {
        "given_name": "Bob",
        "family_name": "Jones",
        "email": "bob@example.com",
    }
    proposal_service = ProposalService(repository)
    permission_service = MagicMock()
    monkeypatch.setattr(proposals_api, "UnitOfWork", lambda: unit_of_work)
    monkeypatch.setattr(
        proposals_api.services, "permission_service", lambda connection: permission_service
    )
    monkeypatch.setattr(
        proposals_api.services, "proposal_service", lambda connection: proposal_service
    )
    return unit_of_work, proposal_service, repository


@pytest.mark.parametrize("granted_period", [36, 0])
def test_decision_endpoint_records_and_notifies_grant_or_decline(
    monkeypatch: pytest.MonkeyPatch, granted_period: int
) -> None:
    proposal_code = "2020-1-SCI-005"
    unit_of_work, _, repository = _mock_decision_endpoint(
        monkeypatch, proposal_code
    )
    decision = ProprietaryPeriodExtensionDecision(
        request_id=5,
        granted_period=granted_period,
        reason="Decision reason",
    )

    with patch.object(MailService, "send_email") as send_email, patch.object(
        ProposalService, "update_proprietary_period_in_ssda"
    ) as update_ssda:
        proposals_api.add_proprietary_period_extension_decision(
            proposal_code=proposal_code,
            decision=decision,
            user=MagicMock(),
        )

    repository.update_proprietary_period_extension_request.assert_called_once_with(
        request_id=5,
        granted_proprietary_period=granted_period,
        reason="Decision reason",
    )
    if granted_period > 0:
        update_ssda.assert_called_once_with(
            proposal_code=proposal_code,
            proprietary_period=granted_period,
        )
    else:
        update_ssda.assert_not_called()
    assert send_email.call_count == 2
    for email_call in send_email.call_args_list:
        email_body = email_call.kwargs["message"].get_payload()[0].get_payload()
        if granted_period > 0:
            assert "has been granted" in email_body
            assert f"Granted proprietary period: {granted_period} months" in email_body
        else:
            assert "has been declined" in email_body
            assert "No additional proprietary period was granted." in email_body
        assert "Decision reason" in email_body
    unit_of_work.commit.assert_called_once()


def test_decision_endpoint_rejects_mismatched_request_before_external_updates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    proposal_code = "2020-1-SCI-005"
    unit_of_work, _, repository = _mock_decision_endpoint(
        monkeypatch, "2020-2-SCI-043"
    )

    with patch.object(MailService, "send_email") as send_email, patch.object(
        ProposalService, "update_proprietary_period_in_ssda"
    ) as update_ssda:
        with pytest.raises(HTTPException) as error:
            proposals_api.add_proprietary_period_extension_decision(
                proposal_code=proposal_code,
                decision=ProprietaryPeriodExtensionDecision(
                    request_id=5,
                    granted_period=36,
                    reason="Decision reason",
                ),
                user=MagicMock(),
            )

    assert error.value.status_code == 400
    update_ssda.assert_not_called()
    send_email.assert_not_called()
    unit_of_work.commit.assert_not_called()
    unit_of_work.rollback.assert_called_once()