from aiomysql import Pool
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies import get_db, get_settings
from app.models.general import AccessToken
from app.settings import Settings
from app.util import authentication

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/token",
    summary="Request an authentication token",
    response_description="An authentication token",
    response_model=AccessToken,
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    settings: Settings = Depends(get_settings),
    db: Pool = Depends(get_db),
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
    user = await authentication.authenticate_user(
        form_data.username, form_data.password, db
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return authentication.create_access_token(settings.secret_key, user)
