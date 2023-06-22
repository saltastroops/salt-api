from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from saltapi.web.schema.common import TargetCoordinates


class Magnitude(BaseModel):
    """Apparent magnitude (range)."""

    minimum_magnitude: float = Field(
        ...,
        title="Minimum magnitude",
        description="Minimum (brightest) apparent magnitude",
    )
    maximum_magnitude: float = Field(
        ...,
        title="Maximum magnitude",
        description="Maximum (faintest) apparent magnitude",
    )
    bandpass: str = Field(
        ..., title="Bandpass", description="Bandpass (filter) fore the magnitude"
    )


class TimeBase(str, Enum):
    BJD = "BJD"  # Barycentric Julian Date
    HJD = "HJD"  # Heliocentric Julian Date
    JD = "JD"  # Julian Date
    UT = "UT"  # Universal Time


class PeriodEphemeris(BaseModel):
    """Period ephemeris for a variable target."""

    zero_point: Decimal = Field(
        ...,
        title="Zero point for the ephemeris",
        description=(
            "Zero point for the target ephemeris. The target phase is 0 at this time"
        ),
    )
    period: Decimal = Field(
        ...,
        title="Target period",
        description="Period of the target at the zero point, in days",
    )
    period_change_rate: Decimal = Field(
        ...,
        title="Period change rate",
        description="Rate of change of the period, in days per day",
    )
    time_base: TimeBase = Field(
        ..., title="Time base", description="Time base for the ephemeris"
    )


class ProperMotion(BaseModel):
    """Proper motion."""

    right_ascension_speed: float = Field(
        ...,
        title="Right ascension speed",
        description="Right ascension speed, in arcseconds per year",
    )
    declination_speed: float = Field(
        ...,
        title="Declination speed",
        description="Declination speed, in arcseconds per year",
    )
    epoch: datetime = Field(
        ...,
        title="Epoch",
        description="Time for which the target coordinates are given",
    )


class TargetType(BaseModel):
    """A target type and subtype, based on the SIMBAD classification."""

    type: str = Field(
        ...,
        title="Target type",
        description="Target type.",
    )
    subtype: str = Field(
        ..., title="Target subtype", description="The target sub type."
    )


class Target(BaseModel):
    """Base model for targets."""

    id: int = Field(
        ..., title="Target id", description="Unique identifier of the target"
    )
    name: str = Field(..., title="Target name", description="Target name")
    coordinates: Optional[TargetCoordinates] = Field(
        ...,
        title="Target coordinates",
        description="Target coordinates for a sidereal target",
    )
    proper_motion: Optional[ProperMotion] = Field(
        ..., title="Proper motion", description="Proper motion"
    )
    magnitude: Optional[Magnitude] = Field(
        ..., title="Magnitude", description="Apparent magnitude (range) of the target"
    )
    target_type: Optional[TargetType] = Field(
        ...,
        title="Target",
        description="Target type, based on the SIMBAD classification",
    )
    period_ephemeris: Optional[PeriodEphemeris] = Field(
        ...,
        title="Period ephemeris",
        description="Ephemeris for the period of a variable target",
    )
    horizons_identifier: Optional[str] = Field(
        ...,
        title="Horizons identifier",
        description=(
            "Identifier for the target in the JPL-Horizons database of solar-system"
            " targets"
        ),
    )

    non_sidereal: bool = Field(
        ...,
        title="Is the target non-sidereal?",
        description="Is the target a non-sidereal target?",
    )
