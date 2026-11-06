from unittest.mock import MagicMock, patch

import pytest
import requests
from sqlalchemy.engine import Connection

from saltapi.exceptions import SSDAError
from saltapi.repository.proposal_repository import ProposalRepository
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


def test_send_proprietary_period_extension_notification_to_salt_help(
    db_connection: Connection,
) -> None:
    proposal_code = "2020-1-SCI-005"
    repo = ProposalRepository(db_connection)
    service = ProposalService(repo)
    user = _create_mock_user(
        given_name="John", family_name="Doe", email="john@example.com"
    )

    with patch.object(MailService, "send_email") as mock_send, patch.object(
        MailService, "generate_email", wraps=MailService.generate_email
    ) as mock_generate:
        service.send_proprietary_period_extension_notification_to_salt_help(
            proposal_code=proposal_code,
            user=user,
            proprietary_period=24,
            motivation="Need more time for analysis",
        )

        assert mock_generate.call_count == 1
        assert mock_send.call_count == 1

        salt_help_call = mock_generate.call_args_list[0].kwargs
        assert "salthelp@salt.ac.za" in salt_help_call["to"]
        assert proposal_code in salt_help_call["subject"]
        assert proposal_code in salt_help_call["plain_body"]
        assert "John Doe" in salt_help_call["plain_body"]
        assert "john@example.com" in salt_help_call["plain_body"]
        assert "24 months" in salt_help_call["plain_body"]
        assert "Need more time for analysis" in salt_help_call["plain_body"]


def test_send_proprietary_period_extension_notification_to_pc_and_pi_same_person(
    db_connection: Connection,
) -> None:
    proposal_code = "2020-1-SCI-005"
    repo = ProposalRepository(db_connection)
    service = ProposalService(repo)

    pc = repo.get_principal_contact(proposal_code)
    pc_name = f"{pc['given_name']} {pc['family_name']}".strip()
    pc_email = pc["email"]

    user = _create_mock_user(
        given_name=pc["given_name"],
        family_name=pc["family_name"],
        email=pc["email"],
    )

    with patch.object(
        ProposalRepository, "get_principal_investigator", return_value=pc
    ):
        with patch.object(MailService, "send_email") as mock_send, patch.object(
            MailService, "generate_email", wraps=MailService.generate_email
        ) as mock_generate:
            service.send_proprietary_period_extension_notification_to_pc_and_pi(
                proposal_code=proposal_code,
                user=user,
                proprietary_period=24,
                motivation="Need more time for analysis",
            )

            assert mock_generate.call_count == 1
            assert mock_send.call_count == 1

            pc_call = mock_generate.call_args_list[0].kwargs
            assert pc_email in pc_call["to"]
            assert f"Dear {pc_name}," in pc_call["plain_body"]
            assert f"{pc_name}'s request to extend" in pc_call["plain_body"]
            assert proposal_code in pc_call["subject"]
            assert proposal_code in pc_call["plain_body"]
            assert "waiting for approval" in pc_call["plain_body"]
            assert "24 months" in pc_call["plain_body"]
            assert "Need more time for analysis" in pc_call["plain_body"]
            mock_send.assert_called_once_with(
                to=[pc_email], message=mock_generate.return_value
            )


def test_send_proprietary_period_extension_notification_to_pc_and_pi_different_people(
    db_connection: Connection,
) -> None:
    proposal_code = "2020-1-SCI-005"
    repo = ProposalRepository(db_connection)
    service = ProposalService(repo)

    pc = {"given_name": "Alice", "family_name": "Smith", "email": "alice@example.com"}
    pi = {"given_name": "Bob", "family_name": "Jones", "email": "bob@example.com"}

    # User is Alice (PC)
    user = _create_mock_user(
        given_name="Alice", family_name="Smith", email="alice@example.com"
    )

    with patch.object(
        ProposalRepository, "get_principal_contact", return_value=pc
    ), patch.object(ProposalRepository, "get_principal_investigator", return_value=pi):
        with patch.object(MailService, "send_email") as mock_send, patch.object(
            MailService, "generate_email", wraps=MailService.generate_email
        ) as mock_generate:
            service.send_proprietary_period_extension_notification_to_pc_and_pi(
                proposal_code=proposal_code,
                user=user,
                proprietary_period=12,
                motivation="Alice needs more time",
            )

            assert mock_generate.call_count == 1
            assert mock_send.call_count == 1

            call_kwargs = mock_generate.call_args_list[0].kwargs
            assert (
                "Alice Smith <alice@example.com>, Bob Jones <bob@example.com>"
                == call_kwargs["to"]
            )
            assert "Dear Alice Smith and Bob Jones," in call_kwargs["plain_body"]
            assert "Alice Smith's request to extend" in call_kwargs["plain_body"]
            mock_send.assert_called_once_with(
                to=["alice@example.com", "bob@example.com"],
                message=mock_generate.return_value,
            )


def test_send_proprietary_period_extension_notification(
    db_connection: Connection,
) -> None:
    proposal_code = "2020-1-SCI-005"
    repo = ProposalRepository(db_connection)
    service = ProposalService(repo)
    user = _create_mock_user(
        given_name="John", family_name="Doe", email="john@example.com"
    )

    with patch.object(
        service, "send_proprietary_period_extension_notification_to_salt_help"
    ) as mock_salt_help, patch.object(
        service, "send_proprietary_period_extension_notification_to_pc_and_pi"
    ) as mock_pc_pi:
        service.send_proprietary_period_extension_notification(
            proposal_code=proposal_code,
            user=user,
            proprietary_period=24,
            motivation="Need more time for analysis",
        )

        mock_salt_help.assert_called_once_with(
            proposal_code=proposal_code,
            proprietary_period=24,
            motivation="Need more time for analysis",
            user=user,
        )
        mock_pc_pi.assert_called_once_with(
            proposal_code=proposal_code,
            proprietary_period=24,
            motivation="Need more time for analysis",
            user=user,
        )


def test_send_proprietary_period_extension_notification_custom_salt_help(
    db_connection: Connection, monkeypatch: pytest.MonkeyPatch
) -> None:
    proposal_code = "2020-1-SCI-005"
    repo = ProposalRepository(db_connection)
    service = ProposalService(repo)
    user = _create_mock_user()

    custom_email = "custom_salthelp@example.com"
    monkeypatch.setenv("SALT_HELP_EMAIL", custom_email)

    with patch.object(MailService, "send_email"), patch.object(
        MailService, "generate_email", wraps=MailService.generate_email
    ) as mock_generate:
        service.send_proprietary_period_extension_notification_to_salt_help(
            proposal_code=proposal_code,
            user=user,
            proprietary_period=18,
            motivation="Motivation text",
        )

        salt_help_call = mock_generate.call_args_list[0].kwargs
        assert salt_help_call["to"] == custom_email


def test_create_proprietary_period_extension_request(
    db_connection: Connection,
) -> None:
    proposal_code = "2020-1-SCI-005"
    repo = ProposalRepository(db_connection)
    service = ProposalService(repo)
    user = _create_mock_user(given_name="Alice", family_name="Smith", username="asmith")

    with patch.object(
        repo, "insert_proprietary_period_extension_request"
    ) as mock_insert, patch.object(
        service, "send_proprietary_period_extension_notification_to_salt_help"
    ) as mock_salt_help, patch.object(
        service, "send_proprietary_period_extension_notification_to_pc_and_pi"
    ) as mock_pc_pi:
        service.create_proprietary_period_extension_request(
            proposal_code=proposal_code,
            proprietary_period=12,
            motivation="Need time",
            user=user,
        )

        mock_insert.assert_called_once_with(proposal_code, 12, "Need time", "asmith")
        mock_salt_help.assert_called_once_with(
            proposal_code=proposal_code,
            proprietary_period=12,
            motivation="Need time",
            user=user,
        )
        mock_pc_pi.assert_called_once_with(
            proposal_code=proposal_code,
            proprietary_period=12,
            motivation="Need time",
            user=user,
        )


def test_update_proprietary_period_in_ssda_success(
    db_connection: Connection,
) -> None:
    repo = ProposalRepository(db_connection)
    service = ProposalService(repo)
    proposal_code = "2020-1-SCI-005"

    mock_response = MagicMock()
    mock_response.json.return_value = {
        "data": {"updateReleaseDates": {"status": "SUCCESSFUL"}}
    }

    with patch.object(
        repo, "get_release_date", return_value="2022-01-01"
    ), patch(
        "saltapi.service.proposal_service.requests.post", return_value=mock_response
    ) as mock_post:
        service.update_proprietary_period_in_ssda(proposal_code, 24)
        mock_post.assert_called_once()


def test_update_proprietary_period_in_ssda_logs_and_raises_on_graphql_errors(
    db_connection: Connection,
) -> None:
    repo = ProposalRepository(db_connection)
    service = ProposalService(repo)
    proposal_code = "2020-1-SCI-005"

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

    with patch.object(
        repo, "get_release_date", return_value="2022-01-01"
    ), patch(
        "saltapi.service.proposal_service.requests.post", return_value=mock_response
    ), patch(
        "saltapi.service.proposal_service.logger"
    ) as mock_logger:
        with pytest.raises(SSDAError):
            service.update_proprietary_period_in_ssda(proposal_code, 24)

        assert mock_logger.error.call_count == 2
        logged_msgs = [call.args[0] for call in mock_logger.error.call_args_list]
        assert "Cannot update release dates" in logged_msgs[0]
        assert "FORBIDDEN" in logged_msgs[0]
        assert "Invalid proposal code" in logged_msgs[1]
        assert "updateReleaseDates" in logged_msgs[1]


def test_update_proprietary_period_in_ssda_logs_and_raises_on_request_exception(
    db_connection: Connection,
) -> None:
    repo = ProposalRepository(db_connection)
    service = ProposalService(repo)
    proposal_code = "2020-1-SCI-005"

    with patch.object(
        repo, "get_release_date", return_value="2022-01-01"
    ), patch(
        "saltapi.service.proposal_service.requests.post",
        side_effect=requests.exceptions.ConnectionError("Connection refused"),
    ), patch(
        "saltapi.service.proposal_service.logger"
    ) as mock_logger:
        with pytest.raises(SSDAError):
            service.update_proprietary_period_in_ssda(proposal_code, 24)

        mock_logger.error.assert_called_once()
        assert "Connection refused" in mock_logger.error.call_args[0][0]


def test_proposals_requesting_more_time(
    db_connection: Connection,
) -> None:
    repo = ProposalRepository(db_connection)
    service = ProposalService(repo)
    semester = "2026-1"
    expected = [
        {
            "proposal_code": "2020-2-MLT-007",
            "request_reason": "Need more time",
            "grant_reason": None,
            "granted_period": None,
            "made_at": "2026-04-01T09:36:07",
            "requester_name": "Natalie Matchett",
            "requester_email": "natmatch98@gmail.com",
            "requested_period": 36,
            "current_period": 24,
        }
    ]

    with patch.object(
        repo, "proposals_requesting_proprietary_period_extension", return_value=expected
    ) as mock_repo_method:
        result = service.proposals_requesting_proprietary_request_extension(semester)
        from saltapi.util import semester_start
        mock_repo_method.assert_called_once_with(semester_start(semester))
        assert result == expected