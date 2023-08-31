from datetime import date, datetime
from pathlib import Path
from typing import Any, Callable, Dict, List
from unittest.mock import patch

import freezegun
import pytest
from pytest_mock import MockerFixture
from sqlalchemy.engine import Connection

import saltapi.repository.proposal_repository
from saltapi.exceptions import NotFoundError
from saltapi.repository.proposal_repository import ProposalRepository
from saltapi.settings import Settings, get_settings
from tests.conftest import find_username
from tests.markers import nodatabase

mock_now = date(2022, 12, 1)


@nodatabase
@pytest.mark.parametrize(
    "semester,proposal_code",
    [("2020-1", "2020-1-DDT-008"), ("2020-2", "2018-2-LSP-001")],
)
def test_list_returns_correct_content(
    semester: str,
    proposal_code: str,
    db_connection: Connection,
    check_data: Callable[[Any], None],
) -> None:
    salt_astronomer = find_username("SALT Astronomer")
    proposal_repository = ProposalRepository(db_connection)
    proposals = proposal_repository.list(salt_astronomer, semester, semester)
    proposal = [p for p in proposals if p["proposal_code"] == proposal_code][0]
    check_data(proposal)


@nodatabase
@pytest.mark.parametrize(
    "from_semester,to_semester,user_args",
    [
        # TAC chair for South Africa
        ("2020-1", "2020-1", {"user_type": "TAC Chair", "partner_code": "RSA"}),
        # TAC chair for RU
        # Proposal 2020-1-MLT-005 has an investigator from RU, but isn't requesting time
        # from RU for 2021-1 (although it is requesting time from UW)
        ("2021-1", "2021-1", {"user_type": "TAC Chair", "partner_code": "RU"}),
        # TAC member for UW
        ("2021-1", "2021-1", {"user_type": "TAC member", "partner_code": "UW"}),
        # User without a proposal in the semester
        (
            "2020-2",
            "2020-2",
            {"user_type": "Principal Investigator", "proposal_code": "2014-2-SCI-078"},
        ),
        # User over multiple semesters
        (
            "2017-2",
            "2021-1",
            {"user_type": "Principal Investigator", "proposal_code": "2018-2-LSP-001"},
        ),
        # SALT Astronomer
        # There are 82 proposals for 2020-2, one of which has been deleted
        ("2020-2", "2020-2", {"user_type": "SALT Astronomer"}),
        # Administrator
        # There are 81 proposals for 2018-2, two of which have been deleted
        ("2018-2", "2018-2", {"user_type": "administrator"}),
        # Gravitational wave event proposals can be viewed by a user affiliated with a
        # SALT partner
        (
            "2018-2",
            "2019-1",
            {"user_type": "Principal Investigator", "proposal_code": "2014-2-SCI-078"},
        ),
        # Gravitational wave event proposals cannot be viewed by a user affiliated who
        # is not affiliated to a SALT partner
        (
            "2018-2",
            "2019-1",
            {"user_type": "Principal Contact", "proposal_code": "2021-1-SCI-014"},
        ),
    ],
)
def test_list_returns_correct_proposal_codes(
    from_semester: str,
    to_semester: str,
    user_args: Dict[str, Any],
    db_connection: Connection,
    check_data: Callable[[Any], None],
) -> None:
    proposal_repository = ProposalRepository(db_connection)
    username = find_username(**user_args)
    proposals = proposal_repository.list(
        username=username, from_semester=from_semester, to_semester=to_semester
    )
    proposal_codes = sorted(p["proposal_code"] for p in proposals)
    check_data(
        {"proposal_count": len(proposal_codes), "proposal_codes": proposal_codes}
    )


@nodatabase
def test_list_handles_omitted_semester_limits(db_connection: Connection) -> None:
    proposal_repository = ProposalRepository(db_connection)

    salt_astronomer = find_username("SALT Astronomer")
    assert len(
        proposal_repository.list(username=salt_astronomer, to_semester="2015-1")
    ) == len(
        proposal_repository.list(
            username=salt_astronomer, from_semester="2000-1", to_semester="2015-1"
        )
    )
    assert len(
        proposal_repository.list(username=salt_astronomer, from_semester="2020-1")
    ) == len(proposal_repository.list(username=salt_astronomer, from_semester="2020-1"))
    assert len(proposal_repository.list(username=salt_astronomer)) == len(
        proposal_repository.list(
            username=salt_astronomer, from_semester="2000-1", to_semester="2100-1"
        )
    )


@nodatabase
@pytest.mark.parametrize("semester,limit", [("2019-1", 4), ("2020-2", 0)])
def test_list_results_can_be_limited(
    semester: str,
    limit: int,
    db_connection: Connection,
    check_data: Callable[[Any], None],
) -> None:
    salt_astronomer = find_username("SALT Astronomer")
    proposal_repository = ProposalRepository(db_connection)
    proposals = proposal_repository.list(
        username=salt_astronomer,
        from_semester=semester,
        to_semester=semester,
        limit=limit,
    )
    check_data([p["proposal_code"] for p in proposals])


@nodatabase
def test_list_handles_omitted_limit(db_connection: Connection) -> None:
    proposal_repository = ProposalRepository(db_connection)
    assert proposal_repository.list(
        username="someone", from_semester="2018-2", to_semester="2019-2"
    ) == proposal_repository.list(
        username="someone", from_semester="2018-2", to_semester="2019-2", limit=100000
    )


def test_list_raises_error_for_negative_limit(db_connection: Connection) -> None:
    with pytest.raises(ValueError) as excinfo:
        proposal_repository = ProposalRepository(db_connection)
        proposal_repository.list(username="someone", limit=-1)

    assert "negative" in str(excinfo)


@pytest.mark.parametrize(
    "incorrect_semester",
    ["200-1", "20212-1", "2020-", "2020-11", "2020", "20202", "abcd-1", "2021-a"],
)
@nodatabase
def test_list_raises_error_for_wrong_semester_format(
    incorrect_semester: str, db_connection: Connection
) -> None:
    proposal_repository = ProposalRepository(db_connection)

    with pytest.raises(ValueError) as excinfo:
        proposal_repository.list(username="someone", from_semester=incorrect_semester)
    assert "format" in str(excinfo)

    with pytest.raises(ValueError) as excinfo:
        proposal_repository.list(username="someone", to_semester=incorrect_semester)
    assert "format" in str(excinfo)


@nodatabase
def test_list_raises_error_for_wrong_semester_order(db_connection: Connection) -> None:
    proposal_repository = ProposalRepository(db_connection)
    with pytest.raises(ValueError) as excinfo:
        username = find_username("SALT Astronomer")
        proposal_repository.list(
            username=username, from_semester="2021-2", to_semester="2021-1"
        )
    assert "semester" in str(excinfo.value)


@nodatabase
def test_get_raises_error_for_wrong_proposal_code(db_connection: Connection) -> None:
    proposal_repository = ProposalRepository(db_connection)
    with pytest.raises(NotFoundError):
        proposal_repository.get(proposal_code="idontexist")


@nodatabase
def test_get_returns_general_info(
    db_connection: Connection, check_data: Callable[[Any], None]
) -> None:
    proposal_code = "2019-2-DDT-006"
    proposal_repository = ProposalRepository(db_connection)
    proposal = proposal_repository.get(proposal_code)
    general_info = proposal["general_info"]
    check_data(general_info)


@pytest.mark.parametrize(
    "proposal_code,expected_self_activatable",
    [("2018-1-SCI-041", False), ("2018-2-LSP-001", True)],
)
def test_get_returns_correct_value_for_is_self_activatable(
    proposal_code: str, expected_self_activatable: bool, db_connection: Connection
) -> None:
    proposal_repository = ProposalRepository(db_connection)
    proposal = proposal_repository.get(proposal_code)

    assert proposal["general_info"]["is_self_activatable"] == expected_self_activatable


@nodatabase
def test_get_returns_investigators(
    db_connection: Connection, check_data: Callable[[Any], None]
) -> None:
    proposal_code = "2019-2-DDT-006"
    proposal_repository = ProposalRepository(db_connection)
    proposal = proposal_repository.get(proposal_code)
    investigators = proposal["investigators"]
    check_data(investigators)


def test_get_returns_correct_proposal_approval(
    db_connection: Connection, check_data: Callable[[Any], None]
) -> None:
    proposal_code = "2018-2-LSP-001"

    proposal_repository = ProposalRepository(db_connection)
    proposal = proposal_repository.get(proposal_code)
    investigators = proposal["investigators"]

    approved_investigators = [
        i for i in investigators if i["has_approved_proposal"] is True
    ]
    rejected_investigators = [
        i for i in investigators if i["has_approved_proposal"] is False
    ]
    undecided_investigators = [
        i for i in investigators if i["has_approved_proposal"] is None
    ]

    check_data(
        {
            "approved": approved_investigators,
            "rejected": rejected_investigators,
            "undecided": undecided_investigators,
        }
    )


@nodatabase
def test_get_returns_time_allocations(
    db_connection: Connection, check_data: Callable[[Any], None]
) -> None:
    proposal_code = "2018-2-LSP-001"
    semester = "2021-1"

    proposal_repository = ProposalRepository(db_connection)
    proposal = proposal_repository.get(proposal_code, semester)
    allocations = proposal["time_allocations"]
    allocations.sort(key=lambda v: v["partner_code"])
    check_data(allocations)


@nodatabase
def test_get_returns_charged_time(
    db_connection: Connection, check_data: Callable[[Any], None]
) -> None:
    proposal_code = "2018-2-LSP-001"
    semester = "2020-2"

    proposal_repository = ProposalRepository(db_connection)
    proposal = proposal_repository.get(proposal_code, semester)
    charged_time = proposal["charged_time"]

    check_data(charged_time)


@pytest.mark.parametrize(
    "proposal_code",
    ["2016-2-SCI-008", "2020-1-DDT-008", "2019-2-DDT-002", "2019-1-MLT-001"],
)
def test_get_returns_proprietary_period(
    proposal_code: str, db_connection: Connection, check_data: Callable[[Any], None]
) -> None:
    proposal_repository = ProposalRepository(db_connection)
    proposal = proposal_repository.get(proposal_code)
    release_date = proposal["general_info"]["proprietary_period"]
    check_data(release_date)


@pytest.mark.parametrize(
    "now",
    [
        "2021-07-21T11:59:59Z",  # just before the (Julian) day changes,
        "2021-07-21T12:00:01Z",  # just after the (Julian) day changes
    ],
)
def test_get_returns_block_observability(
    now: str, db_connection: Connection, check_data: Callable[[Any], None]
) -> None:
    proposal_code = "2018-2-LSP-001"
    semester = "2021-1"

    with freezegun.freeze_time(now):
        proposal_repository = ProposalRepository(db_connection)
        proposal = proposal_repository.get(proposal_code, semester)
        blocks = proposal["blocks"]
        block_ids = [89205, 89301, 89177, 89392]
        observabilities = []
        for block_id in block_ids:
            block = next(b for b in blocks if b["id"] == block_id)
            observabilities.append(
                {
                    "block_id": block_id,
                    "is_observable_tonight": block["is_observable_tonight"],
                    "remaining_nights": block["remaining_nights"],
                }
            )


def test_get_returns_observation_comments(
    db_connection: Connection, check_data: Callable[[Any], None]
) -> None:
    proposal_code = "2020-2-DDT-001"

    proposal_repository = ProposalRepository(db_connection)
    proposal = proposal_repository.get(proposal_code)
    comments = proposal["observation_comments"]

    check_data(comments)


@pytest.mark.parametrize(
    "proposal_code,expected_proposal_type",
    [
        ("2020-2-SCI-043", "Science"),
        ("2021-1-MLT-003", "Science - Long Term"),
        ("2018-2-LSP-001", "Large Science Proposal"),
        ("2016-1-COM-001", "Commissioning"),
        ("2016-1-SVP-001", "Science Verification"),
        ("2019-1-GWE-005", "Gravitational Wave Event"),
        ("2020-2-DDT-005", "Director's Discretionary Time"),
    ],
)
def test_get_proposal_type_returns_the_correct_proposal_type(
    proposal_code: str, expected_proposal_type: str, db_connection: Connection
) -> None:
    proposal_repository = ProposalRepository(db_connection)
    proposal_type = proposal_repository.get_proposal_type(proposal_code)
    assert proposal_type == expected_proposal_type


def test_get_proposal_type_raises_not_found_error(db_connection: Connection) -> None:
    proposal_repository = ProposalRepository(db_connection)
    with pytest.raises(NotFoundError):
        proposal_repository.get_proposal_type("idontexist")


@pytest.mark.parametrize(
    "proposal_code,expected_status,expected_reason",
    [
        ("2021-2-MLT-002", "Deleted", "Resubmitted as 2021-2-MLT-004"),
        ("2019-1-SCI-010", "Completed", ""),
    ],
)
def test_get_proposal_status(
    proposal_code: str,
    expected_status: str,
    expected_reason: str,
    db_connection: Connection,
) -> None:
    proposal_repository = ProposalRepository(db_connection)
    status = proposal_repository.get_proposal_status(proposal_code)

    assert status["value"] == expected_status
    assert status["comment"] == expected_reason


def test_get_proposal_status_raises_error_for_wrong_proposal_code(
    db_connection: Connection,
) -> None:
    proposal_repository = ProposalRepository(db_connection)
    with pytest.raises(NotFoundError):
        proposal_repository.get_proposal_status("idontexist")


def test_update_proposal_status(db_connection: Connection) -> None:
    # Set the status to "Active"
    proposal_repository = ProposalRepository(db_connection)
    proposal_code = "2020-2-SCI-043"
    proposal_repository.update_proposal_status(proposal_code, "Active")
    status = proposal_repository.get_proposal_status(proposal_code)
    assert status["value"] == "Active"
    assert status["comment"] is None

    # Now set it to "Under technical review"
    proposal_repository.update_proposal_status(proposal_code, "Under technical review")
    assert (
        proposal_repository.get_proposal_status(proposal_code)["value"]
        == "Under technical review"
    )


def test_update_proposal_status_for_not_none_status_reason(
    db_connection: Connection,
) -> None:
    # Set the status to "Expired"
    proposal_repository = ProposalRepository(db_connection)
    proposal_code = "2019-1-SCI-010"
    proposal_repository.update_proposal_status(proposal_code, "Expired")
    status = proposal_repository.get_proposal_status(proposal_code)
    assert status["value"] == "Expired"
    assert status["comment"] is None

    # Now set it to "Deleted"
    proposal_repository.update_proposal_status(proposal_code, "Deleted")
    assert proposal_repository.get_proposal_status(proposal_code)["value"] == "Deleted"


def test_update_proposal_status_raises_error_for_wrong_proposal_code(
    db_connection: Connection,
) -> None:
    proposal_repository = ProposalRepository(db_connection)
    with pytest.raises(NotFoundError):
        proposal_repository.get_proposal_status("idontexist")


def test_update_proposal_status_raises_error_for_wrong_status(
    db_connection: Connection,
) -> None:
    proposal_repository = ProposalRepository(db_connection)
    with pytest.raises(ValueError) as excinfo:
        proposal_repository.update_proposal_status(
            "2020-2-SCIO-043", "Wrong proposal status"
        )

    assert "proposal status" in str(excinfo)


@pytest.mark.parametrize(
    "proposal_code,expected_self_activatable",
    [("2018-1-SCI-041", False), ("2018-2-LSP-001", True)],
)
def test_is_self_activatable(
    proposal_code: str, expected_self_activatable: bool, db_connection: Connection
) -> None:
    proposal_repository = ProposalRepository(db_connection)
    assert (
        proposal_repository.is_self_activatable(proposal_code)
        == expected_self_activatable
    )


@nodatabase
@pytest.mark.parametrize("proposal_code", ["2019-2-SCI-046", "2021-1-MLT-007"])
def test_get_returns_additional_instrument_details(
    proposal_code: str, db_connection: Connection, check_data: Callable[[Any], None]
) -> None:
    proposal_repository = ProposalRepository(db_connection)
    proposal = proposal_repository.get(proposal_code)
    blocks = proposal["blocks"]
    instruments = [
        {"block_id": block["id"], "instruments": block["instruments"]}
        for block in blocks
    ]
    check_data(instruments)


@pytest.mark.parametrize(
    "proposal_code,version",
    [("2022-1-SCI-024", 1), ("2021-2-SCI-004", 2), ("2019-2-SCI-027", 19)],
)
def test_get_current_version_returns_correct_version(
    proposal_code: str, version: int, db_connection: Connection
) -> None:
    proposal_repository = ProposalRepository(db_connection)
    assert proposal_repository.get_current_version(proposal_code) == version


def test_get_current_version_raises_not_found_error(db_connection: Connection) -> None:
    proposal_repository = ProposalRepository(db_connection)
    with pytest.raises(NotFoundError):
        proposal_repository.get_current_version("idontexist")


@pytest.mark.parametrize(
    "proposal_code,maximum_period",
    [
        ("2020-1-SCI-005", 24),  # RSA allocated time
        ("2018-2-LSP-001", 24),  # RSA Allocated time
        ("2020-1-SCI-003", 1200),  # RSA allocated no time
        ("2020-1-MLT-005", 1200),  # RSA allocated no time
        ("2016-1-COM-001", 36),
        ("2016-1-SVP-001", 12),
        ("2019-1-GWE-005", 1200),
        ("2022-1-ORP-001", 24),
        ("2020-2-DDT-005", 6),
    ],
)
def test_get_maximum_proprietary_period_returns_correct_proprietary_period(
    proposal_code: str, maximum_period: int, db_connection: Connection
) -> None:
    proposal_repository = ProposalRepository(db_connection)
    assert (
        proposal_repository.maximum_proprietary_period(proposal_code) == maximum_period
    )


@pytest.mark.parametrize(
    "proposal_code,block_visits,expected_date",
    [
        ("2020-2-SCI-005", [], date(2023, 5, 1)),
        ("2020-2-SCI-005", [{"night": date(2021, 2, 1)}], date(2021, 5, 1)),
        ("2020-2-SCI-005", [{"night": date(2021, 4, 30)}], date(2021, 5, 1)),
        ("2020-2-SCI-005", [{"night": date(2021, 5, 1)}], date(2021, 11, 1)),
        ("2020-2-SCI-005", [{"night": date(2021, 5, 2)}], date(2021, 11, 1)),
        ("2020-2-SCI-005", [{"night": date(2021, 8, 15)}], date(2021, 11, 1)),
        ("2020-2-SCI-005", [{"night": date(2021, 11, 1)}], date(2022, 5, 1)),
        ("2020-2-SCI-005", [{"night": date(2021, 10, 31)}], date(2021, 11, 1)),
        ("2020-2-SCI-005", [{"night": date(2021, 12, 1)}], date(2022, 5, 1)),
        (
            "2020-2-SCI-005",
            [
                {"night": date(2021, 12, 20)},
                {"night": date(2021, 6, 1)},
                {"night": date(2021, 6, 24)},
                {"night": date(2021, 6, 23)},
                {"night": date(2021, 12, 2)},
            ],
            date(2022, 5, 1),
        ),
    ],
)
def test_proprietary_period_start_date_returns_correct_start_date(
    proposal_code: str,
    block_visits: List[Dict[str, Any]],
    expected_date: datetime,
    db_connection: Connection,
    monkeypatch: MockerFixture,
) -> None:
    with patch("saltapi.repository.proposal_repository.datetime") as mock_datetime:
        mock_datetime.today.return_value = mock_now
        mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)
        proposal_repository = ProposalRepository(db_connection)
        assert (
            proposal_repository.proprietary_period_start_date(block_visits)
            == expected_date
        )


@pytest.mark.parametrize(
    "proposal_code,proprietary_period,block_visits,expected_date",
    [
        ("2020-2-SCI-005", 0, [], date(2023, 11, 1)),
        ("2020-2-SCI-005", 10, [], date(2024, 9, 1)),
        ("2020-2-SCI-005", 0, [{"night": date(2021, 2, 1)}], date(2021, 5, 1)),
        ("2020-2-SCI-005", 10, [{"night": date(2021, 2, 1)}], date(2022, 3, 1)),
        ("2020-2-SCI-005", 0, [{"night": date(2021, 4, 30)}], date(2021, 5, 1)),
        ("2020-2-SCI-005", 10, [{"night": date(2021, 4, 30)}], date(2022, 3, 1)),
        ("2020-2-SCI-005", 0, [{"night": date(2021, 5, 1)}], date(2021, 11, 1)),
        ("2020-2-SCI-005", 10, [{"night": date(2021, 5, 1)}], date(2022, 9, 1)),
        ("2020-2-SCI-005", 0, [{"night": date(2021, 8, 2)}], date(2021, 11, 1)),
        ("2020-2-SCI-005", 10, [{"night": date(2021, 8, 2)}], date(2022, 9, 1)),
        ("2020-2-SCI-005", 0, [{"night": date(2021, 10, 31)}], date(2021, 11, 1)),
        ("2020-2-SCI-005", 10, [{"night": date(2021, 10, 31)}], date(2022, 9, 1)),
        (
            "2020-2-SCI-005",
            0,
            [
                {"night": date(2021, 12, 20)},
                {"night": date(2021, 6, 1)},
                {"night": date(2021, 6, 24)},
                {"night": date(2021, 6, 23)},
                {"night": date(2021, 12, 2)},
            ],
            date(2022, 5, 1),
        ),
        (
            "2020-2-SCI-005",
            10,
            [
                {"night": date(2021, 12, 20)},
                {"night": date(2021, 6, 1)},
                {"night": date(2021, 6, 24)},
                {"night": date(2021, 6, 23)},
                {"night": date(2021, 12, 2)},
            ],
            date(2023, 3, 1),
        ),
    ],
)
def test_data_release_date_return_correct_release_date(
    proposal_code: str,
    proprietary_period: int,
    block_visits: List[Dict[str, Any]],
    expected_date: datetime,
    db_connection: Connection,
) -> None:
    proposal_repository = ProposalRepository(db_connection)

    assert (
        proposal_repository._data_release_date(proprietary_period, block_visits)
        == expected_date
    )


def mocked_settings(original_settings: Settings, proposals_dir: Path) -> Settings:
    settings = original_settings.copy()
    settings.proposals_dir = proposals_dir
    return settings


def test_phase_1_and_2_proposals_have_a_summary_url(db_connection: Connection) -> None:
    proposal_repository = ProposalRepository(db_connection)

    proposal = proposal_repository.get("2022-1-SCI-008")
    assert proposal["phase1_proposal_summary"] is not None


def test_phase_2_only_proposals_have_no_summary_url(db_connection: Connection) -> None:
    proposal_repository = ProposalRepository(db_connection)

    proposal = proposal_repository.get("2022-1-DDT-001")
    assert proposal["phase1_proposal_summary"] is None


@pytest.mark.parametrize(
    "proposal_code,expected_current_version",
    [("2021-2-LSP-001", 2), ("2020-1-DDT-001", None)],
)
def test_current_phase1_version(
    proposal_code: str, expected_current_version: int, db_connection: Connection
) -> None:
    proposal_repository = ProposalRepository(db_connection)

    assert (
        proposal_repository.get_current_phase1_version(proposal_code)
        == expected_current_version
    )


@pytest.mark.parametrize(
    "proposal_code,current_version,expected_path",
    [
        ("2022-2-SCI-007", 1, "2022-2-SCI-007/1/Summary.pdf"),
        ("2021-2-LSP-001", 2, "2021-2-LSP-001/2/Summary.pdf"),
    ],
)
def test_get_phase1_summary(
    proposal_code: str,
    current_version: int,
    expected_path: str,
    db_connection: Connection,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Fake the proposals directory
    proposals_dir = tmp_path
    original_settings = get_settings()
    mock_settings = mocked_settings(original_settings, proposals_dir)
    monkeypatch.setattr(
        saltapi.repository.proposal_repository,
        "get_settings",
        lambda: mock_settings,
    )

    # Create the phase 1 summary
    if current_version:
        proposal_dir = proposals_dir / proposal_code
        proposal_dir.mkdir()
        submission_dir = proposals_dir / proposal_code / str(current_version)
        submission_dir.mkdir()
        proposal_file = submission_dir / "Summary.pdf"
        proposal_file.write_text("Fake pdf")

    proposal_repository = ProposalRepository(db_connection)

    path = proposals_dir / Path(expected_path)
    assert proposal_repository.get_phase1_summary(proposal_code) == path


@pytest.mark.parametrize("proposal_code", ["2018-2-LSP-001", "2020-2-DDT-001"])
def test_get_phase1_summary_raises_not_found_error(
    proposal_code: str,
    db_connection: Connection,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    proposal_repository = ProposalRepository(db_connection)

    with pytest.raises(NotFoundError):
        proposal_repository.get_phase1_summary(proposal_code)


@pytest.mark.parametrize(
    "proposal_code,last_submission,expected_path",
    [
        ("2018-2-LSP-001", 440, "2018-2-LSP-001/440/2018-2-LSP-001.zip"),
        ("2020-1-DDT-001", 1, "2020-1-DDT-001/1/2020-1-DDT-001.zip"),
    ],
)
def test_get_proposal_file(
    proposal_code: str,
    last_submission: int,
    expected_path: str,
    db_connection: Connection,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Fake the proposals directory
    proposals_dir = tmp_path
    original_settings = get_settings()
    mock_settings = mocked_settings(original_settings, proposals_dir)
    monkeypatch.setattr(
        saltapi.repository.proposal_repository,
        "get_settings",
        lambda: mock_settings,
    )

    # Create the proposal file
    proposal_dir = proposals_dir / proposal_code
    proposal_dir.mkdir()
    submission_dir = proposals_dir / proposal_code / str(last_submission)
    submission_dir.mkdir()
    proposal_file = submission_dir / f"{proposal_code}.zip"
    proposal_file.write_text("Fake zip")

    proposal_repository = ProposalRepository(db_connection)

    path = proposals_dir / Path(expected_path)
    assert proposal_repository.get_proposal_file(proposal_code) == path


@pytest.mark.parametrize("proposal_code", ["2018-2-LSP-001", "2020-2-DDT-001"])
def test_get_proposal_file_raises_not_found_error(
    proposal_code: str,
    db_connection: Connection,
) -> None:
    proposal_repository = ProposalRepository(db_connection)

    with pytest.raises(NotFoundError):
        proposal_repository.get_proposal_file(proposal_code)


@pytest.mark.parametrize(
    "proposal_code,semesters",
    [
        ("2020-2-SCI-043", []),
        ("2020-2-SCI-018", ["2020-2"]),
        ("2019-2-MLT-001", ["2019-2", "2020-1", "2020-2"]),
    ],
)
def test_get_progress_report_semesters(
    proposal_code: str, semesters: List[str], db_connection: Connection
) -> None:
    proposal_repository = ProposalRepository(db_connection)
    assert proposal_repository.get_progress_report_semesters(proposal_code) == semesters


def test_put_progress_report_handles_missing_partners(
    db_connection: Connection,
) -> None:
    def dict_to_requested_percentages(
        percentages_dict: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        return [
            {
                "partner_code": partner_code,
                "requested_percentage": percentages_dict[partner_code],
            }
            for partner_code in percentages_dict
        ]

    def requested_percentages_to_dict(
        percentages: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        return {p["partner_code"]: p["requested_percentage"] for p in percentages}

    # Initially request time from all partners
    proposal_code = "2021-2-LSP-001"
    semester = "2022-2"
    initial_percentages_dict = {
        "UW": 20.0,
        "RSA": 20.0,
        "UKSC": 20.0,
        "POL": 20.0,
        "IUCAA": 20.0,
        "OTH": 0,
    }
    progress = {
        "requested_time": 4200,
        "maximum_seeing": 2,
        "transparency": "Thin cloud",
        "description_of_observing_constraints": 'Thin/thick cloud and 2-3" seeing.',
        "change_reason": "N/A",
        "summary_of_proposal_status": "See attached.",
        "strategy_changes": "None",
        "partner_requested_percentages": dict_to_requested_percentages(
            initial_percentages_dict
        ),
    }
    proposal_repository = ProposalRepository(db_connection)
    proposal_repository.put_proposal_progress(
        progress,
        proposal_code,
        semester,
        {"proposal_progress_filename": None, "additional_pdf_filename": None},
    )

    # The percentages should have been stored
    saved_progress = proposal_repository.get_progress_report(proposal_code, semester)
    assert (
        requested_percentages_to_dict(saved_progress["partner_requested_percentages"])
        == initial_percentages_dict
    )

    # Now request time from two partners only
    progress["partner_requested_percentages"] = dict_to_requested_percentages(
        {"RSA": 50.0, "IUCAA": 50.0}
    )
    proposal_repository.put_proposal_progress(
        progress,
        proposal_code,
        semester,
        {"proposal_progress_filename": None, "additional_pdf_filename": None},
    )

    # The percentages should be 0 for all the "missing" partners
    saved_progress = proposal_repository.get_progress_report(proposal_code, semester)
    assert requested_percentages_to_dict(
        saved_progress["partner_requested_percentages"]
    ) == {
        "UW": 0,
        "RSA": 50.0,
        "UKSC": 0,
        "POL": 0,
        "IUCAA": 50.0,
        "OTH": 0,
    }


@pytest.mark.parametrize(
    "proposal_code,proposal_code_id",
    [
        ("2020-2-SCI-043", 2753),
        ("2020-2-SCI-018", 2708),
        ("2019-2-MLT-001", 2557),
    ],
)
def test_get_proposal_code_id_returns_correct_id(
    proposal_code: str, proposal_code_id: int, db_connection: Connection
) -> None:
    proposal_repository = ProposalRepository(db_connection)
    assert proposal_repository.get_proposal_code_id(proposal_code) == proposal_code_id


def test_get_proposal_code_id_raises_error_for_none_existing_proposal_code(
    db_connection: Connection,
) -> None:
    proposal_repository = ProposalRepository(db_connection)
    with pytest.raises(NotFoundError):
        proposal_repository.get_proposal_code_id("2023-1-NOT-CODE-001")
