import os
import uuid

import dotenv

# Make sure that the test database etc. are used.
# IMPORTANT: These lines must be executed before any server-related package is imported.

os.environ["DOTENV_FILE"] = ".env.test"
dotenv.load_dotenv(os.environ["DOTENV_FILE"])


from pathlib import Path
from typing import Any, Callable, Dict, Generator, Optional, cast

import pytest
import yaml
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection, Engine

import saltapi.web.api.authentication
from saltapi.exceptions import NotFoundError
from saltapi.main import app
from saltapi.repository.user_repository import UserRepository
from saltapi.service.user import User
from saltapi.service.user_service import UserService


def get_user_authentication_function() -> Callable[[str, str], User]:
    def authenticate_user(username: str, password: str) -> User:
        if password != USER_PASSWORD:
            raise NotFoundError("No user found for username and password")

        with cast(Engine, _create_engine()).connect() as connection:
            user_repository = UserRepository(connection)
            user_service = UserService(user_repository)
            user = user_service.get_user_by_username(username)
            return user

    return authenticate_user


app.dependency_overrides[
    saltapi.web.api.authentication.get_user_authentication_function
] = get_user_authentication_function


TEST_DATA = "users.yaml"


# Replace the user authentication with one which assumes that every user has the
# password "secret".

USER_PASSWORD = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_LIFETIME_HOURS = 7 * 24


def _create_engine():
    sdb_dsn = os.environ.get("SDB_DSN")
    if sdb_dsn:
        echo_sql = True if os.environ.get("ECHO_SQL") else False  # SQLAlchemy needs a bool
        return create_engine(sdb_dsn, echo=echo_sql, future=True)
    else:
        raise ValueError(
            "No SDB_DSN environment variable set"
        )


@pytest.fixture(scope="function")
def db_connection() -> Generator[Connection, None, None]:
    with _create_engine().connect() as connection:
        yield connection


def read_testdata(path: str) -> Any:
    if Path(path).is_absolute():
        raise ValueError("The file path must be a relative path.")

    root_dir = Path(os.environ["TEST_DATA_DIR"])
    datafile = root_dir / path
    if not datafile.exists():
        raise FileNotFoundError(f"File does not exist: {datafile}")

    with open(datafile, "r") as f:
        return yaml.safe_load(f)


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    yield TestClient(app)


def find_username(
    user_type: str,
    proposal_code: Optional[str] = None,
    partner_code: Optional[str] = None,
) -> str:
    """
    Find the username of a user who has a given user type.

    Depending on the user type, a proposal code or partner code must be supplied.
    """
    normalized_user_type = user_type.lower()
    normalized_user_type = normalized_user_type.replace(" ", "_").replace("-", "_")

    users = read_testdata(TEST_DATA)

    if normalized_user_type in [
        "investigator",
        "principal_investigator",
        "principal_contact",
    ]:
        if proposal_code is None:
            raise ValueError(f"Proposal code missing for user type {user_type}")
        return cast(str, users[normalized_user_type + "s"][proposal_code])

    if normalized_user_type in ["tac_chair", "tac_member"]:
        if partner_code is None:
            raise ValueError(f"Partner code missing for user type {user_type}")
        return cast(str, users[normalized_user_type + "s"][partner_code])

    if normalized_user_type in users:
        return cast(str, users[normalized_user_type])

    raise ValueError(f"Unknown user type: {user_type}")


def authenticate(username: str, client: TestClient) -> None:
    response = client.post(
        "/token", data={"username": username, "password": USER_PASSWORD}
    )
    token = response.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"


def get_authenticated_user_id(client: TestClient) -> int:
    response = client.get("/user")
    user = response.json()
    return cast(int, user["id"])


def not_authenticated(client: TestClient) -> None:
    if "Authorization" in client.headers:
        del client.headers["Authorization"]


def misauthenticate(client: TestClient) -> None:
    client.headers["Authorization"] = "Bearer some_invalid_token"


def _random_string() -> str:
    return str(uuid.uuid4())[:8]


def create_user(client: TestClient) -> Dict[str, Any]:
    username = _random_string()
    new_user_details = dict(
        username=username,
        email=f"{username}@example.com",
        given_name=_random_string(),
        family_name=_random_string(),
        password="very_secret",
        institution_id=5,
    )
    response = client.post("/users/", json=new_user_details)
    return dict(response.json())
