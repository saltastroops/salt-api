from typing import Any, Dict, List

from fastapi import APIRouter, Body, Depends, Path
from starlette import status

from saltapi.exceptions import NotFoundError
from saltapi.repository.unit_of_work import UnitOfWork
from saltapi.service.authentication_service import get_current_user, get_user_to_verify
from saltapi.service.user import NewUserDetails as _NewUserDetails, Role
from saltapi.service.user import User as _User
from saltapi.service.user import UserDetails as _UserDetails
from saltapi.service.user import UserUpdate as _UserUpdate
from saltapi.web import services
from saltapi.web.schema.common import Message
from saltapi.web.schema.user import (
    NewUserDetails,
    PasswordResetRequest,
    PasswordUpdate,
    ProposalPermission,
    User,
    UserListItem,
    UserUpdate,
    BaseUserDetails,
    UsernameEmail,
    UserContact,
)

router = APIRouter(prefix="/users", tags=["User"])


@router.post(
    "/send-password-reset-email",
    summary="Request an email with a password reset link to be sent.",
    response_description="Success message.",
    response_model=Message,
)
def send_password_reset_email(
    password_reset_request: PasswordResetRequest = Body(
        ..., title="Password reset request", description="Password reset request"
    ),
) -> Message:
    """
    Requests to send an email with a link for resetting the password. A username or
    email address needs to be supplied, and the email will be sent to the user with that
    username or email address.
    """
    with UnitOfWork() as unit_of_work:
        username_email = password_reset_request.username_email
        user_service = services.user_service(unit_of_work.connection)

        user = user_service.get_user_by_username(
            username_email
        ) or user_service.get_user_by_email(username_email)

        if not user:
            raise NotFoundError("User not found.")

        user_service.send_password_reset_email(user)

        return Message(message="Email with a password reset link sent.")


@router.post(
    "/",
    summary="Create a new user",
    status_code=status.HTTP_201_CREATED,
    response_model=User,
)
def create_user(
    user: NewUserDetails = Body(
        ..., title="User details", description="User details for the user to create."
    )
) -> _User:
    with UnitOfWork() as unit_of_work:
        user_service = services.user_service(unit_of_work.connection)
        pipt_user_id = user_service.create_user(
            _NewUserDetails(
                username=user.username,
                password=user.password,
                email=user.email,
                alternative_emails=[],
                given_name=user.given_name,
                family_name=user.family_name,
                institution_id=user.institution_id,
                legal_status=user.legal_status,
                race=user.race,
                gender=user.gender,
                has_phd=user.has_phd,
                year_of_phd_completion=user.year_of_phd_completion,
            )
        )

        # Now that the user has been added to the Database we need to confirm that the user provided a correct email
        # address.
        # Validate email
        user_service.send_registration_confirmation_email(
            pipt_user_id, f"{user.family_name} {user.given_name}", user.email
        )
        unit_of_work.commit()

        return user_service.get_user_by_username(user.username)


@router.get("/", summary="Get users information", response_model=List[UserListItem])
def get_users(
    user: _User = Depends(get_current_user),
) -> List[Dict[str, Any]]:
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_view_users(user)
        user_service = services.user_service(unit_of_work.connection)
        user = user_service.get_users()
        if user is None:
            raise NotFoundError("User Unknown.")
        return user


@router.post(
    "/send-verification-link",
    summary="Send a verification link.",
    response_model=Message,
)
def send_verification_link(
    username_email: UsernameEmail = Body(
        ..., title="Username or Email", description="Username or Email."
    ),
) -> Message:
    """
    Send verification link.
    """
    with UnitOfWork() as unit_of_work:

        user_service = services.user_service(unit_of_work.connection)

        user = user_service.get_user_by_username(
            username_email.username_email
        ) or user_service.get_user_by_email(username_email.username_email)
        if not user:
            raise NotFoundError()

        user_service.send_registration_confirmation_email(
            user.id, f"{user.family_name} {user.given_name}", user.email
        )

        return Message(message="Email with an activation link has been sent.")


@router.get("/{user_id}", summary="Get user details", response_model=User)
def get_user(
    user_id: int = Path(
        ...,
        title="User id",
        description="User id of the user making the request.",
    ),
    user: _User = Depends(get_current_user),
) -> _User:
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_update_user(user, user_id)
        user_service = services.user_service(unit_of_work.connection)
        user = user_service.get_user(user_id)
        if user is None:
            raise NotFoundError("Unknown user.")
        return user


@router.patch(
    "/{user_id}", summary="Update user details", response_model=BaseUserDetails
)
def update_user(
    user_id: int = Path(
        ...,
        title="User id",
        description="Id of the user to update.",
    ),
    user_update: UserUpdate = Body(
        ..., title="User Details", description="User details to update"
    ),
    user: _User = Depends(get_current_user),
) -> _UserDetails:
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_update_user(user, user_id)
        _user_update = _UserUpdate(
            email=user_update.email,
            family_name=user_update.family_name,
            given_name=user_update.given_name,
            password=user_update.password,
            legal_status=user_update.legal_status,
            gender=user_update.gender,
            race=user_update.race,
            has_phd=user_update.has_phd,
            year_of_phd_completion=user_update.year_of_phd_completion,
        )
        user_service = services.user_service(unit_of_work.connection)
        user_service.update_user(user_id, vars(_user_update))

        unit_of_work.commit()

        updated_user_details = user_service.get_user_details(user_id)

        return _UserDetails(**updated_user_details)


@router.get(
    "/{user_id}/proposal-permissions",
    summary="Get proposal permissions",
    response_model=List[ProposalPermission],
)
def get_proposal_permissions(
    user_id: int = Path(
        ...,
        title="User id",
        description="Id of the user",
    ),
    user: _User = Depends(get_current_user),
) -> List[Dict[str, Any]]:
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_view_user(user, user_id)
        user_service = services.user_service(unit_of_work.connection)

        return user_service.get_proposal_permissions(user_id)


@router.post(
    "/{user_id}/grant-proposal-permission",
    summary="Grant a proposal permission",
    response_model=ProposalPermission,
)
def grant_proposal_permission(
    user_id: int = Path(
        ...,
        title="User id",
        description="Id of the user to whom the permission is granted",
    ),
    permission: ProposalPermission = Body(
        ..., title="Permission", description="The permission to grant"
    ),
    user: _User = Depends(get_current_user),
) -> ProposalPermission:
    """
    Grant a proposal permission to a user.

    In case of success, the response contains the granted permission.
    """
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_grant_user_permissions(
            user, permission.proposal_code
        )
        user_service = services.user_service(unit_of_work.connection)
        user_service.grant_proposal_permission(
            user_id=user_id,
            proposal_code=permission.proposal_code,
            permission_type=permission.permission_type,
        )

        unit_of_work.commit()

        # Querying the database for the permission is somewhat pointless, so we just
        # return the permission submitted by the user.
        return permission


@router.post(
    "/{user_id}/revoke-proposal-permission",
    summary="Revoke a proposal permission",
    response_model=ProposalPermission,
)
def revoke_proposal_permission(
    user_id: int = Path(
        ...,
        title="User id",
        description="Id of the user for whom the permission is revoked",
    ),
    permission: ProposalPermission = Body(
        ..., title="Permission", description="The permission to revoke"
    ),
    user: _User = Depends(get_current_user),
) -> ProposalPermission:
    """
    Revoke a proposal permission from a user.

    In case of success, the response contains the revoked permission.
    """
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_grant_user_permissions(
            user, permission.proposal_code
        )
        user_service = services.user_service(unit_of_work.connection)
        user_service.revoke_proposal_permission(
            user_id=user_id,
            proposal_code=permission.proposal_code,
            permission_type=permission.permission_type,
        )

        unit_of_work.commit()

        # Querying the database for the permission is somewhat pointless, so we just
        # return the permission submitted by the user.
        return permission


@router.post(
    "/{user_id}/update-password", summary="Update user's password", response_model=User
)
def update_password(
    user_id: int = Path(
        ...,
        title="User id",
        description="Id for whom the password is updated",
    ),
    password_update: PasswordUpdate = Body(
        ...,
        title="Password and authentication token",
        description="Password to replace the old one, and an authentication token to verify the user.",
    ),
) -> _User:
    """
    Update user's password.
    """
    with UnitOfWork() as unit_of_work:
        authentication_service = services.authentication_service(
            unit_of_work.connection
        )
        user = authentication_service.validate_auth_token(
            password_update.authentication_key, verification=True
        )
        if not user:
            raise NotFoundError("Unknown user.")

        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_update_user(user, user_id)

        user_service = services.user_service(unit_of_work.connection)
        user_service.update_password(user_id, password_update.password)

        unit_of_work.commit()
        user = user_service.get_user(user_id)
        return user


@router.post("/{user_id}/verify-user", summary="Verify user", response_model=User)
def verify_user(
    user_id: int = Path(
        ...,
        title="User id",
        description="Id for user to verify",
    ),
    user: _User = Depends(get_user_to_verify),
) -> _User:
    """
    Verify user
    """
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_validate_user(user_id, user)
        user_service = services.user_service(unit_of_work.connection)
        user_service.verify_user(user_id)

        unit_of_work.commit()

        return user_service.get_user(user_id)


@router.post(
    "/{user_id}/update-roles", summary="Update user roles", response_model=User
)
def update_user_roles(
    user_id: int = Path(
        ..., title="User id", description="Id for user to update rights for."
    ),
    user: _User = Depends(get_current_user),
    roles: List[Role] = Body(
        ..., title="User Roles", description="User roles to update."
    ),
) -> User:
    """
    Update user's roles.
    """
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_update_user_roles(user)

        user_service = services.user_service(unit_of_work.connection)
        user_service.update_user_roles(user_id, roles)

        unit_of_work.commit()
        user = user_service.get_user(user_id)
        return user


@router.post(
    "/{user_id}/add-contact", summary="Add user's contact", response_model=User
)
def add_contact(
        user_id: int = Path(
            ..., title="User id", description="Id for user to add contact for."
        ),
        user: _User = Depends(get_current_user),
        contact: UserContact = Body(
            ..., title="User Contact", description="User contact to add."
        ),
) -> User:
    """
    Add user contact.
    """
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_add_user_contact(user_id, user)

        user_service = services.user_service(unit_of_work.connection)
        user = user_service.add_contact(user_id, vars(contact))
        if not user:
            raise NotFoundError("Unknown user.")
        unit_of_work.commit()
        return user