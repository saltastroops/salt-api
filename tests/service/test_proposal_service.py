from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest
import requests

from saltapi.exceptions import SSDAError
from saltapi.service.mail_service import MailService
from saltapi.service.proposal_service import ProposalService
from saltapi.service.user import User


def _create_mock_user(
    given_name: str = "Test",
    family_name: str = "User",
    email: str = "testuser@example.com",
    username: str = "testuser",
) -> User:
    return User(
        id=1,
        username=username,
        given_name=given_name,
        family_name=family_name,
        email=email,
        password_hash="hash",
        affiliations=[],
        roles=[],
        user_verified=True,
        active=True,
        demographics=None,
    )


@pytest.fixture
def mock_settings(monkeypatch: pytest.MonkeyPatch) -> SimpleNamespace:
    settings = SimpleNamespace(
        salt_help_email="help@example.com",
        from_email="webmanager@example.com",
        ssda_api_key="test-api-key",
        ssda_api_url="https://ssda.example.com/graphql",
    )
    monkeypatch.setattr(
        "saltapi.service.proposal_service.get_settings", lambda: settings
    )
    monkeypatch.setattr("saltapi.service.mail_service.get_settings", lambda: settings)
    return settings


def test_send_proprietary_period_extension_notification_to_salt_help(
    mock_settings: SimpleNamespace,
) -> None:
    proposal_code = "2099-1-TST-001"
    repo = MagicMock()
    service = ProposalService(repo)
    user = _create_mock_user(
        given_name="Alex", family_name="Example", email="alex@example.com"
    )

    with patch.object(MailService, "send_email") as mock_send, patch.object(
        MailService, "generate_email", wraps=MailService.generate_email
    ) as mock_generate:
        service.send_proprietary_period_extension_notification_to_salt_help(
            proposal_code=proposal_code,
            requester=user,
            proprietary_period=24,
            motivation="Need more time for analysis",
        )

        assert mock_generate.call_count == 1
        assert mock_send.call_count == 1

        salt_help_call = mock_generate.call_args_list[0].kwargs
        assert salt_help_call["to"] == mock_settings.salt_help_email
        assert proposal_code in salt_help_call["subject"]
        for body_type in ["plain_body", "html_body"]:
            assert proposal_code in salt_help_call[body_type]
            assert "Alex Example" in salt_help_call[body_type]
            assert "alex@example.com" in salt_help_call[body_type]
            assert "24 months" in salt_help_call[body_type]
            assert "Need more time for analysis" in salt_help_call[body_type]
        mock_send.assert_called_once()
        sent_message = mock_send.call_args.kwargs["message"]
        assert mock_send.call_args.kwargs["to"] == [mock_settings.salt_help_email]
        assert sent_message["To"] == mock_settings.salt_help_email
        assert sent_message["Subject"] == salt_help_call["subject"]


def test_send_proprietary_period_extension_notification_to_pc_and_pi_same_person(
    mock_settings: SimpleNamespace,
) -> None:
    proposal_code = "2099-1-TST-001"
    repo = MagicMock()
    pc = {
        "given_name": "Alex",
        "family_name": "Example",
        "email": "alex@example.com",
    }
    repo.get_principal_contact.return_value = pc
    repo.get_principal_investigator.return_value = pc
    service = ProposalService(repo)
    pc_name = f"{pc['given_name']} {pc['family_name']}".strip()
    pc_email = pc["email"]

    user = _create_mock_user(
        given_name=pc["given_name"],
        family_name=pc["family_name"],
        email=pc["email"],
    )

    with patch.object(MailService, "send_email") as mock_send, patch.object(
        MailService, "generate_email", wraps=MailService.generate_email
    ) as mock_generate:
        service.send_proprietary_period_extension_notification_to_pc_and_pi(
            proposal_code=proposal_code,
            requester=user,
            proprietary_period=24,
            motivation="Need more time for analysis",
        )

        assert mock_generate.call_count == 1
        assert mock_send.call_count == 1

        pc_call = mock_generate.call_args_list[0].kwargs
        assert pc_call["to"] == f"{pc_name} <{pc_email}>"
        assert proposal_code in pc_call["subject"]
        for body_type in ["plain_body", "html_body"]:
            assert f"Dear {pc_name}," in pc_call[body_type]
            assert "Your request to extend" in pc_call[body_type]
            assert proposal_code in pc_call[body_type]
            assert "24 months" in pc_call[body_type]
            assert "Need more time for analysis" in pc_call[body_type]
        mock_send.assert_called_once()
        sent_message = mock_send.call_args.kwargs["message"]
        assert mock_send.call_args.kwargs["to"] == [pc_email]
        assert sent_message["To"] == f"{pc_name} <{pc_email}>"
        assert sent_message["Subject"] == pc_call["subject"]


def test_send_proprietary_period_extension_notification_to_pc_and_pi_different_people(
    mock_settings: SimpleNamespace,
) -> None:
    proposal_code = "2099-1-TST-001"
    pc = {"given_name": "Alex", "family_name": "Example", "email": "alex@example.com"}
    pi = {"given_name": "Pat", "family_name": "Sample", "email": "pat@example.com"}
    repo = MagicMock()
    repo.get_principal_contact.return_value = pc
    repo.get_principal_investigator.return_value = pi
    service = ProposalService(repo)
    requester = _create_mock_user(
        given_name="Alex", family_name="Example", email="alex@example.com"
    )

    with patch.object(MailService, "send_email") as mock_send, patch.object(
        MailService, "generate_email", wraps=MailService.generate_email
    ) as mock_generate:
        service.send_proprietary_period_extension_notification_to_pc_and_pi(
            proposal_code=proposal_code,
            requester=requester,
            proprietary_period=12,
            motivation="Additional analysis is required",
        )

    assert mock_generate.call_count == 2
    assert mock_send.call_count == 2
    pc_email, pi_email = mock_generate.call_args_list
    assert pc_email.kwargs["to"] == "Alex Example <alex@example.com>"
    assert pi_email.kwargs["to"] == "Pat Sample <pat@example.com>"
    assert "Your request to extend" in pc_email.kwargs["plain_body"]
    assert "Alex Example has submitted a request" in pi_email.kwargs["plain_body"]
    for email_call in (pc_email, pi_email):
        assert proposal_code in email_call.kwargs["subject"]
        assert "12 months" in email_call.kwargs["plain_body"]
        assert "Additional analysis is required" in email_call.kwargs["plain_body"]
    assert [call.kwargs["to"] for call in mock_send.call_args_list] == [
        ["alex@example.com"],
        ["pat@example.com"],
    ]


def test_send_proprietary_period_extension_notification() -> None:
    proposal_code = "2099-1-TST-001"
    service = ProposalService(MagicMock())
    user = _create_mock_user(given_name="Alex", family_name="Example")

    with patch.object(
        service, "send_proprietary_period_extension_notification_to_salt_help"
    ) as mock_salt_help, patch.object(
        service, "send_proprietary_period_extension_notification_to_pc_and_pi"
    ) as mock_pc_pi:
        service.send_proprietary_period_extension_notification(
            proposal_code=proposal_code,
            requester=user,
            proprietary_period=24,
            motivation="Need more time for analysis",
        )

        mock_salt_help.assert_called_once_with(
            proposal_code=proposal_code,
            proprietary_period=24,
            motivation="Need more time for analysis",
            requester=user,
        )
        mock_pc_pi.assert_called_once_with(
            proposal_code=proposal_code,
            proprietary_period=24,
            motivation="Need more time for analysis",
            requester=user,
        )


def test_send_proprietary_period_extension_notification_custom_salt_help(
    mock_settings: SimpleNamespace,
) -> None:
    proposal_code = "2099-1-TST-001"
    service = ProposalService(MagicMock())
    requester = _create_mock_user()

    mock_settings.salt_help_email = "custom-help@example.com"

    with patch.object(MailService, "send_email"), patch.object(
        MailService, "generate_email", wraps=MailService.generate_email
    ) as mock_generate:
        service.send_proprietary_period_extension_notification_to_salt_help(
            proposal_code=proposal_code,
            requester=requester,
            proprietary_period=18,
            motivation="Motivation text",
        )

    assert mock_generate.call_args.kwargs["to"] == mock_settings.salt_help_email


def test_create_proprietary_period_extension_request() -> None:
    proposal_code = "2099-1-TST-001"
    repo = MagicMock()
    service = ProposalService(repo)
    user = _create_mock_user(given_name="Alex", family_name="Example", username="aexample")

    with patch.object(
        service, "send_proprietary_period_extension_notification_to_salt_help"
    ) as mock_salt_help, patch.object(
        service, "send_proprietary_period_extension_notification_to_pc_and_pi"
    ) as mock_pc_pi:
        service.create_proprietary_period_extension_request(
            proposal_code=proposal_code,
            proprietary_period=12,
            motivation="Need time",
            requester=user,
        )

        repo.insert_proprietary_period_extension_request.assert_called_once_with(
            proposal_code, 12, "Need time", "aexample"
        )
        mock_salt_help.assert_called_once_with(
            proposal_code=proposal_code,
            proprietary_period=12,
            motivation="Need time",
            requester=user,
        )
        mock_pc_pi.assert_called_once_with(
            proposal_code=proposal_code,
            proprietary_period=12,
            motivation="Need time",
            requester=user,
        )


def test_update_proprietary_period_in_ssda_success(
    mock_settings: SimpleNamespace,
) -> None:
    repo = MagicMock()
    repo.get_release_date.return_value = "2022-01-01"
    service = ProposalService(repo)
    proposal_code = "2099-1-TST-001"

    mock_response = MagicMock()
    mock_response.json.return_value = {
        "data": {"updateReleaseDates": {"status": "SUCCESSFUL"}}
    }

    with patch(
        "saltapi.service.proposal_service.requests.post", return_value=mock_response
    ) as mock_post:
        service.update_proprietary_period_in_ssda(proposal_code, 24)

    mock_post.assert_called_once_with(
        mock_settings.ssda_api_url,
        json=mock_post.call_args.kwargs["json"],
    )
    assert mock_post.call_args.kwargs["json"]["variables"] == {
        "proposalCode": proposal_code,
        "institution": "SALT",
        "releaseDate": "2022-01-01",
        "apiKey": mock_settings.ssda_api_key,
    }


def test_update_proprietary_period_in_ssda_logs_and_raises_on_graphql_errors(
    mock_settings: SimpleNamespace,
) -> None:
    repo = MagicMock()
    repo.get_release_date.return_value = "2022-01-01"
    service = ProposalService(repo)
    proposal_code = "2099-1-TST-001"

    mock_response = MagicMock()
    mock_response.json.return_value = {
        "errors": [
            {
                "message": "Cannot update release dates",
                "locations": [{"line": 1, "column": 10}],
                "extensions": {"code": "FORBIDDEN"},
            },
            {
                "message": "Invalid proposal code",
                "path": ["updateReleaseDates"],
            },
        ]
    }

    with patch(
        "saltapi.service.proposal_service.requests.post", return_value=mock_response
    ), patch("saltapi.service.proposal_service.logger") as mock_logger:
        with pytest.raises(SSDAError):
            service.update_proprietary_period_in_ssda(proposal_code, 24)

    assert mock_logger.error.call_count == 2
    logged_msgs = [call.args[0] for call in mock_logger.error.call_args_list]
    assert "Cannot update release dates" in logged_msgs[0]
    assert "FORBIDDEN" in logged_msgs[0]
    assert "Invalid proposal code" in logged_msgs[1]
    assert "updateReleaseDates" in logged_msgs[1]


def test_update_proprietary_period_in_ssda_logs_and_raises_on_request_exception(
    mock_settings: SimpleNamespace,
) -> None:
    repo = MagicMock()
    repo.get_release_date.return_value = "2022-01-01"
    service = ProposalService(repo)
    proposal_code = "2099-1-TST-001"

    with patch(
        "saltapi.service.proposal_service.requests.post",
        side_effect=requests.exceptions.ConnectionError("Connection refused"),
    ), patch("saltapi.service.proposal_service.logger") as mock_logger:
        with pytest.raises(SSDAError):
            service.update_proprietary_period_in_ssda(proposal_code, 24)

    mock_logger.error.assert_called_once()
    assert "Connection refused" in mock_logger.error.call_args[0][0]


def test_proposals_requesting_more_time() -> None:
    repo = MagicMock()
    service = ProposalService(repo)
    expected = [
        {
            "id": 1,
            "proposal_code": "2099-1-TST-001",
            "grant_reason": None,
            "granted_period": None,
            "release_date": "2030-04-01",
            "current_request": {
                "request_motivation": "Need more time",
                "made_at": "2029-04-01T09:36:07",
                "requester": "Test Requester",
                "requester_email": "requester@example.com",
                "requested_period": 36,
            },
            "previous_requests": [],
        }
    ]
    repo.proprietary_period_extension_requests.return_value = expected

    result = service.proposals_requesting_proprietary_request_extension()

    repo.proprietary_period_extension_requests.assert_called_once_with()
    assert result == expected