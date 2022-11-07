from typing import List, Optional, cast

from saltapi.exceptions import AuthorizationError
from saltapi.repository.block_repository import BlockRepository
from saltapi.repository.proposal_repository import ProposalRepository
from saltapi.repository.user_repository import UserRepository
from saltapi.service.user import Role, User


class PermissionService:
    def __init__(
        self,
        user_repository: UserRepository,
        proposal_repository: ProposalRepository,
        block_repository: BlockRepository,
    ) -> None:
        self.user_repository = user_repository
        self.proposal_repository = proposal_repository
        self.block_repository = block_repository

    def user_has_role(
        self, username: str, proposal_code: Optional[str], role: Role
    ) -> bool:
        """
        Check whether the user has a role required to perform a specific
        action on a given proposal.
        """
        if role == Role.ADMINISTRATOR:
            return self.user_repository.is_administrator(username)

        elif role == Role.BOARD_MEMBER:
            return self.user_repository.is_board_member(username)

        elif role == Role.ENGINEER:
            return self.user_repository.is_engineer()

        elif role == Role.INVESTIGATOR:
            return self.user_repository.is_investigator(
                username, cast(str, proposal_code)
            )

        elif role == Role.PARTNER_AFFILIATED:
            return self.user_repository.is_partner_affiliated_user(username)

        elif role == Role.PRINCIPAL_CONTACT:
            return self.user_repository.is_principal_contact(
                username, cast(str, proposal_code)
            )

        elif role == Role.PRINCIPAL_INVESTIGATOR:
            return self.user_repository.is_principal_investigator(
                username, cast(str, proposal_code)
            )

        elif role == Role.PROPOSAL_TAC_CHAIR:
            return self.user_repository.is_tac_chair_for_proposal(
                username, cast(str, proposal_code)
            )

        elif role == Role.PROPOSAL_TAC_MEMBER:
            return self.user_repository.is_tac_member_for_proposal(
                username, cast(str, proposal_code)
            )

        elif role == Role.SALT_ASTRONOMER:
            return self.user_repository.is_salt_astronomer(username)

        elif role == Role.SALT_OPERATOR:
            return self.user_repository.is_salt_astronomer(username)

        elif role == Role.TAC_CHAIR:
            return self.user_repository.is_tac_chair_in_general(username)

        elif role == Role.TAC_MEMBER:
            return self.user_repository.is_tac_member_in_general(username)
        else:
            return False

    def check_permissions(
        self,
        username: str,
        proposal_code: Optional[str],
        permitted_user_roles: List[Role],
    ) -> None:
        """
        Check whether the user has permissions to perform a specific action
        on a given proposal.
        """
        has_permissions = []
        for role in permitted_user_roles:
            has_permission = self.user_has_role(username, proposal_code, role)
            has_permissions.append(has_permission)
        if not any(has_permissions):
            raise AuthorizationError()

    def check_permission_to_view_proposal(self, user: User, proposal_code: str) -> None:
        """
        Check whether the user may view a proposal.

        This is the case if the user is any of the following:

        * a SALT Astronomer
        * an investigator on the proposal
        * a TAC member for the proposal
        * an administrator
        """
        username = user.username
        proposal_type = self.proposal_repository.get_proposal_type(proposal_code)

        if proposal_type != "Gravitational Wave Event":
            permitted_roles = [
                Role.SALT_ASTRONOMER,
                Role.INVESTIGATOR,
                Role.PROPOSAL_TAC_MEMBER,
                Role.ADMINISTRATOR,
            ]
            self.check_permissions(username, proposal_code, permitted_roles)
        else:
            # Gravitational wave event proposals are a special case; they can be viewed
            # by anyone who belongs to a SALT partner.
            permitted_roles = [
                Role.SALT_ASTRONOMER,
                Role.PARTNER_AFFILIATED,
                Role.ADMINISTRATOR,
            ]

            self.check_permissions(username, proposal_code, permitted_roles)

    def check_permission_to_activate_proposal(
        self, user: User, proposal_code: str
    ) -> None:
        """
        Check whether the user may activate a proposal.

        This is the case if the user is any of the following:

        * the Principal Investigator (and the proposal can be activated by the PI or PC)
        * the Principal Contact (and the proposal can be activated by the PI or PC)
        * a SALT Astronomer
        * an administrator
        """
        username = user.username

        if self.proposal_repository.is_self_activatable(proposal_code):
            permitted_roles = [
                Role.PRINCIPAL_INVESTIGATOR,
                Role.PRINCIPAL_CONTACT,
                Role.SALT_ASTRONOMER,
                Role.ADMINISTRATOR,
            ]
            self.check_permissions(username, proposal_code, permitted_roles)
        else:
            permitted_roles = [Role.SALT_ASTRONOMER, Role.ADMINISTRATOR]
            self.check_permissions(username, proposal_code, permitted_roles)

    def check_permission_to_deactivate_proposal(
        self, user: User, proposal_code: str
    ) -> None:
        """
        Check whether the user may deactivate a proposal.

        This is the case if the user is any of the following:

        * the Principal Investigator
        * the Principal Contact
        * a SALT Astronomer
        * an administrator
        """
        username = user.username

        permitted_roles = [
            Role.PRINCIPAL_INVESTIGATOR,
            Role.PRINCIPAL_CONTACT,
            Role.SALT_ASTRONOMER,
            Role.ADMINISTRATOR,
        ]

        self.check_permissions(username, proposal_code, permitted_roles)

    def check_permission_to_update_proposal_status(self, user: User) -> None:
        """
        Check whether the user may update a proposal status.

        This is the case if the user is any of the following:

        * a SALT Astronomer
        * an administrator
        """
        username = user.username

        permitted_roles = [Role.SALT_ASTRONOMER, Role.ADMINISTRATOR]

        self.check_permissions(
            username=username, proposal_code=None, permitted_user_roles=permitted_roles
        )

    def check_permission_to_add_observation_comment(
        self, user: User, proposal_code: str
    ) -> None:
        """
        Checks if the user can add an observation comment

        This is the case if the user is any of the following:

        * a SALT Astronomer
        * a Principal Investigator
        * a Principal Contact
        * an administrator
        """
        username = user.username

        permitted_roles = [
            Role.PRINCIPAL_INVESTIGATOR,
            Role.PRINCIPAL_CONTACT,
            Role.SALT_ASTRONOMER,
            Role.ADMINISTRATOR,
        ]

        self.check_permissions(username, proposal_code, permitted_roles)

    def check_permission_to_view_observation_comments(
        self, user: User, proposal_code: str
    ) -> None:
        """
        Checks if the user may view the observation comments

        This is the case if the user may add observation comments.
        """
        self.check_permission_to_add_observation_comment(user, proposal_code)

    def check_permission_to_view_block(self, user: User, block_id: int) -> None:
        """
        Check whether the user may view a block.

        This is the case if the user may view the proposal which the block belongs to.
        """
        proposal_code: str = self.block_repository.get_proposal_code_for_block_id(
            block_id
        )

        self.check_permission_to_view_proposal(user, proposal_code)

    def check_permission_to_view_block_status(self, user: User, block_id: int) -> None:
        """
        Check whether the user may view a block status.

        This is the case if the user may view the block.
        """
        self.check_permission_to_view_block(user, block_id)

    def check_permission_to_update_block_status(self, user: User) -> None:
        """
        Check whether the user may view a block status.

        This is the case if the user may update a proposal status.
        """
        self.check_permission_to_update_proposal_status(user)

    def check_permission_to_view_block_visit(
        self, user: User, block_visit_id: int
    ) -> None:
        """
        Check whether the user may view a block visit.

        This is the case if the user may view the proposal for which the block visit
        was taken.
        """
        proposal_code: str = self.block_repository.get_proposal_code_for_block_visit_id(
            block_visit_id
        )

        self.check_permission_to_view_proposal(user, proposal_code)

    def check_permission_to_update_block_visit_status(self, user: User) -> None:
        """
        Check whether the user may update a block visit status.

        This is the case if the user may update a proposal status.
        """
        self.check_permission_to_update_proposal_status(user)

    def check_permission_to_view_user(self, user: User, updated_user_id: int) -> None:
        """
        Check whether the user may view a user.

        Administrators may view any users. Other users may only view their own user
        details.
        """
        if not user.id == updated_user_id:
            permitted_roles = [Role.ADMINISTRATOR]

            self.check_permissions(
                username=user.username,
                proposal_code=None,
                permitted_user_roles=permitted_roles,
            )

    def check_permission_to_update_user(self, user: User, updated_user_id: int) -> None:
        """
        Check whether the user may update a user.

        This is the case if the user may update a user.
        """
        self.check_permission_to_view_user(user, updated_user_id)

    def check_permission_to_view_mos_mask_metadata(self, user: User) -> None:
        """
        Check whether the user may view MOS mask data.

        Administrators and SALT Astronomers may view MOS data.
        details.
        """

        username = user.username

        permitted_roles = [Role.SALT_ASTRONOMER, Role.ADMINISTRATOR]

        self.check_permissions(
            username=username, proposal_code=None, permitted_user_roles=permitted_roles
        )

    def check_permission_to_update_mos_mask_metadata(self, user: User) -> None:
        """
        Check whether the user can update a MOS mask metadata.
        """
        username = user.username

        permitted_roles = [Role.SALT_ASTRONOMER, Role.ADMINISTRATOR, Role.ENGINEER]

        self.check_permissions(
            username=username, proposal_code=None, permitted_user_roles=permitted_roles
        )

    @staticmethod
    def check_user_has_role(user: User, role: Role) -> bool:
        if role in user.roles:
            return True
        return False

    def check_permission_to_update_proposal_progress(
        self, user: User, proposal_code: str
    ) -> None:
        """
        Check whether the user can update proposal progress details.
        """
        username = user.username

        permitted_roles = [
            Role.PRINCIPAL_INVESTIGATOR,
            Role.PRINCIPAL_CONTACT,
            Role.ADMINISTRATOR,
        ]

        self.check_permissions(username, proposal_code, permitted_roles)
