import pathlib
from typing import Any, Callable, NamedTuple

import pytest
from fastapi.testclient import TestClient
from starlette import status

from tests.conftest import authenticate, find_username

PROGRESS_REPORT_URL = "/progress"


def _prepare_settings_and_summary(
    proposal_code: str, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    class MockSettings(NamedTuple):
        proposals_dir: pathlib.Path

    def mock_get_settings() -> Any:
        return MockSettings(pathlib.Path(tmp_path))

    monkeypatch.setattr(
        "saltapi.service.proposal_service.get_settings", mock_get_settings
    )

    proposal_dir = mock_get_settings().proposals_dir / proposal_code
    included_dir = proposal_dir / "Included"
    # The included directory must exist as the generated progress report is stored in
    # that directory.
    included_dir.mkdir(parents=True)
    submission_version_dir = proposal_dir / "1"
    submission_version_dir.mkdir(parents=True)

    summary_pdf: pathlib.Path = submission_version_dir / "Summary.pdf"
    fake_summary_pdf = pathlib.Path.cwd() / "tests" / "data" / "summary.pdf"
    summary_pdf.write_bytes(fake_summary_pdf.read_bytes())


def test_submit_progress_report(
    check_data: Callable[[Any], None],
    client: TestClient,
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    proposal_code = "2018-2-SCI-020"
    _prepare_settings_and_summary(proposal_code, tmp_path, monkeypatch)

    data = {
        "requested_time": 4200,
        "maximum_seeing": 2,
        "transparency": "Thin cloud",
        "description_of_observing_constraints": 'Thin/thick cloud and 2-3" seeing.',
        "change_reason": "N/A",
        "summary_of_proposal_status": "See attached.",
        "strategy_changes": "None",
        "partner_requested_percentages": "RSA:100;UKSC:0;RU:0",
    }
    username = find_username("administrator")
    authenticate(username, client)

    response = client.put(
        PROGRESS_REPORT_URL + "/" + proposal_code + "/2020-2", data=data
    )
    assert response.status_code == status.HTTP_200_OK

    response = client.get(PROGRESS_REPORT_URL + "/" + proposal_code + "/2020-2")
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    # The filename changes with every test run
    del response_data["proposal_progress_pdf"]
    check_data(response_data)


def test_submit_progress_report_repeatedly(
    check_data: Callable[[Any], None],
    client: TestClient,
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    proposal_code = "2018-2-SCI-020"
    _prepare_settings_and_summary(proposal_code, tmp_path, monkeypatch)

    data = {
        "requested_time": 4200,
        "maximum_seeing": 2,
        "transparency": "Thin cloud",
        "description_of_observing_constraints": 'Thin/thick cloud and 2-3" seeing.',
        "change_reason": "N/A",
        "summary_of_proposal_status": "See attached.",
        "strategy_changes": "None",
        "partner_requested_percentages": "RSA:100;UKSC:0;RU:0",
    }
    username = find_username("administrator")
    authenticate(username, client)

    response = client.put(
        PROGRESS_REPORT_URL + "/" + proposal_code + "/2020-2", data=data
    )
    assert response.status_code == status.HTTP_200_OK

    response = client.get(PROGRESS_REPORT_URL + "/" + proposal_code + "/2020-2")
    first_response_data = response.json()
    # The filename changes with every test run
    del first_response_data["proposal_progress_pdf"]

    # Submitting a progress report is idempotent.
    response = client.put(
        PROGRESS_REPORT_URL + "/" + proposal_code + "/2020-2", data=data
    )
    assert response.status_code == status.HTTP_200_OK

    response = client.get(PROGRESS_REPORT_URL + "/" + proposal_code + "/2020-2")
    second_response_data = response.json()
    assert response.status_code == status.HTTP_200_OK
    del second_response_data["proposal_progress_pdf"]
    assert second_response_data == first_response_data

    # Resubmitting with different data updates the request
    updated_data = {
        "requested_time": 11000,
        "maximum_seeing": 3,
        "transparency": "Thick cloud",
        "description_of_observing_constraints": 'Thick cloud and 3" seeing.',
        "change_reason": "Previous data suggests the conditions may be relaxed.",
        "summary_of_proposal_status": "All going well.",
        "strategy_changes": (
            "Relax the observing conditions to increase the observation probability."
        ),
        "partner_requested_percentages": "RSA:33;UKSC:1;RU:64",
    }
    response = client.put(
        PROGRESS_REPORT_URL + "/" + proposal_code + "/2020-2", data=updated_data
    )
    assert response.status_code == status.HTTP_200_OK

    response = client.get(PROGRESS_REPORT_URL + "/" + proposal_code + "/2020-2")
    third_response_data = response.json()
    del third_response_data["proposal_progress_pdf"]
    assert response.status_code == status.HTTP_200_OK
    assert third_response_data != first_response_data
    check_data(third_response_data)
