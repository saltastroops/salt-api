from typing import List

from saltapi.exceptions import AuthorizationError
from saltapi.repository.block_repository import BlockRepository
from saltapi.repository.proposal_repository import ProposalRepository
from saltapi.repository.user_repository import UserRepository
from saltapi.service.user import Role, User
from saltapi.service.user_role_service import UserRoleService


def has_permissions(user_roles: List[Role], permitted_user_roles: List[Role]) -> None:
    if not any(role in permitted_user_roles for role in user_roles):
        raise AuthorizationError()


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

        role_service = UserRoleService(self.user_repository, username, proposal_code)
        user_roles = role_service.get_user_roles()

        if proposal_type != "Gravitational Wave Event":
            permitted_roles = [
                Role.SALT_ASTRONOMER,
                Role.INVESTIGATOR,
                Role.PROPOSAL_TAC_MEMBER,
                Role.ADMINISTRATOR
            ]
            has_permissions(user_roles, permitted_roles)
        else:
            # Gravitational wave event proposals are a special case; they can be viewed
            # by anyone who belongs to a SALT partner.
            permitted_roles = [
                Role.SALT_ASTRONOMER,
                Role.PARTNER_AFFILIATED,
                Role.ADMINISTRATOR
            ]

            has_permissions(user_roles, permitted_roles)

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

        role_service = UserRoleService(self.user_repository, username, proposal_code)
        user_roles = role_service.get_user_roles()

        if self.proposal_repository.is_self_activatable(proposal_code):
            permitted_roles = [
                Role.PRINCIPAL_INVESTIGATOR,
                Role.PRINCIPAL_CONTACT,
                Role.SALT_ASTRONOMER,
                Role.ADMINISTRATOR
            ]
            has_permissions(user_roles, permitted_roles)
        else:
            permitted_roles = [
                Role.SALT_ASTRONOMER,
                Role.ADMINISTRATOR
            ]
            has_permissions(user_roles, permitted_roles)

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

        role_service = UserRoleService(self.user_repository, username, proposal_code)
        user_roles = role_service.get_user_roles()

        permitted_roles = [
            Role.PRINCIPAL_INVESTIGATOR,
            Role.PRINCIPAL_CONTACT,
            Role.SALT_ASTRONOMER,
            Role.ADMINISTRATOR
        ]

        has_permissions(user_roles, permitted_roles)

    def check_permission_to_update_proposal_status(self, user: User) -> None:
        """
        Check whether the user may update a proposal status.

        This is the case if the user is any of the following:

        * a SALT Astronomer
        * an administrator
        """
        username = user.username

        role_service = UserRoleService(self.user_repository, username, proposal_code=None)
        user_roles = role_service.get_user_roles()

        permitted_roles = [
            Role.SALT_ASTRONOMER,
            Role.ADMINISTRATOR
        ]

        has_permissions(user_roles, permitted_roles)

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

        role_service = UserRoleService(self.user_repository, username, proposal_code)
        user_roles = role_service.get_user_roles()

        permitted_roles = [
            Role.PRINCIPAL_INVESTIGATOR,
            Role.PRINCIPAL_CONTACT,
            Role.SALT_ASTRONOMER,
            Role.ADMINISTRATOR
        ]

        has_permissions(user_roles, permitted_roles)

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

    def check_permission_to_update_block_status(
        self, user: User, block_id: int
    ) -> None:
        """
        Check whether the user may view a block status.

        This is the case if the user is any of the following:

        * a SALT Astronomer
        * an administrator
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

        This is the case if the user is any of the following:

        * a SALT Astronomer
        * an administrator
        """
        self.check_permission_to_update_proposal_status(user)

    def check_permission_to_view_user(self, user: User, updated_user_id: int) -> None:
        """
        Check whether the user may update a user.

        Administrators may view any users. Other users may only view their own user
        details.
        """
        if not user.id == updated_user_id:
            role_service = UserRoleService(self.user_repository, user.username, proposal_code=None)
            user_roles = role_service.get_user_roles()

            permitted_roles = [
                Role.ADMINISTRATOR
            ]

            has_permissions(user_roles, permitted_roles)

    def check_permission_to_update_user(self, user: User, updated_user_id: int) -> None:
        """
        Check whether the user may update a user.

        Administrators may update any users. Other users may only update their own user
        details.
        """
        self.check_permission_to_view_user(user, updated_user_id)

    def check_permission_to_view_mos_metadata(self, user: User) -> None:
        """
        Check whether the user may view MOS data.

        Administrators and SALT Astronomers may view MOS data.
        details.
        """

        username = user.username

        role_service = UserRoleService(self.user_repository, username, proposal_code=None)
        user_roles = role_service.get_user_roles()

        permitted_roles = [
            Role.SALT_ASTRONOMER,
            Role.ADMINISTRATOR
        ]

        has_permissions(user_roles, permitted_roles)

    def check_permission_to_update_mos_mask_metadata(self, user: User) -> None:
        """
        Check whether the user can update a slit mask.
        """
        username = user.username

        role_service = UserRoleService(self.user_repository, username, proposal_code=None)
        user_roles = role_service.get_user_roles()

        permitted_roles = [
            Role.SALT_ASTRONOMER,
            Role.ADMINISTRATOR,
            Role.ENGINEER
        ]

        has_permissions(user_roles, permitted_roles)

    @staticmethod
    def check_user_has_role(user: User, role: Role) -> bool:
        if role in user.roles:
            return True
        return False

    def check_permission_to_update_proposal_progress(
        self, user: User, proposal_code: str
    ) -> None:
        """
        Check whether the user can update proposal progress.
        """
        username = user.username

        role_service = UserRoleService(self.user_repository, username, proposal_code)
        user_roles = role_service.get_user_roles()

        permitted_roles = [
            Role.PRINCIPAL_INVESTIGATOR,
            Role.PRINCIPAL_CONTACT,
            Role.ADMINISTRATOR
        ]

        has_permissions(user_roles, permitted_roles)
