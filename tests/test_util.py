from typing import Tuple

import freezegun
import pytest
from dateutil.parser import parse

from saltapi.util import (
    TimeInterval,
    next_semester,
    parse_partner_requested_percentages,
    partner_name,
    semester_end,
    semester_of_datetime,
    semester_start,
    tonight,
)


@pytest.mark.parametrize(
    "partner_code,name",
    [
        ("AMNH", "American Museum of Natural History"),
        ("IUCAA", "Inter-University Centre for Astronomy & Astrophysics"),
        ("RSA", "South Africa"),
    ],
)
def test_partner_name_returns_name(partner_code: str, name: str) -> None:
    assert partner_name(partner_code) == name


@pytest.mark.parametrize(
    "now,start,end",
    [
        ("2021-05-19T11:59:59Z", "2021-05-18T12:00:00Z", "2021-05-19T12:00:00Z"),
        ("2021-11-07T12:00:00Z", "2021-11-07T12:00:00Z", "2021-11-08T12:00:00Z"),
        ("2021-10-31T12:00:01Z", "2021-10-31T12:00:00Z", "2021-11-01T12:00:00Z"),
        ("2021-11-07T23:00:00Z", "2021-11-07T12:00:00Z", "2021-11-08T12:00:00Z"),
        ("2021-01-01T01:00:00Z", "2020-12-31T12:00:00Z", "2021-01-01T12:00:00Z"),
    ],
)
def test_tonight(now: str, start: str, end: str) -> None:
    with freezegun.freeze_time(now):
        assert tonight() == TimeInterval(start=parse(start), end=parse(end))


@pytest.mark.parametrize(
    "t,semester",
    [
        ("2022-05-01T11:59:59Z", "2021-2"),
        ("2022-05-01T12:00:00Z", "2022-1"),
        ("2022-05-01T12:00:01Z", "2022-1"),
        ("2021-11-01T11:59:59Z", "2021-1"),
        ("2023-11-01T12:00:00Z", "2023-2"),
        ("2023-11-01T12:00:01Z", "2023-2"),
        ("2022-03-15T07:14:45Z", "2021-2"),
        ("2021-08-09T14:15:56Z", "2021-1"),
        ("2025-12-31T08:16:24Z", "2025-2"),
        ("2020-05-01T13:59:59+02:00", "2019-2"),
        ("2020-05-01T14:01:01+02:00", "2020-1"),
    ],
)
def test_semester_of_datetime_returns_semester(t: str, semester: str) -> None:
    d = parse(t)
    assert semester_of_datetime(d) == semester


def test_semester_of_datetime_requires_utc_datetimes() -> None:
    d = parse("2021-07-14T14:56:13")
    with pytest.raises(ValueError):
        semester_of_datetime(d)


@pytest.mark.parametrize(
    "semester,start",
    [("2019-1", "2019-05-01T12:00:00Z"), ("2021-2", "2021-11-01T12:00:00Z")],
)
def test_semester_start_returns_correct_datetime(semester: str, start: str) -> None:
    d = parse(start)
    assert semester_start(semester) == d


def test_semester_start_raises_error_for_incorrect_semester() -> None:
    with pytest.raises(ValueError):
        semester_start("2021-3")


@pytest.mark.parametrize(
    "semester,end",
    [("2019-1", "2019-11-01T12:00:00Z"), ("2021-2", "2022-05-01T12:00:00Z")],
)
def test_semester_end_returns_correct_datetime(semester: str, end: str) -> None:
    d = parse(end)
    assert semester_end(semester) == d


def test_semester_end_raises_error_for_incorrect_semester() -> None:
    with pytest.raises(ValueError):
        semester_end("2021-3")


@pytest.mark.parametrize(
    "current_semester", ["invalid", "2020.4-2", "2022-1.9", "2023-3"]
)
def test_next_semester_raises_error_for_incorrect_semester(
    current_semester: str,
) -> None:
    with pytest.raises(ValueError):
        next_semester(current_semester)


@pytest.mark.parametrize(
    "semester,d",
    [
        ("2019-2", "2019-09-05T12:00:00Z"),
        ("2022-1", "2022-02-01T12:00:00Z"),
        ("2022-1", "2022-03-11T12:00:00Z"),
        ("2022-2", "2022-06-23T12:00:00Z"),
        ("2023-1", "2023-04-30T12:00:00Z"),
        # Test if the start of the first semester is correct
        ("2022-1", "2022-05-01T00:00:00Z"),
        ("2022-1", "2022-05-01T11:59:59Z"),
        ("2022-2", "2022-05-01T12:00:00Z"),
        ("2022-2", "2022-05-01T12:00:01Z"),
        # Test if start of the second semester is correct.
        ("2022-2", "2022-11-01T00:00:01Z"),
        ("2022-2", "2022-11-01T11:59:59Z"),
        ("2023-1", "2022-11-01T12:00:00Z"),
        ("2023-1", "2022-11-01T12:00:01Z"),
        # Test the last date of the start/end semester month
        ("2022-2", "2022-05-31T00:00:00Z"),
        ("2022-2", "2022-05-31T11:59:59Z"),
        ("2022-2", "2022-05-31T12:00:00Z"),
        ("2022-1", "2022-04-30T00:00:01Z"),
        ("2022-1", "2022-04-30T12:00:01Z"),
        ("2022-2", "2022-10-31T00:00:00Z"),
        ("2022-2", "2022-10-31T12:00:00Z"),
        ("2022-2", "2022-10-31T12:00:01Z"),
    ],
)
def test_next_semester_returns_correct_semester_without_semester_argument(
    semester: str, d: str
) -> None:
    with freezegun.freeze_time(d):
        assert next_semester() == semester


@pytest.mark.parametrize(
    "semester,d,current_semester",
    [
        ("2018-2", "2019-09-05T12:00:00Z", "2018-1"),
        ("2022-1", "2022-02-01T12:00:00Z", "2021-2"),
        ("2022-1", "2024-02-01T12:00:00Z", "2021-2"),
    ],
)
def test_next_semester_returns_correct_semester_with_semester_argument(
    semester: str, d: str, current_semester: str
) -> None:
    with freezegun.freeze_time(d):
        assert next_semester(current_semester) == semester


@pytest.mark.parametrize(
    "value",
    [
        # no value - hence the values don't add up to 100%
        "",
        # invalid value
        "RSA:OTH:100",
        # unknown partner code
        "UNKNOWN:100",
        # invalid float value
        "RSA:8e",
        # negative float value
        "RSA:-3;IUCAA:53;UKSC:50",
        # values don't add up to 100%
        "RSA:99",
        # values don't add up to 100%
        "RSA:101",
        # values don't add up to 100%
        "RSA:33;DC:66"
        # values don't add up to 100%
        "RSA:50;POL:50.5",
    ],
)
def test_parse_partner_requested_percentages_fails_for_invalid_values(
    value: str,
) -> None:
    with pytest.raises(ValueError):
        parse_partner_requested_percentages(value)


@pytest.mark.parametrize(
    "value,percentages",
    [
        ("RSA:100", (("RSA", 100),)),
        (
            "IUCAA:5.8;UKSC:94.2",
            (
                ("IUCAA", 5.8),
                ("UKSC", 94.2),
            ),
        ),
        (" RSA : 0 ; DC : 90 ; IUCAA : 10", (("RSA", 0), ("DC", 90), ("IUCAA", 10))),
    ],
)
def test_parse_partner_requested_percentages(
    value: str, percentages: Tuple[Tuple[str, float], ...]
) -> None:
    expected_percentages = [
        {"partner_code": partner_code, "requested_percentage": percentage}
        for partner_code, percentage in percentages
    ]
    assert parse_partner_requested_percentages(value) == expected_percentages
