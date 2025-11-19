from datetime import timedelta
from typing import Any, Dict, List, Optional

from saltapi.exceptions import (
    AuthorizationError,
    NotFoundError,
    SSDAError,
    ValidationError,
)
from saltapi.repository.user_repository import UserRepository
from saltapi.service.authentication_service import AuthenticationService
from saltapi.service.mail_service import MailService
from saltapi.service.user import NewUserDetails, Role, User
from saltapi.settings import get_settings
from saltapi.web.schema.user import ProposalPermissionType, Subscription, UserContact


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def send_password_reset_email(self, user: User) -> None:
        mail_service = MailService()
        authentication_service = AuthenticationService(self.repository)
        reset_token = authentication_service.jwt_token(
            {"sub": str(user.id)}, timedelta(hours=1), verification=True
        )
        user_full_name = f"{user.given_name} {user.family_name}"

        password_reset_url = self.password_reset_url(user.id, reset_token)
        plain_body = f"""Dear {user_full_name},

Someone (probably you) has requested to reset your SALT Web Manager password.

Please click on the link below to reset your password:

{password_reset_url}

Alternatively you can copy the link into the address bar of your browser.

If you have not requested to reset your password, you can just ignore this email.

Kind regards,

SALT Team
        """

        html_body = f"""
<html>
  <head></head>
  <body>
    <p>Dear {user_full_name},</p>
    <p>Someone (probably you) has requested to reset your SALT Web Manager password.</p>
    <p>Please click on the link below to reset your password:</p>
    <p><a href="{password_reset_url}">{password_reset_url}</a>.</p>
    <p>Alternatively you can copy the link into the address bar of your browser.</p>
    <p>If you have not requested to reset your password, you can just ignore this
    email.</p>
    <p>Kind regards,</p>
    <p>SALT Team</p>
  </body>
</html>
        """
        message = mail_service.generate_email(
            to=f"{user.given_name} {user.family_name} <{user.email}>",
            html_body=html_body,
            plain_body=plain_body,
            subject="SALT Web Manager password reset",
        )
        mail_service.send_email(to=[user.email], message=message)

    @staticmethod
    def password_reset_url(user_id: int, token: str) -> str:
        return get_settings().frontend_uri + f"/change-password/{user_id}/" + token

    def get_user_roles(self, username: str) -> List[Role]:
        return self.repository.get_user_roles(username)

    def _does_user_exist(self, username: str) -> bool:
        return self.get_user_by_username(username) is not None

    @staticmethod
    def _validate_user_statistics(user_details: Dict[str, Any]) -> None:
        if user_details["legal_status"] in [
            "South African citizen",
            "Permanent resident of South Africa",
        ]:
            if not user_details["gender"]:
                raise ValidationError("Gender is missing.")
            if not user_details["race"]:
                raise ValidationError("Race is missing.")
            if user_details["has_phd"] and not user_details["year_of_phd_completion"]:
                raise ValidationError("Year of completing PhD is missing.")

    def create_user(self, user: NewUserDetails) -> int:
        if self._does_user_exist(user.username):
            raise ValidationError(f"The username {user.username} exists already.")
        self._validate_user_statistics(vars(user))
        return self.repository.create(vars(user))

    def get_user(self, user_id: int) -> Optional[User]:
        user = self.repository.get(user_id)
        # Just in case the password hash ends up somewhere
        if user:
            # Just in case the password hash ends up somewhere
            user.password_hash = "***"  # nosec
        return user

    def get_user_details(self, user_id: int) -> Dict[str, Any]:
        user = self.repository.get_user_details(user_id)
        return user

    def get_users(self) -> List[Dict[str, Any]]:
        users_details = self.repository.get_users()
        return users_details

    def get_user_by_email(self, email: str) -> Optional[User]:
        user = self.repository.get_by_email(email)
        if user:
            # Just in case the password hash ends up somewhere
            user.password_hash = "***"  # nosec
        return user

    def get_user_by_username(self, username: str) -> Optional[User]:
        user = self.repository.get_by_username(username)
        if user:
            # Just in case the password hash ends up somewhere
            user.password_hash = "***"  # nosec
        return user

    def update_user(self, user_id: int, user: Dict[str, Any]) -> None:
        self._validate_user_statistics(user)
        self.repository.update(user_id, user)

    def update_password(self, user_id: int, password: str) -> None:
        self.repository.update_password(user_id, password)

    def get_salt_astronomers(self) -> List[Dict[str, Any]]:
        return self.repository.get_salt_astronomers()

    def get_proposal_permissions(self, user_id: int) -> List[Dict[str, Any]]:
        return self.repository.get_proposal_permissions(user_id)

    def grant_proposal_permission(
        self, user_id: int, permission_type: ProposalPermissionType, proposal_code: str
    ) -> None:
        if not self.repository.is_existing_user_id(user_id):
            raise NotFoundError(f"Unknown user id: {user_id}")

        # We know that the user exists and that the permission type is correct. So any
        # not found error must be due to an incorrect proposal code.
        try:
            self.repository.grant_proposal_permission(
                user_id=user_id,
                permission_type=permission_type.value,
                proposal_code=proposal_code,
            )
        except NotFoundError:
            raise ValidationError(f"Unknown proposal code: {proposal_code}")

    def revoke_proposal_permission(
        self, user_id: int, permission_type: ProposalPermissionType, proposal_code: str
    ) -> None:
        if not self.repository.is_existing_user_id(user_id):
            raise NotFoundError(f"Unknown user id: {user_id}")

        # We know that the user exists and that the permission type is correct. So any
        # not found error must be due to an incorrect proposal code.
        try:
            self.repository.revoke_proposal_permission(
                user_id=user_id,
                permission_type=permission_type.value,
                proposal_code=proposal_code,
            )

            return
        except NotFoundError:
            raise ValidationError(f"Unknown proposal code: {proposal_code}")

    def send_registration_confirmation_email(
        self, pipt_user_id: int, user_fullname: str, user_email: str
    ) -> None:
        mail_service = MailService()
        authentication_service = AuthenticationService(self.repository)
        confirmation_token = authentication_service.jwt_token(
            {"sub": str(pipt_user_id)}, timedelta(hours=3), verification=True
        )

        registration_confirmation_url = (
            get_settings().frontend_uri
            + "/verify-user/"
            + str(pipt_user_id)
            + "/"
            + confirmation_token
        )
        plain_body = f"""Dear {user_fullname},

It appears that someone (likely you) is registering to the SALT Web Manager.

To verify your email and complete the registration process, please click on the link below:

{registration_confirmation_url}

Alternatively, you can copy the link and paste it into the address bar of your browser.

Please note that this verification link will expire in 3 hours.

If you did not intend to register to the SALT Web Manager, please disregard this email.

Kind regards,

SALT Team
        """

        html_body = f"""
<html>
  <head></head>
  <body>
    <p>Dear {user_fullname},</p>
    <p>It appears that someone (likely you) is registering to the SALT Web Manager.</p>
    <p>To verify your email and complete the registration process, please click on the link below:</p>
    <p><a href="{registration_confirmation_url}">{registration_confirmation_url}</a>.</p>
    <p>Alternatively, you can copy the link and paste it into the address bar of your browser.</p>
    <p>Please note that this verification link will expire in 3 hours.</p>
    <p>If you did not intend to register to the SALT Web Manager, please disregard this email.</p>
    <p>Kind regards,</p>
    <p>SALT Team</p>
  </body>
</html>
        """

        message = mail_service.generate_email(
            to=f"{user_fullname} <{user_email}>",
            html_body=html_body,
            plain_body=plain_body,
            subject="SALT Web Manager User Verification",
        )
        mail_service.send_email(to=[user_email], message=message)

    def verify_user(self, user_id: int) -> None:
        self.repository.verify_user(user_id)

    def update_user_roles(self, user_id: int, new_roles: List[Role]) -> None:
        self.repository.update_user_roles(user_id, new_roles)

    def add_contact(self, user_id: int, contact: Dict[str, str]) -> int:
        new_email = contact["email"]
        existing_investigators = self.repository.get_user_emails(user_id)

        existing_contact = next(
            (email for email in existing_investigators if email["email"] == new_email),
            None,
        )

        investigator_id = self.repository.add_contact_details(user_id, contact)

        # Send validation only if email is new or existing but not yet validated
        if not existing_contact or existing_contact["pending"] != 0:
            validation_code = self.repository.generate_validation_code()
            self.repository.add_email_validation(investigator_id, validation_code)

        return investigator_id

    def get_validation_code_if_exists(self, investigator_id: int) -> Optional[str]:
        """
        Return the validation code if it exists, otherwise return None.
        """
        try:
            return self.get_email_validation_code(investigator_id)
        except ValueError:
            return None

    def update_subscriptions(
        self, user_id: int, subscriptions: List[Subscription]
    ) -> None:
        for subscription in subscriptions:
            if subscription.to == "Gravitational Wave Notifications":
                self.repository.subscribe_to_gravitational_wave_notifications(
                    user_id, subscription.is_subscribed
                )
            if subscription.to == "SALT News":
                self.repository.subscribe_to_salt_news(
                    user_id, subscription.is_subscribed
                )

    def get_subscriptions(self, user_id: int) -> List[Dict[str, Any]]:
        return self.repository.get_subscriptions(user_id)

    def set_preferred_email(
        self, user_id: int, email: str, investigator_id: int
    ) -> str:
        """
        Sets a user's preferred email.
        """
        emails = self.repository.get_user_emails(user_id)
        matching_email = next(
            (
                e
                for e in emails
                if e["email"] == email and e["investigator_id"] == investigator_id
            ),
            None,
        )

        if not matching_email:
            raise NotFoundError(
                f"No email '{email}' found for investigator {investigator_id}."
            )

        if matching_email["pending"] != 0:
            raise ValidationError(
                "You cannot set this email as preferred until it's validated."
            )

        self.repository.set_preferred_contact(user_id, investigator_id)
        return f"Preferred email successfully set to {email}"

    def get_email_validation_code(self, investigator_id: int) -> str:
        """Get validation code for a certain investigator id"""

        validation_code = self.repository.get_validation_code(investigator_id)
        if not validation_code:
            raise ValidationError("No validation code found for this investigator.")
        return validation_code

    def validate_email(self, validation_code: str) -> str:
        """Validate an email using its validation code."""
        investigator = self.repository.get_investigator_by_validation_code(
            validation_code
        )
        if not investigator:
            raise ValidationError("Invalid validation code.")

        investigator_id = investigator["Investigator_Id"]
        self.repository.clear_validation_code(investigator_id)

        email = investigator["Email"]
        user_id = investigator["PiptUser_Id"]
        user_emails = self.repository.get_user_emails(user_id)

        for other in user_emails:
            if other["email"] == email and other["pending"] != 0:
                self.repository.clear_validation_code(other["investigator_id"])

        return f"Email '{email}' successfully validated for all matching investigators."

    def resend_verification_email_for_contact(self, user_id: int, email: str) -> None:
        """
        Resend the verification email for an unvalidated contact.
        """
        contacts = self.repository.get_user_emails(user_id)

        contact = next((c for c in contacts if c["email"] == email), None)
        if not contact:
            raise NotFoundError(f"No contact found with email {email}")

        if contact.get("pending") != 1:
            raise ValidationError(f"The email {email} has already been validated.")

        investigator_id = contact["investigator_id"]

        validation_code = self.get_email_validation_code(investigator_id)

        affected_user = self.get_user(user_id)

        contact_info = {
            "given_name": affected_user.given_name,
            "family_name": affected_user.family_name,
            "email": contact["email"],
        }

        self.send_contact_verification_email(contact_info, validation_code)

    def create_contact(self, user_id: int, contact: UserContact) -> User:
        """Adding contact details and sending a verification email."""
        affected_user = self.get_user(user_id)
        if not affected_user:
            raise NotFoundError(f"User with ID {user_id} not found.")

        new_contact = dict(contact)
        new_contact["family_name"] = affected_user.family_name
        new_contact["given_name"] = affected_user.given_name
        try:
            investigator_id = self.add_contact(user_id, new_contact)

            validation_code = self.get_validation_code_if_exists(investigator_id)
            if validation_code:
                self.send_contact_verification_email(new_contact, validation_code)

        except (ValidationError, AuthorizationError, NotFoundError):
            raise
        except Exception as e:
            raise SSDAError(f"Failed to send verification email: {str(e)}")
        return self.get_user(user_id)

    def send_contact_verification_email(
        self,
        new_contact: Dict[str, str],
        validation_code: str,
    ) -> None:
        """
        Sends the verification email to a new contact.
        """
        mail_service = MailService()
        confirm_url = (
            f"{get_settings().frontend_uri}/verify-user-email/{validation_code}"
        )

        plain_body = f"""Dear {new_contact['given_name']} {new_contact['family_name']},

Thank you for using the SALT Web Manager!

A new investigator has been created for you.
  Name: {new_contact['given_name']} {new_contact['family_name']}
  Email: {new_contact['email']}

Please confirm your email address by pointing your browser to the following URL:
{confirm_url}

If you have any questions, please feel free to reply to this email.

Sincerely,
SALT Team
"""
        html_body = f"""
<html>
  <body>
    <p>Dear {new_contact['given_name']} {new_contact['family_name']},</p>
    <p>Thank you for using the SALT Web Manager!</p>
    <p>A new investigator has been created for you.</p>
    <ul>
      <li>Name: {new_contact['given_name']} {new_contact['family_name']}</li>
      <li>Email: {new_contact['email']}</li>
    </ul>
    <p>Please confirm your email address by pointing your browser to the following URL:</p>
    <p><a href="{confirm_url}">{confirm_url}</a></p>
    <p>If you have any questions, please feel free to reply to this email.</p>
    <p>Sincerely,</p>
    <p>SALT Team</p>
  </body>
</html>
"""
        message = mail_service.generate_email(
            to=(
                f"{new_contact['given_name']} {new_contact['family_name']} <{new_contact['email']}>"
            ),
            html_body=html_body,
            plain_body=plain_body,
            subject="SALT Web Manager Email Confirmation",
        )
        mail_service.send_email(to=[new_contact["email"]], message=message)
