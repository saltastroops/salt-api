from datetime import datetime, timedelta
from typing import Any, Dict, Optional, cast

from fastapi import HTTPException, Request
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt
from starlette import status

from saltapi.exceptions import AuthenticationError, NotFoundError, ValidationError
from saltapi.repository.unit_of_work import UnitOfWork
from saltapi.repository.user_repository import UserRepository
from saltapi.service.authentication import AccessToken
from saltapi.service.user import User
from saltapi.settings import get_settings
from saltapi.util import validate_user

ALGORITHM = "HS256"
ACCESS_TOKEN_LIFETIME_HOURS = get_settings().auth_token_lifetime_hours
SECRET_KEY = get_settings().secret_key
VERIFICATION_KEY = get_settings().verification_key
USER_ID_KEY = "user_id"  # nosec
SECONDARY_AUTH_TOKEN_KEY = "secondary_auth_token"  # nosec


class AuthenticationService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    @staticmethod
    def access_token(
        user: User, token_lifetime_hours: Optional[int] = None
    ) -> AccessToken:
        """Generate an authentication token."""
        if token_lifetime_hours is not None:
            token_expires = timedelta(hours=token_lifetime_hours)
        else:
            token_expires = timedelta(hours=ACCESS_TOKEN_LIFETIME_HOURS)
        token = AuthenticationService.jwt_token(
            payload={"sub": str(user.id)},  # subject must be a string, not an integer
            expires_delta=token_expires,
        )

        token_type = "bearer"  # nosec
        return AccessToken(
            access_token=token,
            token_type=token_type,
            expires_at=datetime.now() + token_expires,
        )

    @staticmethod
    def jwt_token(
        payload: Dict[str, Any],
        expires_delta: Optional[timedelta] = None,
        verification: bool = False,
    ) -> str:
        """Create a JWT token."""
        to_encode = payload.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_LIFETIME_HOURS)
        to_encode["exp"] = expire
        secret_key = SECRET_KEY
        if verification:
            secret_key = VERIFICATION_KEY
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)

        return cast(str, encoded_jwt)

    def authenticate_user(self, username: str, password: str) -> User:
        user = self.user_repository.find_user_with_username_and_password(
            username, password
        )
        if not user:
            raise AuthenticationError("User not found.")
        return user

    def validate_auth_token(
        self, token: str, verification: bool = False
    ) -> Optional[User]:
        secret_key = SECRET_KEY
        if verification:
            secret_key = VERIFICATION_KEY
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        if not payload:
            raise JWTError("Token failed to decode.")

        return self.user_repository.get(payload["sub"])


def get_current_user(request: Request) -> User:
    authorization: Optional[str] = request.headers.get("Authorization")
    if authorization:
        user = _user_from_auth_header(authorization)
    else:
        user = _user_from_session(request)
    if not user:
        raise NotFoundError("Could not validate token.")
    validate_user(user)
    return user


def _user_from_auth_header(authorization: str, verification: bool = False) -> User:
    # Based on FastAPI's OAuth2PasswordBearer class
    scheme, token = get_authorization_scheme_param(authorization)
    if scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return find_user_from_token(token, verification)


def _user_from_session(request: Request) -> User:
    user_id = request.session.get(USER_ID_KEY)

    signed_auth_token = request.cookies.get(SECONDARY_AUTH_TOKEN_KEY)
    secondary_auth_token = jwt.decode(
        signed_auth_token, SECRET_KEY, algorithms=[ALGORITHM]
    )

    signed_auth_token_from_session = request.session.get(SECONDARY_AUTH_TOKEN_KEY)
    secondary_auth_token_from_session = jwt.decode(
        signed_auth_token_from_session, SECRET_KEY, algorithms=[ALGORITHM]
    )
    if (
        not user_id
        or not secondary_auth_token
        or secondary_auth_token != secondary_auth_token_from_session
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    with UnitOfWork() as unit_of_work:
        user_repository = UserRepository(unit_of_work.connection)
        return user_repository.get(user_id)


def find_user_from_token(token: str, verification: bool = False) -> Optional[User]:
    with UnitOfWork() as unit_of_work:
        user_repository = UserRepository(unit_of_work.connection)
        authentication_repository = AuthenticationService(user_repository)

        return authentication_repository.validate_auth_token(token, verification)


def get_user_to_verify(request: Request) -> User:
    try:
        authorization: Optional[str] = request.headers.get("Authorization")

        if not authorization:
            raise ValidationError("Failed to validate user.")

        user = _user_from_auth_header(authorization, verification=True)
        if not user:
            raise NotFoundError("User not found.")
        return user

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Couldn't validate validation token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
