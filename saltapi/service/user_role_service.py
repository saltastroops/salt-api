from typing import List, Optional

from saltapi.repository.user_repository import UserRepository
from saltapi.service.user import Role


class UserRoleService:
    def __init__(
            self,
            user_repository: UserRepository,
            username: str,
            proposal_code: Optional[str],
    ):
        self.user_repository = user_repository
        self.username = username
        self.proposal_code = proposal_code

    def get_user_roles(self) -> List[Role]:
        """
        Get a user's roles.

        The roles do include roles which are specific to a particular proposal (such
        as Principal Investigator). Also, they include roles which are specific to a
        partner (i.e. TAC chair and member).
        """
        roles = []
        if self.user_repository.is_administrator(self.username):
            roles.append(Role.ADMINISTRATOR)

        if self.user_repository.is_salt_astronomer(self.username):
            roles.append(Role.SALT_ASTRONOMER)

        if self.user_repository.is_board_member(self.username):
            roles.append(Role.BOARD_MEMBER)

        if self.user_repository.is_tac_chair_in_general(self.username):
            roles.append(Role.TAC_CHAIR)

        if self.user_repository.is_tac_member_in_general(self.username):
            roles.append(Role.TAC_MEMBER)

        if self.user_repository.is_tac_member_for_proposal(
                self.username, self.proposal_code
        ):
            roles.append(Role.PROPOSAL_TAC_MEMBER)

        if self.user_repository.is_partner_affiliated_user(self.username):
            roles.append(Role.PARTNER_AFFILIATED)

        if self.user_repository.is_principal_investigator(
                self.username, self.proposal_code
        ):
            roles.append(Role.PRINCIPAL_INVESTIGATOR)

        if self.user_repository.is_principal_contact(
                self.username, self.proposal_code
        ):
            roles.append(Role.PRINCIPAL_CONTACT)

        if self.user_repository.is_investigator(
                self.username, self.proposal_code
        ):
            roles.append(Role.INVESTIGATOR)

        if self.user_repository.is_engineer():
            roles.append(Role.ENGINEER)

        return roles
