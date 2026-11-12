from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from saltapi.exceptions import SSDAError
from saltapi.repository.proposal_repository import ProposalRepository
from saltapi.service.mail_service import MailService
from saltapi.service.proposal_service import ProposalService
from saltapi.web.api import proposals as proposals_api
from saltapi.web.schema.proposal import ProprietaryPeriodExtensionDecision


def _create_proposal_service(pc: dict, pi: dict) -> ProposalService:
    repository = MagicMock()
    repository.get_principal_contact.return_value = pc
    repository.get_principal_investigator.return_value = pi
    return ProposalService(repository)


def test_decision_notification_sends_grant_to_pc_and_pi_and_escapes_html() -> None:
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
        assert (
            f"for proposal {proposal_code} has been considered."
            in call.kwargs["plain_body"]
        )
        assert "Granted proprietary period: 36 months" in call.kwargs["plain_body"]
        assert call.kwargs["plain_body"].count(reason) == 2
        assert "&lt;script&gt;" in call.kwargs["html_body"]


def test_notification_omits_empty_reason_and_deduplicates_recipients() -> None:
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
            granted_period=12,
        )

    send_email.assert_called_once()
    generate_email.assert_called_once()
    email = generate_email.call_args.kwargs
    assert f"for proposal {proposal_code} has been considered." in email["plain_body"]
    assert "Granted proprietary period: 12 months" in email["plain_body"]
    assert "Decision reason:" not in email["plain_body"]
    assert "Decision reason:" not in email["html_body"]


def _mock_decision_endpoint(monkeypatch):
    unit_of_work = MagicMock()
    unit_of_work.__enter__.return_value = unit_of_work

    def exit_unit_of_work(exc_type, *_):
        if not exc_type:
            unit_of_work.commit.assert_called_once()
        unit_of_work.rollback()
        return False

    unit_of_work.__exit__.side_effect = exit_unit_of_work

    repository = MagicMock()
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

    def contact_before_exit(contact):
        def get_contact(_proposal_code):
            unit_of_work.commit.assert_called_once()
            unit_of_work.__exit__.assert_not_called()
            return contact

        return get_contact

    repository.get_principal_contact.side_effect = contact_before_exit(
        repository.get_principal_contact.return_value
    )
    repository.get_principal_investigator.side_effect = contact_before_exit(
        repository.get_principal_investigator.return_value
    )
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


def test_decision_endpoint_records_and_notifies_grant(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    proposal_code = "2020-1-SCI-005"
    granted_period = 36
    unit_of_work, _, repository = _mock_decision_endpoint(monkeypatch)
    decision = ProprietaryPeriodExtensionDecision(
        request_id=5,
        granted_period=granted_period,
        reason="Decision reason",
    )

    with patch.object(MailService, "send_email") as send_email, patch.object(
        ProposalService, "update_proprietary_period_in_ssda"
    ) as update_ssda:
        response = proposals_api.add_proprietary_period_extension_decision(
            proposal_code=proposal_code,
            decision=decision,
            user=MagicMock(),
        )

    repository.update_proprietary_period_extension_request.assert_called_once_with(
        proposal_code=proposal_code,
        granted_proprietary_period=granted_period,
        reason="Decision reason",
    )
    update_ssda.assert_called_once_with(
        proposal_code=proposal_code,
        proprietary_period=granted_period,
    )
    assert send_email.call_count == 2
    assert response["success"] is True
    assert response["email_sent"] is True
    for email_call in send_email.call_args_list:
        email_body = email_call.kwargs["message"].get_payload()[0].get_payload()
        assert f"for proposal {proposal_code} has been considered." in email_body
        assert f"Granted proprietary period: {granted_period} months" in email_body
        assert "Decision reason" in email_body
    unit_of_work.commit.assert_called_once()


def test_decision_endpoint_rejects_zero_before_updates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    unit_of_work, _, repository = _mock_decision_endpoint(monkeypatch)

    with patch.object(MailService, "send_email") as send_email, patch.object(
        ProposalService, "update_proprietary_period_in_ssda"
    ) as update_ssda:
        with pytest.raises(HTTPException) as error:
            proposals_api.add_proprietary_period_extension_decision(
                proposal_code="2020-1-SCI-005",
                decision=ProprietaryPeriodExtensionDecision(
                    request_id=5, granted_period=0, reason="Not approved"
                ),
                user=MagicMock(),
            )

    assert error.value.status_code == 400
    repository.update_proprietary_period_extension_request.assert_not_called()
    update_ssda.assert_not_called()
    send_email.assert_not_called()
    unit_of_work.commit.assert_not_called()
    unit_of_work.rollback.assert_called_once()


def test_decision_endpoint_rolls_back_if_ssda_update_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    unit_of_work, _, _ = _mock_decision_endpoint(monkeypatch)
    with patch.object(MailService, "send_email") as send_email, patch.object(
        ProposalService, "update_proprietary_period_in_ssda", side_effect=SSDAError("failed")
    ):
        with pytest.raises(HTTPException) as error:
            proposals_api.add_proprietary_period_extension_decision(
                proposal_code="2020-1-SCI-005",
                decision=ProprietaryPeriodExtensionDecision(request_id=5, granted_period=36),
                user=MagicMock(),
            )

    assert error.value.status_code == 500
    send_email.assert_not_called()
    unit_of_work.commit.assert_not_called()
    unit_of_work.rollback.assert_called_once()


def test_decision_endpoint_reports_email_failure_after_commit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    unit_of_work, _, _ = _mock_decision_endpoint(monkeypatch)
    with patch.object(
        MailService, "send_email", side_effect=RuntimeError("mail unavailable")
    ), patch.object(ProposalService, "update_proprietary_period_in_ssda"):
        response = proposals_api.add_proprietary_period_extension_decision(
            proposal_code="2020-1-SCI-005",
            decision=ProprietaryPeriodExtensionDecision(request_id=5, granted_period=36),
            user=MagicMock(),
        )

    assert response["success"] is True
    assert response["email_sent"] is False
    unit_of_work.commit.assert_called_once()


def test_repository_leaves_decision_timestamp_to_database() -> None:
    connection = MagicMock()
    connection.execute.return_value.one_or_none.return_value.request_id = 5
    repository = ProposalRepository(connection)
    repository.update_proprietary_period = MagicMock()

    repository.update_proprietary_period_extension_request(
        "2020-1-SCI-005", 36, "Approved"
    )

    statement, parameters = connection.execute.call_args_list[1].args
    assert set(statement._bindparams) == set(parameters)
    assert "made_at" not in parameters
    assert "MadeAt" not in str(statement)
    repository.update_proprietary_period.assert_called_once_with("2020-1-SCI-005", 36)