"""Utility functions."""
import inspect
from datetime import datetime, timedelta
from typing import Any, Dict, List, NamedTuple, Optional, Type, cast

import pytz
from astropy.coordinates import Angle
from fastapi import Form
from pydantic import BaseModel

from saltapi.web.schema.common import PartnerCode


class TimeInterval(NamedTuple):
    start: datetime
    end: datetime


_partners = dict(
    AMNH="American Museum of Natural History",
    CMU="Carnegie Mellon University",
    DC="Dartmouth College",
    DUR="Durham University",
    GU="Georg-August-Universität Göttingen",
    HET="Hobby Eberly Telescope Board",
    IUCAA="Inter-University Centre for Astronomy & Astrophysics",
    ORP="OPTICON-Radionet Pilot",
    OTH="Other",
    POL="Poland",
    RSA="South Africa",
    RU="Rutgers University",
    UC="University of Canterbury",
    UKSC="UK SALT Consortium",
    UNC="University of North Carolina - Chapel Hill",
    UW="University of Wisconsin-Madison",
)


def partner_name(partner_code: str) -> str:
    """
    Return the partner name for a SALT partner code.
    """

    if partner_code not in _partners:
        raise ValueError(f"Unknown partner code: {partner_code}")

    return _partners[partner_code]


def tonight() -> TimeInterval:
    """
    Return the date interval corresponding to the "night" in which the current time
    lies.

    A night is defined to run from noon to noon.

    For example, for 11 July 2021 11:59:59 "tonight" would be the time interval from
    10 July 2021 12:00:00 to 11 July 2021 12:00. On the other hand, for 11 July 2021
    12:00:01 "tonight" would be the time interval from 11 July 2021 12:00:00 to 12 July
    2021 12:00:00.

    All times are in UTC.
    """
    now = datetime.now(tz=pytz.utc)
    if now.hour < 12:
        now -= timedelta(hours=24)

    start = datetime(now.year, now.month, now.day, 12, 0, 0, 0, tzinfo=pytz.utc)
    end = start + timedelta(hours=24)

    return TimeInterval(start, end)


def semester_start(semester: str) -> datetime:
    """
    Return the start datetime of a semester. The semester must be a string of the
    form "year-semester", such as "2020-2" or "2021-1". Semester 1 of a year starts
    on 1 May noon UTC, semester 2 starts on 1 November noon UTC.

    The returned datetime is in UTC.
    """

    year_str, sem_str = semester.split("-")
    year = int(year_str)
    sem = int(sem_str)
    if sem == 1:
        return datetime(year, 5, 1, 12, 0, 0, 0, tzinfo=pytz.utc)
    if sem == 2:
        return datetime(year, 11, 1, 12, 0, 0, 0, tzinfo=pytz.utc)

    raise ValueError(f"Unknown semester ({sem_str}:  The semester must be 1 or 2.")


def semester_end(semester: str) -> datetime:
    """
    Return the end datetime of a semester. The semester must be a string of the form
    "year-semester", such as "2020-2" or "2021-1". Semester 1 of a year ends on 1
    November noon UTC, semester ends 2 on 1 May noon UTC of the following year.

    The returned datetime is in UTC.
    """

    year_str, sem_str = semester.split("-")
    year = int(year_str)
    sem = int(sem_str)
    if sem == 1:
        return datetime(year, 11, 1, 12, 0, 0, 0, tzinfo=pytz.utc)
    if sem == 2:
        return datetime(year + 1, 5, 1, 12, 0, 0, 0, tzinfo=pytz.utc)

    raise ValueError(f"Unknown semester ({sem_str}:  The semester must be 1 or 2.")


def semester_of_datetime(t: datetime) -> str:
    """
    Return the semester in which a datetime lies.

    The semester is returned as a string of the form "year-semester", such as "2020-2"
    or "2021-1". Semester 1 of a year starts on 1 May noon UTC, semester 2 starts on
    1 November noon UTC.

    The given datetime must be timezone-aware.
    """
    if t.tzinfo is None:
        raise ValueError("The datetime must be timezone-aware")

    shifted = t.astimezone(pytz.utc) - timedelta(hours=12)

    if shifted.month < 5:
        year = shifted.year - 1
        semester = 2
    elif shifted.month < 11:
        year = shifted.year
        semester = 1
    else:
        year = shifted.year
        semester = 2

    return f"{year}-{semester}"


def next_semester(current_semester: Optional[str] = None) -> str:
    """
    Get the next semester.

    If the semester is specified, this is the semester following that semester.
    Otherwise, it is the semester following the semester of the current dae and time.
    """
    if current_semester is None:
        current_semester = semester_of_datetime(datetime.now(tz=pytz.utc))

    try:
        year_str, semester_str = current_semester.split("-")
        year = int(year_str.strip())
        semester = int(semester_str.strip())
        if semester == 1:
            semester = 2
        elif semester == 2:
            year += 1
            semester = 1
        else:
            raise ValueError(f"No such semester: {semester}")
        return f"{year}-{semester}"
    except ValueError:
        raise ValueError(f"Invalid semester string: {current_semester}")


def as_form(cls: Type[BaseModel]) -> Type[BaseModel]:
    """
    Adds an as_form class method to decorated models. The as_form class method
    can be used with FastAPI endpoints. The as_form decorator will convert the
    BaseModel to FormData.

    Reference:
     https://lightrun.com/answers/tiangolo-fastapi-multipartform-data-unable-to-parse-complex-types-in-a-request-form
    """
    new_params = [
        inspect.Parameter(
            field.alias,
            inspect.Parameter.POSITIONAL_ONLY,
            default=(Form(field.default) if not field.required else Form(...)),
            annotation=field.outer_type_,
        )
        for field in cls.__fields__.values()
    ]

    async def _as_form(**data) -> BaseModel:  # type: ignore
        return cls(**data)

    sig = inspect.signature(_as_form)
    sig = sig.replace(parameters=new_params)
    _as_form.__signature__ = sig  # type: ignore
    setattr(cls, "as_form", _as_form)
    return cls


def target_coordinates(row: Any) -> Optional[Dict[str, Any]]:
    if row.ra_h is None:
        return None

    ra = Angle(f"{row.ra_h}:{row.ra_m}:{row.ra_s} hours").degree
    dec = Angle(f"{row.dec_sign}{row.dec_d}:{row.dec_m}:{row.dec_s} degrees").degree

    if ra == 0 and dec == 0:
        return None

    return {
        "right_ascension": float(ra),
        "declination": float(dec),
        "equinox": float(row.equinox),
    }


def target_magnitude(row: Any) -> Optional[Dict[str, Any]]:
    if row.min_mag is None:
        return None

    return {
        "minimum_magnitude": float(row.min_mag),
        "maximum_magnitude": float(row.max_mag),
        "bandpass": row.bandpass,
    }


def target_type(row: Any) -> Optional[Dict[str, str]]:
    if row.target_sub_type is None:
        return None

    if row.target_type != "Unknown":
        return {"type": row.target_type, "subtype": row.target_sub_type}
    else:
        return {"type": "Unknown", "subtype": "Unknown"}


def target_proper_motion(row: Any) -> Optional[Dict[str, Any]]:
    if row.ra_dot is None or (row.ra_dot == 0 and row.dec_dot == 0):
        return None

    return {
        "right_ascension_speed": float(row.ra_dot),
        "declination_speed": float(row.dec_dot),
        "epoch": pytz.utc.localize(row.epoch),
    }


def target_period_ephemeris(row: Any) -> Optional[Dict[str, Any]]:
    if row.period is None:
        return None

    return {
        "zero_point": float(row.period_zero_point),
        "period": float(row.period),
        "period_change_rate": float(row.period_change_rate),
        "time_base": row.period_time_base,
    }


def normalised_hrs_mode(mode: str) -> str:
    modes = {
        "HIGH RESOLUTION": "High Resolution",
        "HIGH STABILITY": "High Stability",
        "INT CAL FIBRE": "Int Cal Fiber",
        "LOW RESOLUTION": "Low Resolution",
        "MEDIUM RESOLUTION": "Medium Resolution",
    }

    return modes[mode]


def parse_partner_requested_percentages(value: str) -> List[Dict[str, Any]]:
    """
    Extract the partner requested percentages from a string.

    The string must be of the form
    "PartnerCode1:Percentage1;PartnerCode1:Percentage1;...", where PartnerCode is a
    valid partner code and Percentage is a non-negative float. The percentages must add
    up to 100%.

    Examples of valid values are "RSA:100", "IUCAA:5.8;UKSC:94.2" and
    " RSA : 0 ; DC : 90 ; IUCAA : 10".
    """
    partner_requested_percentages = []
    partner_codes = [pc.value for pc in PartnerCode]
    for p in value.split(";"):
        prp = p.split(":", maxsplit=1)
        if len(prp) != 2:
            raise ValueError(f"Invalid value: {value}")

        partner_code = prp[0].strip()
        if partner_code not in partner_codes:
            raise ValueError(f"Unknown partner code: {partner_code}")

        percentage = float(prp[1])
        if percentage < 0:
            raise ValueError(f"Negative percentage: {percentage}")

        partner_requested_percentages.append(
            {"partner_code": partner_code, "requested_percentage": percentage}
        )

    percentages_total = cast(
        float, sum(prp["requested_percentage"] for prp in partner_requested_percentages)
    )
    if percentages_total < 99.999 or percentages_total > 100.001:
        raise ValueError(f"The percentages do not add up to 100%: {value}")

    return partner_requested_percentages
