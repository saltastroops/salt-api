from datetime import date
from unittest.mock import MagicMock

from get_proposals_by_release_date import (
    calculate_release_date_for_proposal,
    get_proposals_in_release_date_range,
)


def test_calculate_release_date_with_block_visits() -> None:
    repo = MagicMock()
    # Visits with latest observation on 2021-12-20
    # Semester of 2021-12-20 is 2021-2 (ending on 2022-04-30 / 2022-05-01)
    # Proprietary period = 10 months -> 2023-03-01
    repo.block_visits.return_value = [
        {"night": date(2021, 6, 1)},
        {"night": date(2021, 12, 20)},
        {"night": date(2021, 12, 2)},
    ]
    release_date = calculate_release_date_for_proposal(
        repo=repo,
        proposal_code="2020-2-SCI-005",
        proprietary_period=10,
    )
    assert release_date == date(2023, 3, 1)


def test_calculate_release_date_without_block_visits() -> None:
    repo = MagicMock()
    repo.block_visits.return_value = []
    # If no block visits, reference_date date(2026, 10, 30) is in semester 2026-1 (which ends 2026-11-01)
    # With proprietary period = 0 -> 2026-11-01
    release_date = calculate_release_date_for_proposal(
        repo=repo,
        proposal_code="2026-1-ENG-001",
        proprietary_period=0,
        reference_date=date(2026, 10, 30),
    )
    assert release_date == date(2026, 11, 1)


def test_get_proposals_in_release_date_range(monkeypatch) -> None:
    # Setup mock connection and proposal repository
    mock_conn = MagicMock()
    mock_repo = MagicMock()

    mock_proposals_info = [
        {
            "proposal_code": "2024-1-SCI-001",
            "proprietary_period": 12,
        },  # release in range
        {
            "proposal_code": "2020-1-SCI-002",
            "proprietary_period": 12,
        },  # release in past
        {
            "proposal_code": "2026-1-SCI-003",
            "proprietary_period": 24,
        },  # release in future
        {"proposal_code": "2026-1-SCI-004", "proprietary_period": None},  # None period
    ]

    monkeypatch.setattr(
        "get_proposals_by_release_date.get_all_proposals_with_proprietary_info",
        lambda conn: mock_proposals_info,
    )
    monkeypatch.setattr(
        "get_proposals_by_release_date.ProposalRepository",
        lambda conn: mock_repo,
    )

    # For 2024-1-SCI-001: observation on 2025-08-10 (semester 2025-1 -> ends 2025-11-01) + 12 months -> 2026-11-01
    # For 2020-1-SCI-002: observation on 2020-08-10 (semester 2020-1 -> ends 2020-11-01) + 12 months -> 2021-11-01
    # For 2026-1-SCI-003: observation on 2026-08-10 (semester 2026-1 -> ends 2026-11-01) + 24 months -> 2028-11-01
    def mock_block_visits(proposal_code):
        if proposal_code == "2024-1-SCI-001":
            return [{"night": date(2025, 8, 10)}]
        if proposal_code == "2020-1-SCI-002":
            return [{"night": date(2020, 8, 10)}]
        if proposal_code == "2026-1-SCI-003":
            return [{"night": date(2026, 8, 10)}]
        return []

    mock_repo.block_visits.side_effect = mock_block_visits

    from_date = date(2026, 10, 30)
    to_date = date(2026, 12, 31)

    result = get_proposals_in_release_date_range(
        connection=mock_conn,
        from_date=from_date,
        to_date=to_date,
    )

    assert len(result) == 1
    assert result[0]["proposal_code"] == "2024-1-SCI-001"
    assert result[0]["release_date"] == date(2026, 11, 1)
    assert result[0]["proprietary_period"] == 12


def test_calculate_release_date_none_proprietary_period() -> None:
    repo = MagicMock()
    release_date = calculate_release_date_for_proposal(
        repo=repo,
        proposal_code="2026-1-SCI-001",
        proprietary_period=None,
    )
    assert release_date is None
