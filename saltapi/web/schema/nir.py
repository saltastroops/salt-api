from enum import Enum
from typing import List, Optional, Literal

from pydantic import BaseModel, Field


class NirSamplingMode(str, Enum):
    FOCUS = "Focus"
    NORMAL = "Normal"


class NirGrating(str, Enum):
    """NIR grating."""

    PNG0950 = "ng0950"


class NirCameraFilterWheel(str, Enum):
    """NIR camera filter wheel."""

    BLOCK = "Block"
    CLEAR = "Clear"
    CUTOFF = "Cutoff"
    DIFFUSER = "Diffuser"
    EMPTY = "Empty"


class NirConfiguration(BaseModel):
    """NIR configuration."""

    grating: str = Field(..., title="Grating", description="Grating")
    grating_angle: float = Field(
        ..., title="Grating angle", description="Grating angle, in degrees"
    )
    camera_station: str = Field(
        ..., title="Camera station", description="Camera (articulation) station number"
    )
    camera_angle: float = Field(
        ..., title="Camera angle", description="Camera (articulation) angle, in degrees"
    )
    filter: str = Field(..., title="NIR filter", description="NIR filter")
    camera_filter_wheel: NirCameraFilterWheel = Field(
        ..., title="Camera filter wheel", description="Camera filter wheel"
    )


class NirGain(str, Enum):
    """NIR gain."""

    BRIGHT = "Bright"
    FAINT = "Faint"


class NirDetector(BaseModel):
    """NIR detector setup."""

    mode: str = Field(..., title="Instrument mode", description="Instrument mode")
    groups: int = Field(
        ...,
        title="Up-the-ramp groups",
        description="The number of samples up the ramp for the Up-the-Ramp Group mode",
    )
    ramps: float = Field(
        ..., title="Ramps", description="How many exposure sequences to do?"
    )
    reads_per_sample: int = Field(
        ...,
        title="Reads per sample",
        description="Number of reads done for each sample",
    )
    exposure_time: float = Field(
        ...,
        title="Exposure time",
        description="Exposure time per exposure, in seconds",
        ge=0,
    )
    iterations: int = Field(
        ..., title="Number of exposures", description="Number of exposures", ge=1
    )
    gain: NirGain = Field(..., title="Gain", description="Gain")


class NirProcedureType(str, Enum):
    """NIR procedure type."""

    FOWLER = "Focus"
    UP_THE_RAMP_GROUP = "Up-the-Ramp Group"


class NirOffsetType(str, Enum):
    """NIR offset type."""

    FIF_OFFSET = "FIF Offset"
    BUNDLE_SEPARATION_OFFSET = "Bundle Separation Offset"
    TRACKER_GUIDER_OFFSET = "Tracker Guided Offset"
    UNGUIDED_OFFSET = "Unguided Offset"


class NirDitherOffset(BaseModel):
    """NIR offset coordinates."""

    x: float = Field(
        ...,
        title="Horizontal offset",
        description="Horizontal offset (in image coordinates), in arcseconds",
    )
    y: float = Field(
        ...,
        title="Vertical offset",
        description="Vertical offset (in image coordinates), in arcseconds",
    )


class NirDitherStep(BaseModel):
    """NIR dither step."""

    offset: NirDitherOffset = Field(
        ..., title="Dither offset", description="Dither offset"
    )
    offset_type: NirOffsetType = Field(
        ..., title="Dither offset type", description="Dither offset type"
    )
    detector: NirDetector = Field(
        ..., title="Detector setup", description="Detector setup"
    )
    exposure_type: str = Field(..., title="Exposure type", description="Exposure type")


class NirProcedure(BaseModel):
    """NIR procedure."""

    cycles: int = Field(
        ...,
        title="Cycles",
        description="Number of cycles, i.e. how often to execute the procedure",
    )
    procedure_type: str = Field(
        ..., title="Procedure type", description="Procedure type"
    )
    dither_pattern: List[NirDitherStep] = Field(
        ..., title="Dither step", description="Dither step"
    )


class Nir(BaseModel):
    """NIR setup."""

    id: int = Field(
        ..., title="NIR id", description="Unique identifier for the NIR setup"
    )
    configuration: NirConfiguration = Field(
        ..., title="Instrument configuration", description="Instrument configuration"
    )
    procedure: Optional[NirProcedure] = Field(
        ..., title="Detector setup", description="Detector setup"
    )
    observation_time: float = Field(
        ...,
        title="Observation time",
        description="Total time required for the setup, in seconds",
        ge=0,
    )
    overhead_time: float = Field(
        ...,
        title="Overhead time",
        description="Overhead time for the setup, in seconds",
        ge=0,
    )


class NirSummary(BaseModel):
    """Summary information for NIR."""

    name: Literal["NIR"] = Field(
        ..., title="Instrument name", description="Instrument name"
    )
    gratings: Optional[List[NirGrating]] = Field(
        ..., title="Grating", description="Grating"
    )
    filters: Optional[List[str]] = Field(..., title="Filters", description="Filters")