import uuid
from typing import Callable

from fastapi import APIRouter, Body, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from saltapi.exceptions import AuthenticationError, ValidationError
from saltapi.repository.unit_of_work import UnitOfWork
from saltapi.service.authentication import AccessToken
from saltapi.service.authentication_service import (SECONDARY_AUTH_TOKEN_KEY,
                                                    USER_ID_KEY,
                                                    AuthenticationService,
                                                    get_current_user)
from saltapi.service.user import User
from saltapi.settings import get_settings
from saltapi.util import validate_user
from saltapi.web import services
from saltapi.web.schema.user import UserSwitchDetails

router = APIRouter(tags=["Authentication"])


def get_user_authentication_function() -> Callable[[str, str], User]:
    """
    Returns the function for authenticating a user by username and password.
    """

    def authenticate_user(username: str, password: str) -> User:
        with UnitOfWork() as unit_of_work:
            authentication_service = services.authentication_service(
                unit_of_work.connection
            )
            if username == "gw":
                raise AuthenticationError("User cannot be authenticated.")
            user = authentication_service.authenticate_user(username, password)
            return user

    return authenticate_user


@router.post(
    "/token",
    summary="Request an authentication token",
    response_description="An authentication token",
    response_model=AccessToken,
)
def token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    authenticate_user: Callable[[str, str], User] = Depends(
        get_user_authentication_function
    ),
) -> AccessToken:
    """
    Request an authentication token.

    The token returned can be used as an OAuth2 Bearer token for authenticating to the
    API. For example (assuming the token is `abcd1234`):

    ```shell
    curl -H "Authorization: Bearer abcd1234" /api/some/secret/resource
    ```
    The token is effectively a password; so keep it safe and don't share it.

    Note that the token expires 24 hours after being issued.
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise AuthenticationError("User not found")
    validate_user(user)
    return AuthenticationService.access_token(user)


def _login_user(user: User, request: Request) -> Response:
    secondary_auth_token = str(uuid.uuid4())
    request.session[USER_ID_KEY] = user.id
    request.session[SECONDARY_AUTH_TOKEN_KEY] = secondary_auth_token
    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    response.set_cookie(
        key=SECONDARY_AUTH_TOKEN_KEY,
        value=secondary_auth_token,
        httponly=False,
        max_age=3600 * get_settings().auth_token_lifetime_hours,
    )
    return response


@router.post("/login", summary="Log in", status_code=status.HTTP_204_NO_CONTENT)
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    authenticate_user: Callable[[str, str], User] = Depends(
        get_user_authentication_function
    ),
) -> Response:
    """
    Log in.

    Logging in means that two properties are added to the session's cookie:

    * The user id (with key "user_id").
    * A secondary authentication token (with key "secondary_auth_token").

    In addition, the secondary authentication token is stored in a cookie with the key
    "secondary_auth_token". This cookie is *not* HTTP-only. Both cookies must be present
    for authenticating a user, and their secondary authentication tokens must match.

    When logging out, a client should call the /logout endpoint and in addition delete
    the secondary authentication token cookie. The latter ensures that the user is
    logged out even if the call to the /logout endpoint fails.

    This approach was taken from
    https://medium.com/@thbrown/logging-out-with-http-only-session-ad09898876ba.
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise AuthenticationError("User not found.")
    validate_user(user)
    return _login_user(user, request)


@router.post("/logout", summary="Log out", status_code=status.HTTP_204_NO_CONTENT)
def logout(request: Request) -> Response:
    """
    Log out.

    Logging out means that the user id and the secondary authentication are removed from
    the session cookie (if they exist) and that the secondary authentication token
    cookie is deleted (if it exists).

    No error is raised if any of the cookie details don't exist.
    """
    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    if USER_ID_KEY in request.session:
        del request.session[USER_ID_KEY]
    if SECONDARY_AUTH_TOKEN_KEY in request.session:
        del request.session[SECONDARY_AUTH_TOKEN_KEY]
    if SECONDARY_AUTH_TOKEN_KEY in request.cookies:
        response.delete_cookie(SECONDARY_AUTH_TOKEN_KEY)
    return response


@router.post("/switch-user", summary="Switch the user")
def switch_user(
    request: Request,
    user_switch: UserSwitchDetails = Body(
        ..., title="User switch details", description="Details for switching the user"
    ),
    user: User = Depends(get_current_user),
) -> Response:
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_switch_user(user)

        if user_switch.username == "gw":
            raise AuthenticationError("You’re not allowed to switch to this user.")
        user_service = services.user_service(unit_of_work.connection)
        user = user_service.get_user_by_username(user_switch.username)
        if user is not None:
            return _login_user(user, request)
        raise ValidationError(f"Unknown username: {user_switch.username}")
