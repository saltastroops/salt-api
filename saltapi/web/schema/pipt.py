from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, EmailStr, Field

from saltapi.web.schema.common import ProposalCode
from saltapi.web.schema.institution import UserInstitution
from saltapi.web.schema.proposal import ProposalStatus, TimeAllocation


class PiptNewsItem(BaseModel):
    """A PIPT news item."""

    date: datetime = Field(
        ..., title="Date", description="Date and time of the news item"
    )
    title: str = Field(..., title="Title", description="Title of the news item")
    text: str = Field(..., title="Text", description="Content of the news item")


class PiptUserInfo(BaseModel):
    """Basic user details."""

    given_name: str = Field(..., title="First Name")
    family_name: str = Field(..., title="Last Name")
    email: EmailStr = Field(..., title="Email address", description="Email address")
    affiliation: UserInstitution = Field(
        ..., title="Affiliation", description="Affiliation of the user"
    )


class PiptProposalInfo(BaseModel):
    """Details about a proposal."""

    proposal_code: ProposalCode = Field(
        ..., title="Proposal code", description="Proposal code"
    )
    title: str = Field(..., title="Title", description="Proposal title")
    phase: Literal[1, 2] = Field(
        ...,
        title="Proposal phase",
        description="Proposal phase",
    )
    status: ProposalStatus = Field(
        ..., title="Proposal status", description="Proposal status"
    )
    proposal_file: str = Field(
        ...,
        title="Proposal file",
        description=(
            "URL of the proposal file that can be imported into the Principal "
            "Investigator Proposal Tool"
        ),
    )
    time_allocations: List[TimeAllocation] = Field(
        ...,
        title="Time allocations",
        description="Time allocations for the semester",
    )


class ProposalConstraint(BaseModel):
    """Represents constraints of a specified proposal."""

    year: int = Field(..., title="Year", description="Year of the semester")
    semester: int = Field(..., title="Semester", description="Semester number")
    priority: int = Field(..., title="Priority", description="Proposal priority")
    moon: Optional[str] = Field(
        None, title="Moon Phase", description="Moon phase or name (optional)"
    )
    allocated_time: float = Field(
        ..., title="Allocated Time", description="Time allocated"
    )


class NirwalsFlatEntry(BaseModel):
    """Represents a single entry configuration for the NIRWALS instrument."""

    grating: Optional[str] = Field(..., title="Grating", description=" The grating")
    grating_angle: float = Field(
        ..., title="Grating angle", description="Grating angle, in degrees"
    )
    art_station: int = Field(
        ..., title="Station number", description="Nirwals art station number"
    )
    lamp: Optional[str] = Field(
        ..., title="Calibration lamp", description="Calibration lamp"
    )
    exptime: float = Field(
        ..., title="Exposure time", description="Exposure time in seconds"
    )
    n_groups: int = Field(..., title="Groups", description="Number of groups")
    n_ramps: int = Field(..., title="Ramps", description="Number of ramps")
    neutral_density: int = Field(
        ..., ge=0, title="Neutral density", description="Neutral density setting"
    )


class NirwalsFlatDetailsResponse(BaseModel):
    """Response model for NIRWALS flat details."""

    entries: List[NirwalsFlatEntry]


class NirwalsArcEntry(BaseModel):
    """Represents basic arc exposure configuration details for NIRWALS."""

    grating: Optional[str] = Field(..., title="Grating", description=" The grating")
    art_station: int = Field(
        ..., title="Station number", description="Nirwals art station number"
    )


class ExposureEntry(NirwalsArcEntry):
    """Represents single exposure entry for the NIRWALS arc exposures."""

    grating_angle: float = Field(
        ..., title="Grating angle", description="Grating angle, in degrees"
    )
    lamp: Optional[str] = Field(
        ..., title="Calibration lamp", description="Calibration lamp"
    )
    exptime: float = Field(
        ..., title="Exposure time", description="Exposure time in seconds"
    )
    n_groups: int = Field(..., title="Groups", description="Number of groups")
    neutral_density: int = Field(
        ..., ge=0, title="Neutral density", description="Neutral density setting"
    )


class AllowedLampSetupEntry(NirwalsArcEntry):
    """Represents single exposure entry for the NIRWALS arc allowed lamp setups."""

    grating_angle: float = Field(
        ..., title="Grating angle", description="Grating angle, in degrees"
    )
    lamp_setups: List[str] = Field(
        ..., title="Calibration lamps", description="Calibration lamps"
    )


class PreferredLampSetupEntry(BaseModel):
    """Represents single exposure entry for the NIRWALS arc preferred lamp setups."""

    lamp_setup: str = Field(
        ..., title="Calibration lamp", description="Calibration lamp"
    )


class NirwalsArcDetailsResponse(BaseModel):
    """Response model for NIRWALS arc details."""

    exposures: List[ExposureEntry]
    allowed_lamp_setups: List[AllowedLampSetupEntry]
    preferred_lamp_setups: List[PreferredLampSetupEntry]


class SmiFlatDetails(BaseModel):
    """Represents a single flat exposure configuration for the SMI."""

    smi_barcode: str = Field(..., description="RssMask barcode")
    grating: Optional[str] = Field(..., title="Grating", description=" The grating")
    grating_angle: float = Field(
        ..., title="Grating angle", description="Grating angle, in degrees"
    )
    art_station: int = Field(
        ..., title="Station number", description="RSS art station number"
    )
    pre_bin_rows: int = Field(
        ..., ge=1, title="Bining", description="Rows bining value"
    )
    pre_bin_cols: int = Field(
        ..., ge=1, title="Bining", description="Columns bining value"
    )
    lamp: Optional[str] = Field(
        ..., title="Calibration lamp", description="Calibration lamp"
    )
    exptime: float = Field(
        ..., title="Exposure time", description="Exposure time in seconds"
    )
    neutral_density: int = Field(
        ..., ge=0, title="Neutral density", description="Neutral density setting"
    )


class SmiFlatDetailsResponse(BaseModel):
    """Response model for SMI flat details."""

    entries: List[SmiFlatDetails]


class ArcBaseSetup(BaseModel):
    """Base configuration shared by all SMI arc-related setups."""

    smi_barcode: str = Field(..., description="RssMask barcode")
    grating: Optional[str] = Field(..., title="Grating", description=" The grating")
    grating_angle: float = Field(
        ..., title="Grating angle", description="Grating angle, in degrees"
    )
    art_station: int = Field(
        ..., title="Station number", description="RSS art station number"
    )
    pre_bin_rows: int = Field(
        ..., ge=1, title="Bining", description="Rows bining value"
    )
    pre_bin_cols: int = Field(
        ..., ge=1, title="Bining", description="Columns bining value"
    )


class AllowedLampSetup(ArcBaseSetup):
    """Represents allowed lamp setups for a given SMI arc configuration."""

    lamp_setups: List[str] = Field(
        ..., title="Calibration lamps", description="Calibration lamps"
    )


class PreferredLampSetup(ArcBaseSetup):
    """Represents the preferred lamp setup for a specific SMI arc configuration."""

    lamp_setup: str = Field(
        ..., title="Calibration lamp", description="Calibration lamp"
    )


class ArcExposure(ArcBaseSetup):
    """Represents an arc exposure configuration with lamp and exposure time for SMI."""

    lamp: str = Field(..., title="Calibration lamps", description="Calibration lamps")
    exptime: float = Field(
        ..., title="Exposure time", description="Exposure time in seconds"
    )


class SmiArcDetailsResponse(BaseModel):
    """Response model for SMI arc details."""

    allowed_lamp_setups: List[AllowedLampSetup]
    preferred_lamp_setups: List[PreferredLampSetup]
    exposures: List[ArcExposure]


class RssArcExposureEntry(NirwalsArcEntry):
    """Represents an RSS arc exposure entry information."""

    lamp: Optional[str] = Field(
        ..., title="Calibration lamp", description="Calibration lamp"
    )
    exptime: float = Field(
        ..., title="Exposure time", description="Exposure time in seconds"
    )


class RssArcDetailsResponse(BaseModel):
    """Response model for RSS arc exposure details."""

    exposure_times: List[RssArcExposureEntry]
