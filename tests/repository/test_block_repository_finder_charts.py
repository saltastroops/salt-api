import shutil
from pathlib import Path
from typing import List, Tuple

import pytest
from sqlalchemy.engine import Connection

import saltapi.repository.block_repository
from saltapi.settings import Settings, get_settings
from tests.repository.test_block_repository import create_block_repository


def mocked_settings(original_settings: Settings, proposals_dir: Path) -> Settings:
    settings = original_settings.copy()
    settings.proposals_dir = proposals_dir
    return settings


def setup_finder_chart_files(
    proposals_dir: Path,
    proposal_code: str,
    finder_chart_name: str,
    original_suffixes: List[str],
    thumbnail_suffixes: List[str],
) -> None:
    included_dir = proposals_dir / proposal_code / "Included"
    included_dir.mkdir(parents=True)

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
                Path(__file__).parent.parent
                / "integration"
                / "finder_charts"
                / f"finder_chart.{suffix}"
            )
            finder_chart = included_dir / f"{prefix}{finder_chart_name}.{suffix}"
            shutil.copy(finder_chart_template, finder_chart)
            print(finder_chart)
        else:
            pytest.fail(f"Unsupported file suffix in test setup: {suffix}")

    for suffix in original_suffixes:
        setup_finder_chart(suffix, "original")
    for suffix in thumbnail_suffixes:
        setup_finder_chart(suffix, "thumbnail")


@pytest.mark.parametrize(
    "suffixes",
    [
        ([], []),
        (["png"], []),
        ([], ["jpg"]),
        (["png"], ["png"]),
        (["pdf", "png"], ["jpg", "png"]),
    ],
)
def test_should_return_correct_finder_charts(
    suffixes: Tuple[List[str], List[str]],
    db_connection: Connection,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    original_suffixes, thumbnail_suffixes = suffixes
    block_repository = create_block_repository(db_connection)

    # Get a temporary proposals directory
    proposals_dir = tmp_path
    original_settings = get_settings()
    mock_settings = mocked_settings(original_settings, proposals_dir)
    monkeypatch.setattr(
        saltapi.repository.block_repository, "get_settings", lambda: mock_settings
    )

    # Create the finder_chart_files
    finder_chart_name = "2a0bd9fae69a1d89a00e0dd5361d2a0f"
    setup_finder_chart_files(
        proposals_dir=proposals_dir,
        proposal_code="2022-1-DDT-005",
        finder_chart_name=finder_chart_name,
        original_suffixes=original_suffixes,
        thumbnail_suffixes=thumbnail_suffixes,
    )

    # Get the finder chart...
    finder_chart_id = 182648
    block_id = 93455
    block = block_repository.get(block_id)
    finder_charts = block["observations"][0]["finder_charts"]
    if finder_charts[0]["id"] == finder_chart_id:
        finder_chart = finder_charts[0]
    else:
        finder_chart = finder_charts[1]

    # ... and check the files
    files = finder_chart["files"]
    assert len(files) == len(original_suffixes) + len(thumbnail_suffixes)
    for suffix in original_suffixes:
        assert {
            "size": "original",
            "url": f"/finder-charts/{finder_chart_id}.{suffix}",
        } in files
    for suffix in thumbnail_suffixes:
        assert {
            "size": "thumbnail",
            "url": f"/finder-charts/{finder_chart_id}-thumbnail.{suffix}",
        } in files
