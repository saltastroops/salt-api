import os
import re
import shutil
import uuid
from datetime import timedelta
from unittest.mock import MagicMock, patch

import dotenv

from saltapi.service.authentication_service import AuthenticationService
from saltapi.service.mail_service import MailService
from saltapi.web.schema.user import LegalStatus

# Make sure that the test database etc. are used.
# IMPORTANT: These lines must be executed before any server-related package is imported.

os.environ["DOTENV_FILE"] = ".env.test"
dotenv.load_dotenv(os.environ["DOTENV_FILE"])

from pathlib import Path
from typing import Any, Callable, Dict, Generator, List, Optional, cast

import fastapi
import pytest
import yaml
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection, Engine

import saltapi.web.api.authentication
from saltapi.exceptions import AuthenticationError
from saltapi.main import app
from saltapi.repository.user_repository import UserRepository
from saltapi.service.user import User
from saltapi.service.user_service import UserService


def get_user_authentication_function() -> Callable[[str, str], User]:
    def authenticate_user(username: str, password: str) -> User:
        if password != USER_PASSWORD and password != USER_PASSWORD_UPDATE:
            raise AuthenticationError("No user found for username and password")

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
USER_PASSWORD_UPDATE = "my-shiny-very-very-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_LIFETIME_HOURS = 7 * 24


def _create_engine() -> Engine:
    sdb_dsn = os.environ.get("SDB_DSN")
    if sdb_dsn:
        echo_sql = (
            True if os.environ.get("ECHO_SQL") else False
        )  # SQLAlchemy needs a bool
        return create_engine(
            sdb_dsn,
            echo=echo_sql,
            future=True,
        )
    else:
        raise ValueError("No SDB_DSN environment variable set")


@pytest.fixture(autouse=True)
def mock_engine(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(saltapi.repository.unit_of_work, "engine", _create_engine)
    monkeypatch.setattr(saltapi.web.api.submissions, "engine", _create_engine)
    monkeypatch.setattr(saltapi.service.submission_service, "engine", _create_engine)


@pytest.fixture(scope="function")
def db_connection() -> Generator[Connection, None, None]:
    with _create_engine().connect() as connection:
        yield connection


def _data_file(data_type: str, request: pytest.FixtureRequest) -> Path:
    if "TEST_DATA_DIR" not in os.environ:
        pytest.fail("Environment variable not set: TEST_DATA_DIR")
    root_dir = Path(os.environ["TEST_DATA_DIR"]) / data_type

    test_file = request.path.relative_to(request.config.rootpath)
    parent_dir = (root_dir / test_file).parent
    node_dir = test_file.stem
    return parent_dir / node_dir / (re.sub(r"\W", "_", request.node.name) + ".yml")


@pytest.fixture(scope="function")
def check_data(
        data_regression: Any, request: pytest.FixtureRequest
) -> Generator[Callable[[Any], None], None, None]:
    # Figure out the file path for the data file
    data_file = _data_file("regression", request)

    def f(data: Any) -> Any:
        data_regression.check(data, fullpath=data_file)

    yield f


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    yield TestClient(app)


@pytest.fixture()
def saao_client() -> Generator[TestClient, None, None]:
    """
    Test client that has a SAAO network ip.
    """
    request_client = MagicMock()
    request_client.host = "10.1.0.0"
    with patch.object(fastapi.Request, "client", request_client):
        yield TestClient(app)


@pytest.fixture
def email_service_mock():
    return MailService()


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

    if "TEST_DATA_DIR" not in os.environ:
        pytest.fail("Environment variable not set: TEST_DATA_DIR")
    test_data_dir = Path(os.environ["TEST_DATA_DIR"])
    users_file = test_data_dir / "users.yml"
    with open(users_file) as f:
        users = yaml.safe_load(f)

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

    if normalized_user_type == "administrator_and_investigator":
        if proposal_code is None:
            raise ValueError(f"Proposal code missing for user type {user_type}")
        return cast(str, users[normalized_user_type][proposal_code])

    if normalized_user_type == "principal_investigator_of_other_proposals":
        if proposal_code is None:
            raise ValueError(f"Proposal code missing for user type {user_type}")
        return cast(str, users[normalized_user_type][proposal_code])

    if normalized_user_type == "proposal_view_grantee":
        if proposal_code is None:
            raise ValueError(f"Proposal code missing for user type {user_type}")
        return cast(str, users[normalized_user_type][proposal_code])

    if normalized_user_type == "principal_contact_of_other_proposals":
        if proposal_code is None:
            raise ValueError(f"Proposal code missing for user type {user_type}")
        return cast(str, users[normalized_user_type][proposal_code])

    if normalized_user_type in users:
        return cast(str, users[normalized_user_type])

    raise ValueError(f"Unknown user type: {user_type}")


def find_usernames(
        role: str, has_role: bool, proposal_code: Optional[str] = None
) -> List[str]:
    normalized_role = role.lower()
    normalized_role = normalized_role.replace(" ", "_").replace("-", "_")

    if "TEST_DATA_DIR" not in os.environ:
        pytest.fail("Environment variable not set: TEST_DATA_DIR")
    test_data_dir = Path(os.environ["TEST_DATA_DIR"])
    users_file = test_data_dir / "user_roles.yml"
    with open(users_file) as f:
        users = yaml.safe_load(f)

    if normalized_role in [
        "administrator",
        "any",
        "board_member",
        "partner_affiliated_user",
        "salt_astronomer",
    ]:
        usernames = (
            users[normalized_role]["with_role"]
            if has_role
            else users[normalized_role]["without_role"]
        )
        return list(usernames)

    if normalized_role in users:
        usernames = (
            users[normalized_role][proposal_code]["with_role"]
            if has_role
            else users[normalized_role][proposal_code]["without_role"]
        )
        return list(usernames)

    raise ValueError(f"Unknown user role: {role}")


def authenticate(username: str, client: TestClient) -> None:
    response = client.post(
        "/token", data={"username": username, "password": USER_PASSWORD}
    )
    token = response.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"


def authenticate_with_validation_token(user_id: int, client: TestClient) -> None:
    with cast(Engine, _create_engine()).connect() as connection:
        user_repository = UserRepository(connection)
        auth_service = AuthenticationService(user_repository)
        token = auth_service.jwt_token({"sub": str(user_id)}, timedelta(hours=1), verification=True)
        client.headers["Authorization"] = f"Bearer {token}"


def get_user_by_username(username: str) -> User:
    with cast(Engine, _create_engine()).connect() as connection:
        user_repository = UserRepository(connection)
        return user_repository.get_by_username(username)


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
        legal_status=LegalStatus.OTHER,
        race=None,
        gender=None,
        has_phd=None,
        year_of_phd_completion=None,
    )
    response = client.post("/users/", json=new_user_details)
    return dict(response.json())


def setup_finder_chart_files(
        proposals_dir: Path,
        proposal_code: str,
        parent_dirs: List[str],
        finder_chart_name: str,
        original_suffixes: List[str],
        thumbnail_suffixes: List[str],
) -> List[Path]:
    """
    Setup dummy finder charts.

    Parameters
    ----------
    proposals_dir: `~Path`
        Base directory for the proposals content.
    proposal_code: str
        Proposal code to which the finder belongs.
    parent_dirs: list of `str`
        Parent directories below the proposal code directory. This will be a list like
        ["Included"] or ["4", "Included"].
    finder_chart_name: str
        Filename of the finder chart, without a suffix.
    original_suffixes: list of `str`
        List of file suffixes (without leading dot, such as "png" rather than ".png")
        for which an original size finder chart file should exist
    thumbnail_suffixes: list of `str`
        List of file suffixes (without leading dot, such as "png" rather than ".png")
        for which an original size finder chart file should exist

    Returns
    -------
    list of `~Path`
        The created finder chart files.
    """
    created_files = []
    parent_dir = proposals_dir / proposal_code
    for d in parent_dirs:
        parent_dir /= d
    parent_dir.mkdir(parents=True)

    def setup_finder_chart(suffix: str, size: str) -> None:
        prefix = ""
        if size == "original":
            prefix = ""
        elif size == "thumbnail":
            prefix = "Thumbnail"
        else:
            pytest.fail(f"Unsupported size in test setup: {size}")

        if suffix in ["jpg", "pdf", "png"]:
            finder_chart_template = (
                    Path(__file__).parent
                    / "data"
                    / "finder_charts"
                    / f"finder_chart.{suffix}"
            )
            finder_chart = parent_dir / f"{prefix}{finder_chart_name}.{suffix}"
            shutil.copy(finder_chart_template, finder_chart)
            created_files.append(finder_chart)
        else:
            pytest.fail(f"Unsupported file suffix in test setup: {suffix}")

    for suffix in original_suffixes:
        setup_finder_chart(suffix, "original")
    for suffix in thumbnail_suffixes:
        setup_finder_chart(suffix, "thumbnail")

    return created_files
