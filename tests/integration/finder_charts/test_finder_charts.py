from itertools import product
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from starlette import status

import saltapi.service.finder_chart_service
from saltapi.settings import Settings, get_settings
from tests.conftest import (
    authenticate,
    not_authenticated,
    setup_finder_chart_files,
)

FINDER_CHART_URL = "/finder-charts"

USERNAME = "cmofokeng"


def mocked_settings(original_settings: Settings, proposals_dir: Path) -> Settings:
    settings = original_settings.copy()
    settings.proposals_dir = proposals_dir
    return settings


def test_get_finder_chart_returns_401_for_non_authenticated_user(
    client: TestClient,
) -> None:
    not_authenticated(client)
    response = client.get(FINDER_CHART_URL + "/" + str(1))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_finder_chart_returns_403_for_non_authorised_user(
    client: TestClient,
) -> None:
    authenticate("TestUser", client)
    response = client.get(FINDER_CHART_URL + "/" + str(1))

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize(
    "size,suffix", product(["original", "thumbnail"], ["jpg", "pdf", "png"])
)
def test_get_returns_finder_chart_for_authorised_user(
    size: str,
    suffix: str,
    client: TestClient,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    finder_chart_id = 55345
    finder_chart_name = "FindingChart_1445723219288"
    proposal_code = "2015-2-SCI-028"

    proposals_dir = tmp_path
    original_settings = get_settings()
    mock_settings = mocked_settings(original_settings, proposals_dir)
    monkeypatch.setattr(
        saltapi.service.finder_chart_service,
        "get_settings",
        lambda: mock_settings,
    )

    # Create the required finder chart file
    original_suffixes = []
    thumbnail_suffixes = []
    url = ""
    if size == "original":
        original_suffixes = [suffix]
        url = f"{FINDER_CHART_URL}/{finder_chart_id}.{suffix}"
    elif size == "thumbnail":
        thumbnail_suffixes = [suffix]
        url = f"{FINDER_CHART_URL}/{finder_chart_id}-thumbnail.{suffix}"
    else:
        pytest.fail(f"Unsupported size: {size}")
    created_files = setup_finder_chart_files(
        proposals_dir=proposals_dir,
        proposal_code=proposal_code,
        parent_dirs=["4", "Included"],
        finder_chart_name=finder_chart_name,
        original_suffixes=original_suffixes,
        thumbnail_suffixes=thumbnail_suffixes,
    )

    # Store the created file content for later use
    finder_chart_content = created_files[0].read_bytes()

    authenticate(USERNAME, client)

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.content == finder_chart_content


def test_get_finder_chart_returns_404_for_wrong_finding_chart_id(
    client: TestClient,
) -> None:
    authenticate(USERNAME, client)
    finder_chart_id = 0

    response = client.get(FINDER_CHART_URL + "/" + str(finder_chart_id) + ".png")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_finder_chart_returns_404_for_wrong_finding_chart_size(
    client: TestClient,
) -> None:
    authenticate(USERNAME, client)

    response = client.get(FINDER_CHART_URL + "/55345-extralarge.pdf")

    assert response.status_code == status.HTTP_404_NOT_FOUND
