from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from saltapi.web.schema.common import (
    ObservationProbabilities,
    Ranking,
    TargetCoordinates,
)


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
    type: str = Field(
        ...,
        title="Target type",
        description="The target type, based on the SIMBAD classification.",
    )
    sub_type: str = Field(
        ..., title="Target sub type", description="The target sub type."
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


class Phase1Target(Target):
    """A target in a Phase 1 proposal."""

    observing_time: int = Field(
        ...,
        title="The requested time",
        description=" The total time requested to observe this target.",
    )

    is_optional: bool = Field(
        ...,
        title="Optional?",
        description=(
            "Whether the target is optional, i.e. whether it is part of a pool of"
            " targets from which only a subset needs to be observed."
        ),
    )
    requested_observations: int = Field(
        ...,
        title="Number of requested observations",
        description="Number of observations requested for the target",
    )
    max_lunar_phase: float = Field(
        ...,
        title="Maximum lunar phase",
        description=(
            "Maximum lunar phase which was allowed for the observation, as the"
            " percentage of lunar illumination"
        ),
        ge=0,
        le=100,
    )
    ranking: Ranking = Field(
        ...,
        title="Ranking",
        description=(
            "Importance attributed by the Principal Investigator to observations of"
            " this target relative to other observations for the same proposal."
        ),
    )
    track_count: int = Field(
        ...,
        title="Number of tracks",
        description=(
            "The number of tracks in which the observation can be made, given the"
            " requested observation time and observation constraints."
        ),
    )
    night_count: int = Field(
        ...,
        title="Number of nights",
        description=(
            "The number of nights in which the observation can be made, given the"
            " requested observation time and observation constraints."
        ),
    )
    observing_probabilities: ObservationProbabilities = Field(
        ...,
        title="Observing probabilities",
        description="Probabilities related to observing the block",
    )
