from datetime import timedelta
from typing import Any, Dict, List

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
            {"sub": str(user.id)}, timedelta(hours=1)
        )
        user_full_name = f"{user.given_name} {user.family_name}"

        password_reset_url = self.password_reset_url(reset_token)
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
    def password_reset_url(token: str) -> str:
        return get_settings().frontend_uri + "/change-password/" + token

    def get_user_roles(self, username: str) -> List[Role]:
        return self.repository.get_user_roles(username)

    def _does_user_exist(self, username: str) -> bool:
        try:
            self.get_user_by_username(username)
        except NotFoundError:
            return False

        return True

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

    def create_user(self, user: NewUserDetails) -> None:
        if self._does_user_exist(user.username):
            raise ValidationError(f"The username {user.username} exists already.")
        self._validate_user_statistics(vars(user))
        self.repository.create(vars(user))

    def get_user(self, user_id: int) -> User:
        user = self.repository.get(user_id)
        # Just in case the password hash ends up somewhere
        user.password_hash = "***"  # nosec
        return user

    def get_users(self) -> List[Dict[str, Any]]:
        users_details = self.repository.get_users()
        return users_details

    def get_user_by_email(self, email: str) -> User:
        user = self.repository.get_by_email(email)
        # Just in case the password hash ends up somewhere
        user.password_hash = "***"  # nosec
        return user

    def get_user_by_username(self, username: str) -> User:
        user = self.repository.get_by_username(username)
        # Just in case the password hash ends up somewhere
        user.password_hash = "***"  # nosec
        return user

    def update_user(self, user_id: int, user: Dict[str, Any]) -> None:
        self._validate_user_statistics(user)
        self.repository.update(user_id, user)

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
