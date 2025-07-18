import re
from typing import Any, Dict, List, Optional, cast

from fastapi import Request

from saltapi.exceptions import AuthorizationError, ValidationError
from saltapi.repository.block_repository import BlockRepository
from saltapi.repository.proposal_repository import ProposalRepository
from saltapi.repository.submission_repository import SubmissionRepository
from saltapi.repository.user_repository import UserRepository
from saltapi.repository.utils import Utils
from saltapi.service.user import Role, User
from saltapi.settings import get_settings
from saltapi.web.schema.proposal import (
    ProposalStatusValue,
    ProprietaryPeriodUpdateRequest,
)


class PermissionService:
    def __init__(
        self,
        user_repository: UserRepository,
        proposal_repository: ProposalRepository,
        block_repository: BlockRepository,
        submission_repository: SubmissionRepository,
        utils: Utils,
    ) -> None:
        self.user_repository = user_repository
        self.proposal_repository = proposal_repository
        self.block_repository = block_repository
        self.submission_repository = submission_repository
        self.utils = utils

    def user_has_role(
        self,
        username: str,
        role: Optional[Role] = None,
        proposal_code: Optional[str] = None,
    ) -> bool:
        """
        Check that the user has a role required to perform a specific
        action on a given proposal.
        """
        if role == Role.ADMINISTRATOR:
            return self.user_repository.is_administrator(username)

        elif role == Role.BOARD_MEMBER:
            return self.user_repository.is_board_member(username)

        elif role == Role.ENGINEER:
            return self.user_repository.is_engineer()

        elif role == Role.LIBRARIAN:
            return self.user_repository.is_librarian(username)

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
            return self.user_repository.is_salt_operator(username)

        elif role == Role.TAC_CHAIR:
            return self.user_repository.is_tac_chair_in_general(username)

        elif role == Role.TAC_MEMBER:
            return self.user_repository.is_tac_member_in_general(username)
        else:
            return False

    def check_role(
        self,
        username: str,
        roles: List[Role],
        proposal_code: Optional[str] = None,
    ) -> None:
        """
        Check that the user has at least one of a given list of roles.
        """
        has_role = False
        for role in roles:
            if self.user_has_role(username, role, proposal_code):
                has_role = True
                break
        if not has_role:
            raise AuthorizationError()

    def check_permission_to_view_proposal(self, user: User, proposal_code: str) -> None:
        """
        Check that the user may view a proposal.

        This is the case if the user is any of the following:

        * a SALT Astronomer
        * an investigator on the proposal
        * a TAC member for the proposal
        * an administrator
        * a user who has been granted permission

        Gravitational wave proposals are a special case; they can be viewed by anyone
        belonging to a SALT partner.
        """
        username = user.username
        try:
            proposal_type = self.proposal_repository.get_proposal_type(proposal_code)

            if proposal_type != "Gravitational Wave Event":
                roles = [
                    Role.SALT_ASTRONOMER,
                    Role.SALT_OPERATOR,
                    Role.INVESTIGATOR,
                    Role.PROPOSAL_TAC_MEMBER,
                    Role.ADMINISTRATOR,
                    Role.LIBRARIAN,
                ]
                self.check_role(username, roles, proposal_code)
            else:
                # Gravitational wave event proposals are a special case; they can be
                # viewed by anyone who belongs to a SALT partner.
                roles = [
                    Role.SALT_ASTRONOMER,
                    Role.SALT_OPERATOR,
                    Role.PARTNER_AFFILIATED,
                    Role.ADMINISTRATOR,
                    Role.LIBRARIAN,
                ]

                self.check_role(username, roles, proposal_code)
        except AuthorizationError:
            try:
                # Granting a proposal view permission should be the exception rather
                # than the norm. We therefore only check for it (and incur an additional
                # database query) if the user doesn't have the permission to view the
                # proposal because of one of their roles already.
                if self.user_repository.user_has_proposal_permission(
                    user_id=user.id, permission_type="View", proposal_code=proposal_code
                ):
                    return
            except Exception:
                raise AuthorizationError()
            raise

    def check_permission_to_submit_proposal(
        self, user: User, proposal_code: Optional[str]
    ) -> None:
        """
        Check that the user may submit a proposal.

        This is the case if this is new submission rather than a resubmission of if the
        user is any of the following:

        * a SALT Astronomer
        * an administrator
        * a Principal Investigator or Principal Contact of the proposal
        """
        if proposal_code.startswith("Unsubmitted"):
            return
        username = user.username
        if self.user_has_role(
            username, Role.PRINCIPAL_CONTACT, proposal_code
        ) or self.user_has_role(username, Role.PRINCIPAL_INVESTIGATOR, proposal_code):
            return

        roles = [Role.SALT_ASTRONOMER, Role.ADMINISTRATOR]
        self.check_role(username, roles)

    def check_permission_to_view_submission_progress(
        self, user: User, submission: Dict[str, Any]
    ):
        submitter_id = submission["submitter_id"]
        if submitter_id != user.id:
            raise AuthorizationError()

    def check_permission_to_update_proposal_status(
        self, user: User, proposal_code: str, proposal_status: str
    ) -> None:
        """
        Check that the user may update a proposal status.

        This is the case if the user is any of the following:

        * a SALT Astronomer
        * an administrator
        * a Principal Investigator or Principal Contact (if the proposal is deactivated
          or if it is activated and self-activation is allowed)
        """
        username = user.username
        if self.user_has_role(
            username, Role.PRINCIPAL_CONTACT, proposal_code
        ) or self.user_has_role(username, Role.PRINCIPAL_INVESTIGATOR, proposal_code):
            if proposal_status == ProposalStatusValue.INACTIVE or (
                self.proposal_repository.is_self_activatable(proposal_code)
                and proposal_status == ProposalStatusValue.ACTIVE
            ):
                return
            raise AuthorizationError()

        roles = [Role.SALT_ASTRONOMER, Role.ADMINISTRATOR]
        self.check_role(username, roles)

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

        roles = [
            Role.PRINCIPAL_INVESTIGATOR,
            Role.PRINCIPAL_CONTACT,
            Role.SALT_ASTRONOMER,
            Role.ADMINISTRATOR,
        ]

        self.check_role(username, roles, proposal_code)

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
        Check that the user may view a block.

        This is the case if the user may view the proposal which the block belongs to.
        """
        proposal_code: str = self.block_repository.get_proposal_code_for_block_id(
            block_id
        )

        self.check_permission_to_view_proposal(user, proposal_code)

    def check_permission_to_view_block_status(self, user: User, block_id: int) -> None:
        """
        Check that the user may view a block status.

        This is the case if the user may view the block.
        """
        self.check_permission_to_view_block(user, block_id)

    def check_permission_to_update_block_status(
        self, user: User, block_id: int
    ) -> None:
        """
        Check that the user may view a block status.

        This is the case if the user is any of the following:

        * a SALT Astronomer
        * a Principal Investigator
        * a Principal Contact
        * an administrator
        """
        username = user.username

        proposal_code: str = self.block_repository.get_proposal_code_for_block_id(
            block_id
        )

        roles = [
            Role.PRINCIPAL_INVESTIGATOR,
            Role.PRINCIPAL_CONTACT,
            Role.SALT_ASTRONOMER,
            Role.ADMINISTRATOR,
        ]

        self.check_role(username, roles, proposal_code)

    def check_permission_to_view_block_visit(
        self, user: User, block_visit_id: int
    ) -> None:
        """
        Check that the user may view a block visit.

        This is the case if the user may view the proposal for which the block visit
        was taken.
        """
        proposal_code: str = self.block_repository.get_proposal_code_for_block_visit_id(
            block_visit_id
        )

        self.check_permission_to_view_proposal(user, proposal_code)

    def check_permission_to_update_block_visit_status(self, user: User) -> None:
        """
        Check that the user may update a block visit status.

        This is the case if the user is any of the following:

        * a SALT Astronomer
        * an administrator
        """
        username = user.username

        roles = [Role.SALT_ASTRONOMER, Role.ADMINISTRATOR]

        self.check_role(username, roles)

    def check_permission_to_view_user(self, user: User, viewed_user_id: int) -> None:
        """
        Check that the user may view a user.

        Administrators may view any users. Other users may only view their own user
        details.
        """
        if not user.id == viewed_user_id:
            self._check_user_is_admin(user)

    def check_permission_to_switch_user(self, user: User) -> None:
        """
        Check that the user may switch the user, i.e. login as someone else.

        This is the case if the user is an administrator.
        """
        self._check_user_is_admin(user)

    def check_permission_to_view_users(self, user: User) -> None:
        """
        Check that the user may view the list of users.

        This is the case if the user is an administrator.
        """
        self._check_user_is_admin(user)

    def check_permission_to_update_user(self, user: User, updated_user_id: int) -> None:
        """
        Check that the user may update a user.

        This is the case if the user may view the user.
        """
        self.check_permission_to_view_user(user, updated_user_id)

    def check_permission_to_view_mos_mask_metadata(self, user: User) -> None:
        """
        Check that the user may view MOS mask data.

        This is the case if the user is any of the following:

        * a SALT Astronomer
        * an administrator
        * an engineer
        """

        username = user.username

        roles = [Role.SALT_ASTRONOMER, Role.ADMINISTRATOR, Role.ENGINEER]

        self.check_role(username, roles)

    def check_permission_to_update_mos_mask_metadata(self, user: User) -> None:
        """
        Check that the user can update MOS mask metadata.
        """
        username = user.username

        roles = [Role.SALT_ASTRONOMER, Role.ADMINISTRATOR, Role.ENGINEER]

        self.check_role(username, roles)

    def check_permission_to_view_obsolete_masks_in_magazine(self, user: User) -> None:
        """
        Check that the user can view the obsolete masks in the magazine.
        """

        roles = [Role.SALT_ASTRONOMER, Role.ADMINISTRATOR, Role.ENGINEER]

        self.check_role(user.username, roles)

    def check_permission_to_view_rss_masks(self, user: User) -> None:
        """
        Check that the user can view the RSS slit masks.
        """

        roles = [Role.SALT_ASTRONOMER, Role.ADMINISTRATOR, Role.ENGINEER]

        self.check_role(user.username, roles)

    @staticmethod
    def check_user_has_role(user: User, role: Role) -> bool:
        if role in user.roles:
            return True
        return False

    def check_permission_to_update_proposal_progress(
        self, user: User, proposal_code: str
    ) -> None:
        """
        Check that the user can update proposal progress details.
        """
        username = user.username

        roles = [
            Role.PRINCIPAL_INVESTIGATOR,
            Role.PRINCIPAL_CONTACT,
            Role.ADMINISTRATOR,
        ]

        self.check_role(username, roles, proposal_code)

    def check_permission_to_view_currently_observed_block(self, user: User) -> None:
        """
        Check that the user may view the currently observed block.

        This is the case if the user is any of the following:

        * a SALT Astronomer
        * a SALT Operator
        * an administrator
        """
        username = user.username

        roles = [
            Role.SALT_ASTRONOMER,
            Role.SALT_OPERATOR,
            Role.ADMINISTRATOR,
        ]

        self.check_role(username, roles)

    def check_permission_to_view_scheduled_block(self, user: User) -> None:
        """
        Check that the user may view the next scheduled block.

        This is the case if the user may view the currently observed block.
        """

        self.check_permission_to_view_currently_observed_block(user)

    def check_permission_to_update_proprietary_period(
        self, user: User, proposal_code: str
    ) -> None:
        username = user.username
        roles = [
            Role.PRINCIPAL_INVESTIGATOR,
            Role.PRINCIPAL_CONTACT,
            Role.ADMINISTRATOR,
        ]
        self.check_role(username, roles, proposal_code)

    def check_permission_to_grant_user_permissions(
        self, user: User, proposal_code: str
    ) -> None:
        """
        Check that the user is allowed to grant permissions for a proposal to a user (or
        revoke them).

        This is the case if the user is the Principal Investigator, the Principal
        Contact, a SALT Astronomer or an administrator.
        """
        username = user.username
        roles = [
            Role.PRINCIPAL_INVESTIGATOR,
            Role.PRINCIPAL_CONTACT,
            Role.SALT_ASTRONOMER,
            Role.ADMINISTRATOR,
        ]
        self.check_role(username, roles, proposal_code)

    def is_motivation_needed_to_update_proprietary_period(
        self,
        proposal: Dict[str, Any],
        proprietary_period_update: ProprietaryPeriodUpdateRequest,
        username: str,
    ) -> bool:
        proposal_code = proposal["proposal_code"]
        if self.user_has_role(
            username, Role.ADMINISTRATOR, proposal_code
        ) and not self.user_has_role(username, Role.INVESTIGATOR, proposal_code):
            return False

        maximum_period = self.proposal_repository.maximum_proprietary_period(
            proposal_code
        )
        return maximum_period <= proprietary_period_update.proprietary_period

    def _check_user_is_admin(self, user: User) -> None:
        roles = [Role.ADMINISTRATOR]

        self.check_role(
            username=user.username,
            roles=roles,
        )

    def check_permission_to_change_self_activatable(self, user: User) -> None:
        roles = [Role.SALT_ASTRONOMER, Role.ADMINISTRATOR]
        self.check_role(user.username, roles)

    def check_permission_to_update_liaison_astronomer(self, user: User) -> None:
        roles = [Role.SALT_ASTRONOMER, Role.ADMINISTRATOR]
        self.check_role(user.username, roles)

    def check_permission_to_update_investigator_proposal_approval_status(
        self, user: User, approval_user_id: int, proposal_code: str
    ) -> None:
        # Investigators can always change their own approval status,
        # but changing someone else's status requires administrator rights
        roles = [Role.ADMINISTRATOR]
        if user.id != approval_user_id:
            self.check_role(user.username, roles, proposal_code)

    def check_permission_to_request_data(
        self, user: User, proposal_code: str, block_visit_ids: List[int]
    ) -> None:
        roles = [
            Role.ADMINISTRATOR,
            Role.SALT_ASTRONOMER,
            Role.PRINCIPAL_INVESTIGATOR,
            Role.PRINCIPAL_CONTACT,
            Role.INVESTIGATOR,
        ]
        self.check_role(user.username, roles, proposal_code)
        proposal_block_visit_ids = [
            bv["id"] for bv in self.proposal_repository.block_visits(proposal_code)
        ]

        for bv_id in block_visit_ids:
            if bv_id not in proposal_block_visit_ids:
                # Raising a validation error in a permission check may seem odd.
                # However, it must be part of permission checking to ensure that the
                # user is allowed to request all the block visit ids, and the easiest
                # way to do this is to check that they all belong to the requested
                # proposal code.
                raise ValidationError(
                    f"There exists no observation with id {bv_id} "
                    f"for the proposal {proposal_code}."
                )

    def check_permission_to_update_telescope_status(self, request: Request):
        host = request.client.host
        if not re.match(get_settings().allow_status_update_origin_regex, host):
            raise AuthorizationError(
                f"You may not update the status from this ip address: {host}"
            )

    def check_permission_to_validate_user(self, user_id: int, user: User) -> None:
        if self.check_user_has_role(user, Role.ADMINISTRATOR):
            return
        if user_id != user.id:
            raise ValidationError(f"You can't validate user with user ID {user_id}.")

    def check_permission_to_update_user_roles(self, user: User) -> None:
        if self.check_user_has_role(user, Role.ADMINISTRATOR):
            return

        raise AuthorizationError(f"You are not allowed update user roles.")

    def check_permission_to_add_user_contact(self, user_id: int, user: User):
        if self.check_user_has_role(user, Role.ADMINISTRATOR):
            return
        if user_id == user.id:
            return

        raise AuthorizationError("You are not allowed to add a contact to this user")

    def check_permission_to_subscribe_to_gravitational_wave_notifications(
        self, user_id: int, user: User, subscribe: bool
    ):
        if self.check_user_has_role(user, Role.ADMINISTRATOR):
            return
        if user_id == user.id:
            if not subscribe:
                return
            else:
                for affiliation in user.affiliations:
                    if affiliation.partner_code in self.utils.all_partners():
                        return
                raise AuthorizationError(
                    "You aren't allowed to subscribe as you aren't affiliated with a"
                    " SALT partner."
                )
        raise AuthorizationError(
            "You are not allowed to subscribe or unsubscribe another user."
        )

    def check_permission_to_subscribe_to_salt_news(self, user_id: int, user: User):
        if self.check_user_has_role(user, Role.ADMINISTRATOR) or user_id == user.id:
            return
        raise AuthorizationError(
            "You are not allowed to subscribe or unsubscribe another user."
        )

    def check_permission_to_view_subscriptions(self, user_id, user):
        if self.check_user_has_role(user, Role.ADMINISTRATOR) or user_id == user.id:
            return
        raise AuthorizationError("You are not allowed view the subscriptions.")
