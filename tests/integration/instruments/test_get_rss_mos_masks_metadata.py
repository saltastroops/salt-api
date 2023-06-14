import pytest
from fastapi.testclient import TestClient
from starlette import status

from tests.conftest import authenticate, not_authenticated, find_username

RSS_MOS_MASKS_METADATA_URL = "/rss/mos-mask-metadata"

def test_get_mos_masks_metadata_requires_authentication(
        client: TestClient,
) -> None:
    barcode = "P000127N03"

    not_authenticated(client)
    response = client.get(RSS_MOS_MASKS_METADATA_URL + "/")
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize(
    "from_semester, to_semester",
    [
        ("2022-1", "2021-2"),
        ("2020-1", "2019-2"),
        ("2022-2", "2020-1"),
    ],
)
def test_get_mos_masks_metadata_requires_start_semester_not_later_than_end_semester(
        from_semester: str, to_semester: str, client: TestClient
) -> None:
    username = find_username("Administrator")
    authenticate(username, client)
    response = client.get(RSS_MOS_MASKS_METADATA_URL + "/", params={
        "from": from_semester,
        "to": to_semester,
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.parametrize(
    "from_semester, to_semester",
    [
        ("abc", "2021-2"),
        ("2", "2019-2"),
        ("2022", "2020-1"),
        ("2020-1", "2021-3"),
        ("2020-1", "abc"),
    ],
)
def test_get_mos_masks_metadata_requires_valid_semesters(
        from_semester: str, to_semester: str, client: TestClient
) -> None:
    username = find_username("Administrator")
    authenticate(username, client)
    response = client.get(RSS_MOS_MASKS_METADATA_URL + "/", params={
        "from": from_semester,
        "to": to_semester,
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "username,from_semester,to_semester,mos_masks_count",
    [
        [
            find_username("TAC Chair", partner_code="RSA"),
            "2020-1",
            "2020-1",
            114
        ],
        [
            find_username("TAC Chair", partner_code="RU"),
            "2021-1",
            "2021-1",
            119,
        ],
        [
            find_username("Principal Investigator", proposal_code="2014-2-SCI-078"),
            "2020-2",
            "2020-2",
            127,
        ],
        [
            find_username("Principal Investigator", proposal_code="2018-2-LSP-001"),
            "2017-2",
            "2021-1",
            756,
        ],
        [find_username("SALT Astronomer"), "2016-1", "2022-2", 1193],
        [find_username("Administrator"), "2018-2", "2018-2", 56],
        [
            find_username("Principal Investigator", proposal_code="2014-2-SCI-078"),
            "2018-2",
            "2019-1",
            106,
        ],
    ],
)
def test_get_mos_masks_metadata(
    username: str,
    from_semester: str,
    to_semester: str,
    mos_masks_count: int,
    client: TestClient,
) -> None:

    username = find_username("Administrator")
    authenticate(username, client)
    response = client.get(RSS_MOS_MASKS_METADATA_URL + "/", params={
        "from": from_semester,
        "to": to_semester
    })
    assert response.status_code == status.HTTP_200_OK

    mos_masks_metadata = response.json()
    assert len(mos_masks_metadata) == mos_masks_count

    for mos in mos_masks_metadata:
        assert "cut_by" in mos
        assert "cut_date" in mos
        assert "mask_comment" in mos
