from datetime import datetime
from enum import Enum
from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from saltapi.web.schema.bvit import Bvit
from saltapi.web.schema.common import TargetCoordinates, TimeInterval
from saltapi.web.schema.hrs import Hrs
from saltapi.web.schema.nir import Nir
from saltapi.web.schema.rss import Rss
from saltapi.web.schema.salticam import Salticam
from saltapi.web.schema.target import Target


class CalibrationFilter(str, Enum):
    """Calibration filter."""

    BLUE_AND_RED = "Blue and Red"
    CLEAR_AND_ND = "Clear and ND"
    CLEAR_AND_UV = "Clear and UV"
    ND_AND_CLEAR = "ND and Clear"
    NONE = "None"
    RED_AND_CLEAR = "Red and Clear"
    UV_AND_BLUE = "UV and Blue"


class DitherPattern(BaseModel):
    """Dither pattern."""

    horizontal_tiles: int = Field(
        ...,
        title="Horizontal tiles",
        description="Number of horizontal tiles in the pattern",
        ge=1,
    )
    vertical_tiles: int = Field(
        ...,
        title="Horizontal tiles",
        description="Number of horizontal tiles in the pattern",
        ge=1,
    )
    offset_size: float = Field(
        ...,
        title="Offset size",
        description="Offset size, i.e. size of a dither step, in arcseconds",
    )
    steps: int = Field(..., title="Number of steps", description="Number of steps")


class FinderChartFile(BaseModel):
    size: Literal["original", "thumbnail"] = Field(
        ..., title="Size", description="Geometrical size of this finder chart file"
    )
    url: str = Field(
        ...,
        title="URL",
        description="URL at which this finder chart file is available",
    )


class FinderChart(BaseModel):
    id: int = Field(
        ..., title="Finder chart", description="Unique identifier for the finder chart"
    )
    comment: Optional[str] = Field(
        ..., title="Comment by the Principal Investigator regarding the finder chart"
    )
    valid_from: Optional[datetime] = Field(
        ..., title="Time from when the finder chart may be used"
    )
    valid_until: Optional[datetime] = Field(
        ..., title="Time until when the finder chart may be used"
    )
    files: List[FinderChartFile] = Field(
        ..., title="Available files for this finder chart"
    )


class GuideMethod(str, Enum):
    """Guide method."""

    HRS_PROBE = "HRS Probe"
    MANUAL = "Manual"
    NONE = "None"
    QUACK = "QUACK"
    RSS_PROBE = "RSS Probe"
    SALTICAM = "SALTICAM"
    SALTICAM_PROBE = "SALTICAM Probe"
    SLITVIEWER = "Slitviewer"


class GuideStar(TargetCoordinates):
    """Guide star."""

    magnitude: float = Field(..., title="Magnitude", description="Magnitude")


class Instruments(BaseModel):
    """Instrument setups."""

    salticam: Optional[List[Salticam]] = Field(
        ..., title="Salticam setups", description="Salticam setups"
    )
    rss: Optional[List[Rss]] = Field(..., title="RSS setups", description="RSS setups")
    hrs: Optional[List[Hrs]] = Field(..., title="HRS setups", description="HRS setups")
    bvit: Optional[List[Bvit]] = Field(
        ..., title="BVIT setups", description="BVIT setups"
    )
    nir: Optional[List[Nir]] = Field(..., title="NIR setups", description="NIR setups")


class PayloadConfigurationType(str, Enum):
    """Payload configuration type."""

    ACQUISITION = "Acquisition"
    CALIBRATION = "Calibration"
    INSTRUMENT_ACQUISITION = "Instrument Acquisition"
    SCIENCE = "Science"


class PhaseInterval(BaseModel):
    """Phase interval."""

    start: float = Field(
        ..., title="Interval start", description="Start phase of the interval"
    )
    end: float = Field(
        ..., title="Interval end", description="End phase of the interval"
    )


class PayloadConfiguration(BaseModel):
    """Payload configuration."""

    payload_configuration_type: Optional[PayloadConfigurationType] = Field(
        ...,
        title="Payload configuration type",
        description="Payload configuration type",
    )
    use_calibration_screen: Optional[bool] = Field(
        ...,
        title="Calibration screen used?",
        description="Whether the calibration screen is used",
    )
    lamp: Optional[str] = Field(
        ..., title="Calibration lamp", description="Calibration lamp"
    )
    calibration_filter: Optional[CalibrationFilter] = Field(
        ..., title="Calibration filter", description="Calibration filter"
    )
    guide_method: GuideMethod = Field(
        ..., title="Guide method", description="Guide method"
    )
    instruments: Instruments = Field(
        ..., title="Instrument setups", description="Instrument setups"
    )


class TelescopeConfiguration(BaseModel):
    """Telescope configuration."""

    iterations: int = Field(
        ...,
        title="Iterations",
        description="Number of iterations. This should usually be 1",
    )
    position_angle: Optional[float] = Field(
        ...,
        title="Position angle",
        description="Position angle, measured from north to east, in degrees",
    )
    is_position_angle_fixed: bool = Field(
        ...,
        title="Is the position angle fixed?",
        description=(
            "Is the position angle fixed and must not be flipped by 180 degrees?"
        ),
    )
    use_parallactic_angle: bool = Field(
        ...,
        title="Use parallactic angle?",
        description="Whether to use a parallactic angle",
    )
    dither_pattern: Optional[DitherPattern] = Field(
        ..., title="Dither pattern", description="Dither pattern"
    )
    guide_star: Optional[GuideStar] = Field(
        ..., title="Guide star", description="Guide star"
    )
    payload_configurations: List[PayloadConfiguration] = Field(
        ..., title="Payload configurations", description="Payload configurations"
    )


class Observation(BaseModel):
    """Observation."""

    observation_time: int = Field(
        ...,
        title="Observation time",
        description=(
            "Time required for executing the observation, including the overhead time,"
            " in seconds"
        ),
        gt=0,
    )
    overhead_time: Optional[int] = Field(
        ..., title="Overhead time for the observation, in seconds", gt=0
    )
    target: Target = Field(..., title="Target", description="Target to be observed")
    finder_charts: List[FinderChart] = Field(
        ..., title="Finder charts", description="Finder charts"
    )
    time_restrictions: Optional[List[TimeInterval]] = Field(
        ...,
        title="Time restrictions",
        description=(
            "List of time intervals outside which the observation should not be made"
        ),
    )
    phase_constraints: Optional[List[PhaseInterval]] = Field(
        ...,
        title="Phase constraints",
        description=(
            "List of phase constraints. An observation should only be made when the"
            " phase of the (periodic) target is one of these intervals"
        ),
    )
    telescope_configurations: List[TelescopeConfiguration] = Field(
        ..., title="Telescope configurations", description="Telescope configurations"
    )
