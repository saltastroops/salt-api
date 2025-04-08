from datetime import timedelta
from typing import Any, Dict, List, Optional

from saltapi.exceptions import NotFoundError, ValidationError
from saltapi.repository.user_repository import UserRepository
from saltapi.service.authentication_service import AuthenticationService
from saltapi.service.mail_service import MailService
from saltapi.service.user import NewUserDetails, Role, User
from saltapi.settings import get_settings
from saltapi.web.schema.user import ProposalPermissionType


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

    def add_contact(self,user_id: int, contact: Dict[str, str]) -> None:
        user_details = self.get_user_details(user_id)
        contact["given_name"] = user_details["given_name"]
        contact["family_name"] = user_details["family_name"]
        investigator_id = self.repository.add_contact_details(user_id, contact)
        self.repository.set_preferred_contact(user_id, investigator_id)

    def subscribe_to_gw(self, user_id: int, subscribe: bool) -> None:
        self.repository.subscribe_to_gw(user_id, subscribe)

