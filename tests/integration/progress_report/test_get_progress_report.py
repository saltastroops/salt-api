from pathlib import Path

from fastapi.testclient import TestClient
from starlette import status

from saltapi.settings import get_settings
from tests.conftest import authenticate, not_authenticated

PROGRESS_REPORT_URL = "/progress"

USERNAME = "cmofokeng"

PROPOSALS_DIR = get_settings().proposals_dir


def test_get_progress_report_returns_401_for_non_authenticated_user(
    client: TestClient,
) -> None:
    semester = "2018-2"
    proposal_code = "2022-1-SCI-025"
    not_authenticated(client)
    response = client.get(PROGRESS_REPORT_URL + "/" + proposal_code + "/" + semester)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_progress_report_returns_403_for_non_authorised_user(
    client: TestClient,
) -> None:
    semester = "2018-2"
    proposal_code = "2022-1-SCI-025"
    authenticate("TestUser", client)
    response = client.get(PROGRESS_REPORT_URL + "/" + proposal_code + "/" + semester)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_progress_report_returns_404_for_wrong_proposal_code(
    client: TestClient,
) -> None:
    semester = "2022-1"
    proposal_code = "2099-1-SCI-001"
    authenticate(USERNAME, client)
    response = client.get(PROGRESS_REPORT_URL + "/" + proposal_code + "/" + semester)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_returns_progress_report_and_pdf_files_for_authorised_user(
    client: TestClient,
) -> None:
    semester = "2018-2"
    proposal_code = "2018-2-LSP-001"
    expected_progress_report_pdf_path = (
        "/Included/ProposalProgressReport-505998bf6cb6d910b7de8567c21e45f4.pdf"
    )
    expected_additional_progress_report_pdf_path = (
        "/Included/ProposalProgressSupplementary-0e5b27408c40240de7c1c42f9eef7805.pdf"
    )
    authenticate(USERNAME, client)

    response = client.get(PROGRESS_REPORT_URL + "/" + proposal_code + "/" + semester)

    proposal_progress_report = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert proposal_progress_report["semester"] == semester
    assert proposal_progress_report["proposal_progress_pdf"] is not None

    assert (
        proposal_code + "/" + semester + "/" + "report.pdf"
    ) in proposal_progress_report["proposal_progress_pdf"]
    assert (
        proposal_code + "/" + semester + "/" + "supplementary-report.pdf"
    ) in proposal_progress_report["additional_pdf"]

    try:
        progress_pdf_response = client.get(
            proposal_progress_report["proposal_progress_pdf"]
        )

        assert progress_pdf_response.headers[
            "content-disposition"
        ] == 'attachment; filename="{}"'.format(
            Path(expected_progress_report_pdf_path).name
        )
        assert progress_pdf_response.headers["content-type"] == "application/pdf"

        additional_pdf_response = client.get(proposal_progress_report["additional_pdf"])

        assert additional_pdf_response.headers[
            "content-disposition"
        ] == 'attachment; filename="{}"'.format(
            Path(expected_additional_progress_report_pdf_path).name
        )
        assert additional_pdf_response.headers["content-type"] == "application/pdf"

    except RuntimeError as excinfo:
        assert any(
            file_path
            in [
                expected_progress_report_pdf_path,
                expected_additional_progress_report_pdf_path,
            ]
            for file_path in excinfo.__str__()
        )


def test_get_returns_progress_report_and_no_pdf_files_for_authorised_user(
    client: TestClient,
) -> None:
    semester = "2022-1"
    proposal_code = "2022-1-SCI-025"
    authenticate(USERNAME, client)

    response = client.get(PROGRESS_REPORT_URL + "/" + proposal_code + "/" + semester)

    assert response.status_code == status.HTTP_200_OK

    proposal_progress_report = response.json()

    assert proposal_progress_report["semester"] == semester

    assert proposal_progress_report["proposal_progress_pdf"] is None

    assert proposal_progress_report["additional_pdf"] is None
