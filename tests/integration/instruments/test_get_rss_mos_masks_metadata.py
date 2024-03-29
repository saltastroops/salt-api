from typing import Any, Callable

import pytest
from fastapi.testclient import TestClient
from starlette import status

from tests.conftest import authenticate, find_username, not_authenticated

RSS_MOS_MASKS_METADATA_URL = "/rss/mos-mask-metadata"


def test_get_mos_masks_metadata_requires_authentication(
    client: TestClient,
) -> None:
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
    response = client.get(
        RSS_MOS_MASKS_METADATA_URL + "/",
        params={
            "from": from_semester,
            "to": to_semester,
        },
    )
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
    response = client.get(
        RSS_MOS_MASKS_METADATA_URL + "/",
        params={
            "from": from_semester,
            "to": to_semester,
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "from_semester,to_semester,mos_masks_count",
    [
        ["2020-1", "2020-1", 114],
        [
            "2021-1",
            "2021-1",
            119,
        ],
        [
            "2020-2",
            "2020-2",
            127,
        ],
        [
            "2017-2",
            "2021-1",
            756,
        ],
        ["2016-1", "2022-2", 1193],
        ["2018-2", "2018-2", 56],
        [
            "2018-2",
            "2019-1",
            106,
        ],
    ],
)
def test_get_mos_masks_metadata(
    from_semester: str,
    to_semester: str,
    mos_masks_count: int,
    client: TestClient,
    check_data: Callable[[Any], None],
) -> None:
    username = find_username("Administrator")
    authenticate(username, client)
    response = client.get(
        RSS_MOS_MASKS_METADATA_URL + "/",
        params={"from": from_semester, "to": to_semester},
    )
    assert response.status_code == status.HTTP_200_OK

    mos_masks_metadata = response.json()
    assert len(mos_masks_metadata) == mos_masks_count

    check_data(mos_masks_metadata)
