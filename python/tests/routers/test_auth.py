from typing import Optional

import pytest
from _pytest.monkeypatch import MonkeyPatch
from aiomysql import Pool
from fastapi import status
from jose import jwt
from requests import Session

from app.models.general import User
from app.settings import Settings
from app.util import authentication
from app.util.authentication import ALGORITHM


@pytest.mark.parametrize(
    "username,password",
    [
        ("", ""),
        ("", "secret"),
        ("sipho", ""),
        ("pieter", "pieter-pw"),
        ("pieter", "pieter-pwt"),
        ("pieter", "pieter-pwdd"),
    ],
)
def test_token_for_incorrect_credentials(
    username: str, password: str, client: Session, monkeypatch: MonkeyPatch
) -> None:
    """Calling /api/token with incorrect credentials gives a 401 error."""

    async def mock_authenticate_user(
        username: str, password: str, db: Pool
    ) -> Optional[User]:
        if username + "-pwd" == password:
            return User(
                email="whoever@example.com",
                family_name="Doe",
                given_name="Jane",
                username=username,
            )
        return None

    monkeypatch.setattr(authentication, "authenticate_user", mock_authenticate_user)

    resp = client.post("/auth/token", data={"username": username, "password": password})

    assert resp.status_code in [
        status.HTTP_422_UNPROCESSABLE_ENTITY,  # missing username or password
        status.HTTP_401_UNAUTHORIZED,  # wrong username or password
    ]


def test_token_returns_authentication_token(
    client: Session, monkeypatch: MonkeyPatch, settings: Settings
) -> None:
    """/api/token returns a valid authentication token."""

    async def mock_authenticate_user(
        username: str, password: str, db: Pool
    ) -> Optional[User]:
        if username + "-pwd" == password:
            return User(
                email="jane@example.com",
                family_name="Doe",
                given_name="Jane",
                username=username,
            )
        return None

    monkeypatch.setattr(authentication, "authenticate_user", mock_authenticate_user)

    # request a token...
    resp = client.post("/auth/token", data={"username": "jane", "password": "jane-pwd"})
    token = resp.json()["access_token"]

    # ... and check that it is valid
    payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
    assert payload["sub"] == "jane"