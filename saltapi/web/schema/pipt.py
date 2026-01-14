from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, EmailStr, Field

from saltapi.web.schema.common import BlockVisitStatusValue, ProposalCode, Semester
from saltapi.web.schema.institution import UserInstitution, Institution
from saltapi.web.schema.proposal import ProposalStatus, TimeAllocation, ProposalUser


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


class PiptTimeAllocation(BaseModel):
    """Represents constraints of a specified proposal."""

    year: int = Field(..., title="Year", description="Year of the semester")
    semester: int = Field(..., title="Semester", description="Semester number")
    priority: int = Field(..., title="Priority", description="Proposal priority")
    moon: Optional[str] = Field(
        None, title="Moon Phase", description="Moon phase or name"
    )
    allocated_time: float = Field(
        ..., title="Allocated Time", description="Time allocated"
    )


class NirwalsFlatListItem(BaseModel):
    """Represents a single configuration item for the NIRWALS instrument list."""

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
    exposure_time: float = Field(
        ..., title="Exposure time", description="Exposure time in seconds"
    )
    n_groups: int = Field(..., title="Groups", description="Number of groups")
    n_ramps: int = Field(..., title="Ramps", description="Number of ramps")
    neutral_density: int = Field(
        ..., ge=0, title="Neutral density", description="Neutral density setting"
    )


class NirwalsFlatDetailsSetup(BaseModel):
    """List for NIRWALS flat field details."""

    entries: List[NirwalsFlatListItem]


class BaseArcListItem(BaseModel):
    """Represents basic arc configuration item for the NIRWALS instrument list."""

    grating: Optional[str] = Field(..., title="Grating", description=" The grating")
    art_station: int = Field(
        ..., title="Station number", description="Nirwals art station number"
    )


class NirwalsExposureListItem(BaseArcListItem):
    """Represents exposure item for the NIRWALS arc exposures."""

    grating_angle: float = Field(
        ..., title="Grating angle", description="Grating angle, in degrees"
    )
    lamp: Optional[str] = Field(
        ..., title="Calibration lamp", description="Calibration lamp"
    )
    exposure_time: float = Field(
        ..., title="Exposure time", description="Exposure time in seconds"
    )
    n_groups: int = Field(..., title="Groups", description="Number of groups")
    neutral_density: int = Field(
        ..., ge=0, title="Neutral density", description="Neutral density setting"
    )


class NirwalsAllowedLampSetup(BaseArcListItem):
    """Represents item for the NIRWALS arc allowed lamp setups."""

    grating_angle: float = Field(
        ..., title="Grating angle", description="Grating angle, in degrees"
    )
    lamp_setups: List[str] = Field(
        ..., title="Calibration lamps", description="Calibration lamps"
    )


class NirwalsPreferredLampSetup(BaseArcListItem):
    """Represents item for the NIRWALS arc preferred lamp setups."""

    lamp_setup: str = Field(
        ..., title="Calibration lamp", description="Calibration lamp"
    )


class NirwalsArcDetailsSetup(BaseModel):
    """List for NIRWALS arc details."""

    exposures: List[NirwalsExposureListItem]
    allowed_lamp_setups: List[NirwalsAllowedLampSetup]
    preferred_lamp_setups: List[NirwalsPreferredLampSetup]


class RssFPCalibrationRegion(BaseModel):
    mode: str = Field(..., title="FabryPerot mode", description="Instrument mode")
    w_min: float = Field(
        ...,
        title="Minimum wavelength",
        description="Minimum wavelength of calibration region (Å)",
    )
    w_max: float = Field(
        ...,
        title="Maximum wavelength",
        description="Maximum wavelength of calibration region (Å)",
    )
    filter: Optional[str] = Field(None, title="RSS filter", description="RSS filter")
    line_id: Optional[int] = Field(
        None, title="Line Id", description="RssFabryPerotCalibration line Id"
    )
    valid: bool = Field(..., title="Valid", description="Valid")


class RssFPCalibrationLine(BaseModel):
    line_id: Optional[int] = Field(
        None, title="Line Id", description="RssFabryPerotCalibration line Id"
    )
    lamp: str = Field(..., title="Calibration lamp", description="Calibration lamp")
    w_line: float = Field(..., title="Wavelength", description="Wavelength")
    w_obs: float = Field(..., title="Wavelength", description="Wavelength + 12")
    rel_intensity: float = Field(
        ..., title="Relative Intensity", description="Relative Intensity"
    )
    exposure_time: int = Field(..., title="Exposure time", description="Exposure time")


class RssRingDetailsSetup(BaseModel):
    fp_calibration_regions: List[RssFPCalibrationRegion] = Field(
        ..., description="Fabry-Perot calibration regions"
    )
    fp_calibration_lines: List[RssFPCalibrationLine] = Field(
        ..., description="Fabry-Perot calibration lines"
    )


class SmiFlatDetailsListItem(BaseModel):
    """Represents a single flat exposure configuration item for the SMI."""

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
    exposure_time: float = Field(
        ..., title="Exposure time", description="Exposure time in seconds"
    )
    neutral_density: int = Field(
        ..., ge=0, title="Neutral density", description="Neutral density setting"
    )


class SmiFlatDetailsSetup(BaseModel):
    """List for SMI flat details."""

    entries: List[SmiFlatDetailsListItem]


class SmiArcListItem(BaseModel):
    """Represents configuration item for SMI arc-related setups."""

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


class SmiAllowedLampSetup(SmiArcListItem):
    """Represents allowed lamp setup item for SMI arc configuration."""

    lamp_setups: List[str] = Field(
        ..., title="Calibration lamps", description="Calibration lamps"
    )


class SmiPreferredLampSetup(SmiArcListItem):
    """Represents the preferred lamp setup for SMI arc configuration."""

    lamp_setup: str = Field(
        ..., title="Calibration lamp", description="Calibration lamp"
    )


class SmiArcExposure(SmiArcListItem):
    """Represents exposure item for SMI arc exposures."""

    lamp: str = Field(..., title="Calibration lamps", description="Calibration lamps")
    exposure_time: float = Field(
        ...,
        title="Exposure time",
        description="Exposure time in seconds",
    )


class SmiArcDetailsSetup(BaseModel):
    """Response model for SMI arc details."""

    allowed_lamp_setups: List[SmiAllowedLampSetup]
    preferred_lamp_setups: List[SmiPreferredLampSetup]
    exposures: List[SmiArcExposure]


class RssArcExposureListItem(BaseArcListItem):
    """Represents exposure item for the RSS arc exposures."""

    lamp: Optional[str] = Field(
        ..., title="Calibration lamp", description="Calibration lamp"
    )
    exposure_time: float = Field(
        ..., title="Exposure time", description="Exposure time in seconds"
    )


class RssArcAllowedLampSetup(BaseArcListItem):
    """Represents item for the RSS arc allowed lamp setups."""

    lamps: List[str] = Field(
        ..., title="Calibration lamps", description="Calibration lamps"
    )


class RssArcPreferredLampSetup(BaseArcListItem):
    """Represents item for the RSS arc preferred lamp setups."""

    lamp: Optional[str] = Field(
        ..., title="Calibration lamp", description="Calibration lamp"
    )


class RssArcDetailsSetup(BaseModel):
    """Response model for RSS arc calibration details."""

    exposure_times: List[RssArcExposureListItem]
    allowed_lamps: List[RssArcAllowedLampSetup]
    preferred_lamps: List[RssArcPreferredLampSetup]


class PreviousProposalListItem(BaseModel):
    """Represents an item for previous proposals."""

    proposal_code: str = Field(..., title="Proposal code", description="Proposal code")
    title: str = Field(..., title="Title", description="Title of the proposal")
    allocated_time: int = Field(
        ..., title="Allocated Time", description="Time allocated"
    )
    observed_time: int = Field(..., title="Observed Time", description="Time observed")
    publications: List[str] = Field(
        ...,
        title="Publications",
        description="List of publications",
    )


class PiptBlockVisit(BaseModel):
    block_code: Optional[str] = Field(
        None,
        title="Block code",
        description="Identifier for the block",
    )
    block_name: Optional[str] = Field(
        None, title="Block name", description="Name for the block"
    )
    block_visit_status: Optional[str] = Field(
        None,
        title="Block visit status",
        description="Status of the block",
    )
    priority: int = Field(
        ...,
        title="Block priority",
        description="The priority of the block",
    )
    moon: Optional[str] = Field(None, title="Moon phase", description="Moon phase")
    total_time: Optional[float] = Field(
        None,
        title="Total observation time",
        description="Total observation time",
    )
    overhead_time: Optional[float] = Field(
        None, title="Overhead time", description="Overhead time"
    )
    pool_code: Optional[str] = Field(
        None,
        title="Pool code",
        description="Code of the associated pool, if any",
    )
    semester: Semester = Field(
        ...,
        title="Semester",
        description="Semester of the observation",
    )


class PiptProposal(BaseModel):
    """A PIPT proposal."""

    proposal_id: int = Field(
        ..., title="Proposal ID", description="Unique identifier for the proposal"
    )
    proposal_code: str = Field(..., title="Proposal code", description="Proposal code")
    title: str = Field(..., title="Title", description="Proposal title")
    semester: Semester = Field(
        ...,
        title="Semester",
        description="Semester for which the proposal details are given",
    )
    principal_investigator: str = Field(
        ..., title="Principal Investigator", description="Principal Investigator"
    )
    editable: bool = Field(
        ...,
        title="Editable",
        description="Indicates whether the current user can edit this proposal",
    )
    proposal_file: str = Field(
        ...,
        title="Proposal file",
        description=(
            "URL of the proposal file that can be imported into the Principal "
            "Investigator Proposal Tool"
        ),
    )


class PiptInstitute(BaseModel):
    """Institute details, as needed by the PIPT."""

    name: str = Field(..., title="Name", description="The name of the institute.")
    department: Optional[str] = Field(
        None, title="Department", description="The name of the department."
    )


class PiptPartner(BaseModel):
    """Partner details, as needed by the PIPT."""

    name: str = Field(
        ...,
        title="Name",
        description='The full name of the partner, such as "University of Wisconsin-Madison".',
    )
    institutes: List[PiptInstitute] = Field(
        ..., title="Institutes", description="The institutes belonging to the partner."
    )


class PiptInvestigator(ProposalUser):
    """Investigator details, as needed by the PIPT."""

    partner: str = Field(
        ..., description="Name of the partner to which the user's institute belongs."
    )
    institute: str = Field(..., description="Name of the user's institute.")
    department: Optional[str] = Field(None, description="Institute department.")
    phone: Optional[str] = Field(None, description="Phone number.")
