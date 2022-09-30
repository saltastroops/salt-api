from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class NirSamplingMode(str, Enum):
    FOCUS = "Focus"
    NORMAL = "Normal"


class NirSpectroscopy(BaseModel):
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


class NirConfiguration(BaseModel):
    mode: str = Field(..., title="Instrument mode", description="Instrument mode")
    spectroscopy: Optional[NirSpectroscopy] = Field(
        ..., title="NIR spectroscopy", description="NIR spectroscopy"
    )
    filter: str = Field(..., title="NIR filter", description="NIR filter")


class NirGain(str, Enum):
    """RSS gain."""

    BRIGHT = "Bright"
    FAINT = "Faint"


class NirDetector(BaseModel):
    mode: str = Field(..., title="Instrument mode", description="Instrument mode")
    resets: int
    ramps: float
    reads_per_sample: int
    exposure_time: float = Field(
        ...,
        title="Exposure time",
        description="Exposure time per exposure, in seconds",
        ge=0,
    )
    iterations: int = Field(
        ..., title="Number of exposures", description="Number of exposures", ge=1
    )
    exposure_type: str = Field(..., title="Exposure type", description="Exposure type")
    gain: NirGain = Field(..., title="Gain", description="Gain")


class NirProcedureType(str, Enum):
    FOWLER = "Focus"
    UP_THE_RAMP_GROUP = "Up-the-Ramp Group"


class NirProcedure(BaseModel):
    cycles: int = Field(
        ...,
        title="Cycles",
        description="Number of cycles, i.e. how often to execute the procedure",
    )
    procedure_type: str = Field(
        ..., title="Procedure type", description="Procedure type"
    )


class Nir(BaseModel):
    id: int = Field(
        ..., title="NIR id", description="Unique identifier for the NIR setup"
    )
    configuration: NirConfiguration = Field(
        ..., title="Instrument configuration", description="Instrument configuration"
    )
    detector: NirDetector = Field(
        ..., title="Detector setup", description="Detector setup"
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
