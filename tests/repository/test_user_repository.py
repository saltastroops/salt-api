import uuid
from dataclasses import asdict
from typing import Any, Callable, Optional, cast

import pytest
from pydantic import EmailStr
from pytest import MonkeyPatch
from sqlalchemy.engine import Connection

from saltapi.exceptions import NotFoundError
from saltapi.repository.user_repository import UserRepository
from saltapi.service.user import NewUserDetails, UserUpdate
from tests.conftest import find_usernames
from tests.markers import nodatabase

user_statistics = {
    "legal_status": "South African citizen",
    "gender": "Male",
    "race": "African",
    "has_phd": True,
    "year_of_phd_completion": 2020,
}


@nodatabase
def test_get_user(db_connection: Connection, check_data: Callable[[Any], None]) -> None:
    usernames = find_usernames("any", True)
    users = []
    for username in usernames:
        user_repository = UserRepository(db_connection)
        user = asdict(user_repository.get_by_username(username))
        user["roles"] = [
            str(role) for role in user["roles"]
        ]  # allow YAML representation
        users.append(user)
    check_data(users)


@nodatabase
def test_get_user_raises_error_for_non_existing_user(db_connection: Connection) -> None:
    user_repository = UserRepository(db_connection)
    with pytest.raises(NotFoundError):
        user_repository.get_by_username("idontexist")


@nodatabase
def test_get_user_by_id_returns_correct_user(
    db_connection: Connection, check_data: Callable[[Any], None]
) -> None:
    user_repository = UserRepository(db_connection)
    user = asdict(user_repository.get(3))
    check_data(user)


@nodatabase
def test_get_user_by_email_returns_correct_user(
    db_connection: Connection, check_data: Callable[[Any], None]
) -> None:
    user_repository = UserRepository(db_connection)
    user = asdict(user_repository.get_by_email("hettlage@saao.ac.za"))
    user["roles"] = [str(role) for role in user["roles"]]  # allow YAML representation
    check_data(user)


def _random_string() -> str:
    return str(uuid.uuid4())[:8]


@nodatabase
def test_create_user_raisers_error_if_username_exists_already(
    db_connection: Connection,
) -> None:
    username = "hettlage"
    new_user_details = NewUserDetails(
        username=username,
        email=EmailStr(f"{username}@example.com"),
        alternative_emails=[],
        given_name=_random_string(),
        family_name=_random_string(),
        password="very_secret",
        institution_id=5,
        **user_statistics,
    )
    user_repository = UserRepository(db_connection)
    with pytest.raises(ValueError) as excinfo:
        user_repository.create(new_user_details)

    assert "username" in str(excinfo.value).lower()


@nodatabase
def test_create_user_creates_a_new_user(db_connection: Connection) -> None:
    username = _random_string()
    new_user_details = NewUserDetails(
        username=username,
        password=_random_string(),
        email=EmailStr(f"{username}@example.com"),
        alternative_emails=[],
        given_name=_random_string(),
        family_name=_random_string(),
        institution_id=5,
        **user_statistics,
    )

    user_repository = UserRepository(db_connection)
    user_repository.create(new_user_details)

    created_user = user_repository.get_by_username(username)
    assert created_user.username == username
    assert created_user.password_hash is not None
    assert created_user.email == new_user_details.email
    assert created_user.given_name == new_user_details.given_name
    assert created_user.family_name == new_user_details.family_name
    assert created_user.roles == []


@nodatabase
def test_get_user_by_email_raises_error_for_non_existing_user(
    db_connection: Connection,
) -> None:
    user_repository = UserRepository(db_connection)
    with pytest.raises(NotFoundError):
        user_repository.get_by_username("invalid@email.com")


@nodatabase
def test_patch_raises_error_for_non_existing_user(db_connection: Connection) -> None:
    user_repository = UserRepository(db_connection)
    with pytest.raises(NotFoundError):
        user_repository.update(
            0, UserUpdate(username=None, password=None, **user_statistics)
        )


@nodatabase
def test_patch_uses_existing_values_by_default(db_connection: Connection) -> None:
    user_repository = UserRepository(db_connection)
    user_id = 1602
    old_user_details = user_repository.get(user_id)
    user_repository.update(
        user_id, UserUpdate(username=None, password=None, **user_statistics)
    )
    new_user_details = user_repository.get(user_id)

    assert old_user_details == new_user_details


def test_patch_replaces_existing_values(db_connection: Connection) -> None:
    user_repository = UserRepository(db_connection)
    user_id = 1602
    old_user_details = user_repository.get(user_id)

    new_username = "hettlage2"
    new_password = "a_new_shiny_password"
    assert not user_repository.verify_password(
        new_password, old_user_details.password_hash
    )

    user_repository.update(
        user_id,
        UserUpdate(username=new_username, password=new_password, **user_statistics),
    )
    new_user_details = user_repository.get(user_id)

    assert new_user_details.username == new_username
    assert user_repository.verify_password(new_password, new_user_details.password_hash)


def test_patch_is_idempotent(db_connection: Connection) -> None:
    user_repository = UserRepository(db_connection)
    user_id = 1602
    new_username = "hettlage2"
    new_password = "a_new_shiny_password"

    user_repository.update(
        user_id,
        UserUpdate(username=new_username, password=new_password, **user_statistics),
    )
    new_user_details_1 = user_repository.get_by_username(new_username)

    user_repository.update(
        user_id,
        UserUpdate(username=new_username, password=new_password, **user_statistics),
    )
    new_user_details_2 = user_repository.get_by_username(new_username)

    assert new_user_details_1 == new_user_details_2


def test_patch_cannot_use_existing_username(db_connection: Connection) -> None:
    user_repository = UserRepository(db_connection)
    user_id = 1602
    existing_username = "nhlavutelo"

    with pytest.raises(ValueError):
        user_repository.update(
            user_id,
            UserUpdate(username=existing_username, password=None, **user_statistics),
        )


def _check_user_has_role(
    role: str, method: str, proposal_code: Optional[str], db_connection: Connection
) -> None:
    user_repository = UserRepository(db_connection)
    for username in find_usernames(role, True, proposal_code):
        error_message = f"{method} should be True for username {username}, "
        f"proposal_code {proposal_code}"
        if proposal_code is not None:
            has_role = getattr(user_repository, method)(username, proposal_code)
        else:
            has_role = getattr(user_repository, method)(username)
        assert has_role, error_message


def _check_user_does_not_have_role(
    role: str, method: str, proposal_code: Optional[str], db_connection: Connection
) -> None:
    user_repository = UserRepository(db_connection)
    for username in find_usernames(role, False, proposal_code):
        error_message = f"{method} should be False for username {username}, "
        f"proposal_code {proposal_code}"
        if proposal_code is not None:
            has_role = getattr(user_repository, method)(username, proposal_code)
        else:
            has_role = getattr(user_repository, method)(username)
        assert not has_role, error_message


def _check_user_role(
    role: str, method: str, proposal_code: Optional[str], db_connection: Connection
) -> None:
    _check_user_has_role(role, method, proposal_code, db_connection)


@nodatabase
def test_is_investigator(db_connection: Connection) -> None:
    _check_user_role("investigator", "is_investigator", "2020-2-SCI-018", db_connection)


@nodatabase
def test_is_principal_investigator(db_connection: Connection) -> None:
    _check_user_role(
        "principal_investigator",
        "is_principal_investigator",
        "2018-2-LSP-001",
        db_connection,
    )


@nodatabase
def test_is_principal_contact(db_connection: Connection) -> None:
    _check_user_role(
        "principal_contact", "is_principal_contact", "2018-2-LSP-001", db_connection
    )


@nodatabase
def test_is_salt_astronomer(db_connection: Connection) -> None:
    _check_user_role("salt_astronomer", "is_salt_astronomer", None, db_connection)


@nodatabase
@pytest.mark.parametrize(
    "proposal_code",
    [
        "2021-2-LSP-001",
        "2019-2-SCI-027",
        "2021-2-MLT-004",
        "2021-1-DDT-002",
        "2016-1-SVP-001",
        "2021-1-DDT-002",
    ],
)
def test_is_tac_member(proposal_code: str, db_connection: Connection) -> None:
    _check_user_role(
        "tac_member", "is_tac_member_for_proposal", proposal_code, db_connection
    )


@nodatabase
@pytest.mark.parametrize(
    "proposal_code",
    [
        "2021-2-LSP-001",
        "2019-2-SCI-027",
        "2021-2-MLT-004",
        "2021-1-DDT-002",
        "2016-1-SVP-001",
        "2021-1-DDT-002",
    ],
)
def test_is_tac_chair(proposal_code: str, db_connection: Connection) -> None:
    _check_user_role(
        "tac_chair", "is_tac_chair_for_proposal", proposal_code, db_connection
    )


@nodatabase
def test_is_board_member(db_connection: Connection) -> None:
    _check_user_role("board_member", "is_board_member", None, db_connection)


@nodatabase
def test_is_partner_affiliated_user(db_connection: Connection) -> None:
    _check_user_role(
        "partner_affiliated_user", "is_partner_affiliated_user", None, db_connection
    )


@nodatabase
def test_is_administrator(db_connection: Connection) -> None:
    _check_user_role("administrator", "is_administrator", None, db_connection)


@nodatabase
@pytest.mark.parametrize(
    "role",
    [
        "investigator",
        "principal_investigator",
        "principal_contact",
        "tac_member_for_proposal",
        "tac_chair_for_proposal",
    ],
)
def test_role_checks_return_false_for_non_existing_proposal(
    db_connection: Connection, role: str
) -> None:
    user_repository = UserRepository(db_connection)
    assert (
        getattr(user_repository, f"is_{role}")(
            username="gw", proposal_code="idontexist"
        )
        is False
    )


def test_has_proposal_permission_returns_correct_result(
    db_connection: Connection,
) -> None:
    user_repository = UserRepository(db_connection)
    proposal_code = "2022-2-COM-001"
    grantee_username = find_usernames("proposal_view_grantee", True, proposal_code)[0]
    grantee_id = user_repository.get_by_username(grantee_username).id
    assert user_repository.user_has_proposal_permission(
        user_id=grantee_id,
        permission_type="View",
        proposal_code=proposal_code,
    )

    non_grantee_username = find_usernames(
        "proposal_view_non_grantee", True, proposal_code
    )[0]
    non_grantee_id = user_repository.get_by_username(non_grantee_username).id
    assert not user_repository.user_has_proposal_permission(
        user_id=non_grantee_id,
        permission_type="View",
        proposal_code=proposal_code,
    )


@nodatabase
def test_find_by_username_and_password_returns_correct_user(
    db_connection: Connection,
    check_data: Callable[[Any], None],
    monkeypatch: MonkeyPatch,
) -> None:
    user_repository = UserRepository(db_connection)

    # Allow any password
    monkeypatch.setattr(
        user_repository, "verify_password", lambda password, hashed_password: True
    )

    username = "hettlage"
    user = asdict(
        user_repository.find_user_with_username_and_password(username, "some_password")
    )
    user["roles"] = [str(role) for role in user["roles"]]  # allow YAML representation

    assert user["username"] == username
    check_data(user)


@nodatabase
@pytest.mark.parametrize("username", ["idontexist", "", None])
def test_find_by_username_and_password_raises_error_for_wrong_username(
    db_connection: Connection, username: Optional[str], monkeypatch: MonkeyPatch
) -> None:
    user_repository = UserRepository(db_connection)

    # Allow any password
    monkeypatch.setattr(
        user_repository, "verify_password", lambda password, hashed_password: True
    )

    with pytest.raises(NotFoundError):
        user_repository.find_user_with_username_and_password(
            cast(str, username), "some_password"
        )


@nodatabase
def test_find_by_username_and_password_raises_error_for_wrong_password(
    db_connection: Connection,
) -> None:
    user_repository = UserRepository(db_connection)
    username = "hettlage"

    # Make sure the user exists
    assert user_repository.get_by_username(username)

    with pytest.raises(NotFoundError):
        user_repository.find_user_with_username_and_password(username, "wrongpassword")

    with pytest.raises(NotFoundError):
        user_repository.find_user_with_username_and_password(username, "")

    # None may raise an exception other than NotFoundError
    with pytest.raises(Exception):
        user_repository.find_user_with_username_and_password(username, cast(str, None))


@pytest.mark.parametrize(
    "user_id,exists",
    [(-1, False), (0, False), (2, False), (3, True), (1768, True), (345678, False)],
)
def test_is_existing_user_id(
    user_id: int, exists: bool, db_connection: Connection
) -> None:
    user_repository = UserRepository(db_connection)

    assert user_repository.is_existing_user_id(user_id) == exists


def test_get_proposal_permissions_raises_not_found_error(
    db_connection: Connection,
) -> None:
    user_repository = UserRepository(db_connection)

    with pytest.raises(NotFoundError):
        user_repository.get_proposal_permissions(-1)


def test_get_proposal_permissions(
    db_connection: Connection,
) -> None:
    user_repository = UserRepository(db_connection)

    user1_id = 42
    user2_id = 145
    permission1 = {"proposal_code": "2020-2-SCI-008", "permission_type": "View"}
    permission2 = {"proposal_code": "2020-2-SCI-009", "permission_type": "View"}
    permission3 = {"proposal_code": "2020-2-SCI-010", "permission_type": "View"}

    # Initially there are no granted permissions
    assert len(user_repository.get_proposal_permissions(user1_id)) == 0

    # Grant some permissions
    user_repository.grant_proposal_permission(user1_id, **permission1)
    user_repository.grant_proposal_permission(user2_id, **permission2)
    user_repository.grant_proposal_permission(user1_id, **permission3)

    # Check that the correct permissions are returned
    granted_permissions = user_repository.get_proposal_permissions(user1_id)

    assert len(granted_permissions) == 2
    assert permission1 in granted_permissions
    assert permission3 in granted_permissions


@pytest.mark.parametrize(
    "user_id,proposal_code,permission_type",
    [
        (-1, "2020-1-SCI-003", "View"),
        (42, "non-existing-proposal-code", "View"),
        (42, "2020-1-SCI-003", "non-existing-type"),
    ],
)
def test_grant_proposal_permission_raises_not_found_errors(
    user_id: int, proposal_code: str, permission_type: str, db_connection: Connection
) -> None:
    user_repository = UserRepository(db_connection)

    with pytest.raises(NotFoundError):
        user_repository.grant_proposal_permission(
            user_id=user_id,
            permission_type=permission_type,
            proposal_code=proposal_code,
        )


def test_grant_proposal_permission(db_connection: Connection) -> None:
    user_repository = UserRepository(db_connection)

    user_id = 15
    permission = {"proposal_code": "2020-1-SCI-003", "permission_type": "View"}

    # Initially there are no granted permissions
    assert len(user_repository.get_proposal_permissions(user_id)) == 0

    # Grant a permission
    user_repository.grant_proposal_permission(user_id, **permission)

    # Check that the permission has been granted
    granted_permissions = user_repository.get_proposal_permissions(user_id)
    assert len(granted_permissions) == 1
    assert granted_permissions[0] == permission


def test_grant_proposal_permissions_is_idempotent(db_connection: Connection) -> None:
    user_repository = UserRepository(db_connection)

    user_id = 15
    permission = {"proposal_code": "2022-2-SCI-007", "permission_type": "View"}

    # Initially there are no granted permissions
    assert len(user_repository.get_proposal_permissions(user_id)) == 0

    # Grant some permissions
    user_repository.grant_proposal_permission(user_id, **permission)
    user_repository.grant_proposal_permission(user_id, **permission)

    # Check that the permission has not been added twice
    granted_permissions = user_repository.get_proposal_permissions(user_id)
    assert len(granted_permissions) == 1
    assert granted_permissions[0] == permission


@pytest.mark.parametrize(
    "user_id,proposal_code,permission_type",
    [
        (-1, "2020-1-SCI-003", "View"),
        (42, "non-existing-proposal-code", "View"),
        (42, "2020-1-SCI-003", "non-existing-type"),
    ],
)
def test_revoke_proposal_permission_raises_not_found_errors(
    user_id: int, proposal_code: str, permission_type: str, db_connection: Connection
) -> None:
    user_repository = UserRepository(db_connection)

    with pytest.raises(NotFoundError):
        user_repository.revoke_proposal_permission(
            user_id=user_id,
            permission_type=permission_type,
            proposal_code=proposal_code,
        )


def test_revoke_proposal_permission(db_connection: Connection) -> None:
    user_repository = UserRepository(db_connection)

    user_id = 15
    permission = {"proposal_code": "2020-1-SCI-003", "permission_type": "View"}

    # Grant a permission
    user_repository.grant_proposal_permission(user_id=user_id, **permission)

    # Check that the permission has been granted
    granted_permissions = user_repository.get_proposal_permissions(user_id)
    assert len(granted_permissions) == 1

    # Revoke the permission
    user_repository.revoke_proposal_permission(user_id, **permission)

    # Check that the permission has been revoked
    granted_permissions = user_repository.get_proposal_permissions(user_id)
    assert len(granted_permissions) == 0


def test_revoke_proposal_permissions_is_idempotent(db_connection: Connection) -> None:
    user_repository = UserRepository(db_connection)

    user_id = 15
    permission = {"proposal_code": "2020-1-SCI-003", "permission_type": "View"}

    # Grant a permission
    user_repository.grant_proposal_permission(user_id, **permission)

    # Check that the permission has been granted
    granted_permissions = user_repository.get_proposal_permissions(user_id)
    assert len(granted_permissions) == 1

    # Revoke the permission twice
    user_repository.revoke_proposal_permission(user_id, **permission)
    user_repository.revoke_proposal_permission(user_id, **permission)

    # Check that the permission has been revoked
    granted_permissions = user_repository.get_proposal_permissions(user_id)
    assert len(granted_permissions) == 0
