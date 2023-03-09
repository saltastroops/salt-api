from datetime import date, datetime
from enum import Enum
from typing import List, Literal, Optional

from pydantic import BaseModel, EmailStr, Field, validator

from saltapi.util import as_form, parse_partner_requested_percentages
from saltapi.web.schema.common import (
    PartnerCode,
    PartnerName,
    Priority,
    ProposalCode,
    Semester,
)
from saltapi.web.schema.institution import Institution
from saltapi.web.schema.user import FullName, UserListItem


class ProposalUser(FullName):
    id: int = Field(..., title="User id", description="User id.")
    email: EmailStr = Field(..., title="Email address", description="Email address")


ProposalApprovalStatus = Literal["Accepted", "Rejected"]


class ProposalStatusValue(str, Enum):
    """Proposal status value."""

    ACCEPTED = "Accepted"
    ACTIVE = "Active"
    COMPLETED = "Completed"
    DELETED = "Deleted"
    EXPIRED = "Expired"
    IN_PREPARATION = "In preparation"
    INACTIVE = "Inactive"
    REJECTED = "Rejected"
    SUPERSEDED = "Superseded"
    UNDER_SCIENTIFIC_REVIEW = "Under scientific review"
    UNDER_TECHNICAL_REVIEW = "Under technical review"


class ProposalInactiveReason(str, Enum):
    """Proposal inactive reason."""

    TARGET_NOT_VISIBLE = "Target not visible"
    UNDOABLE = "Undoable"
    WAITING_FOR_FEEDBACK = "Waiting for feedback"
    WAITING_FOR_INSTRUMENT_AVAILABILITY = "Waiting for instrument availability"
    ToO_AWAITING_PI_INITIATION = "ToO, awaiting PI initiation"
    OTHER = "Other"


class ProposalStatus(BaseModel):
    """Proposal status."""

    value: ProposalStatusValue = Field(
        ..., title="Proposal status", description="Proposal status"
    )
    comment: Optional[str] = Field(
        ..., title="Proposal status comment", description="Proposal status comment"
    )


class ProposalType(str, Enum):
    """Proposal type."""

    COMMISSIONING = "Commissioning"
    DIRECTOR_DISCRETIONARY_TIME = "Director's Discretionary Time"
    ENGINEERING = "Engineering"
    GRAVITATIONAL_WAVE_EVENT = "Gravitational Wave Event"
    KEY_SCIENCE_PROGRAM = "Key Science Program"
    LARGE_SCIENCE_PROPOSAL = "Large Science Proposal"
    OPTICON_RADIO_PILOT = "OPTICON-Radionet Pilot"
    SCIENCE = "Science"
    SCIENCE_LONG_TERM = "Science - Long Term"
    SCIENCE_VERIFICATION = "Science Verification"


class UpdateStatus(str, Enum):
    SUCCESSFUL = "Successful"
    PENDING = "Pending"
    FAILED = "Failed"


class ProprietaryPeriod(BaseModel):
    """Proprietary period."""

    period: Optional[int] = Field(
        ...,
        title="Current proprietary period",
        description="Proprietary period in months.",
    )
    maximum_period: Optional[int] = Field(
        ...,
        title="Maximum proprietary period, in months",
        description=(
            "Maximum proprietary period, in months for partner partners that have it."
        ),
    )
    start_date: Optional[date] = Field(
        ...,
        title="Start date",
        description="Start date from which the proprietary period is counted.",
    )


class GeneralProposalInfo(BaseModel):
    """General proposal information for a semester."""

    title: str = Field(..., title="Title", description="Proposal title")
    abstract: str = Field(..., title="Abstract", description="Proposal abstract")
    current_submission: datetime = Field(
        ...,
        title="Current submission datetime",
        description="Datetime of the latest submission for any semester",
    )
    first_submission: datetime = Field(
        ...,
        title="First submission datetime",
        description="Datetime of the first submission for any semester",
    )
    semesters: List[Semester] = Field(
        ...,
        title="Semesters",
        description="List of semesters for which the proposal has been submitted",
    )
    submission_number: int = Field(
        ...,
        title="Submission number",
        description="Current submission number for any semester",
    )
    status: ProposalStatus = Field(
        ..., title="Proposal status", description="Proposal status"
    )
    proposal_type: ProposalType = Field(
        ..., title="Proposal type", description="Proposal type"
    )
    is_target_of_opportunity: bool = Field(
        ...,
        title="Target of opportunity?",
        description="Whether the proposal contains targets of opportunity",
    )
    total_requested_time: int = Field(
        ...,
        title="Total requested time",
        description="Total requested time, in seconds",
    )

    liaison_salt_astronomer: Optional[UserListItem] = Field(
        ...,
        title="Liaison astronomer",
        description="SALT Astronomer who is the liaison astronomer for the proposal",
    )

    is_self_activatable: bool = Field(
        ...,
        title="Can the proposal be self-activated?",
        description=(
            "Can the proposal be activated by the Principal Investigator or Principal"
            " Contact?"
        ),
    )


class ThesisType(str, Enum):
    MASTERS = ("Masters",)
    PHD = "PhD"


class Thesis(BaseModel):
    thesis_type: ThesisType = Field(
        ..., title="Thesis type", description="The thesis type"
    )
    relevance_of_proposal: Optional[str] = Field(
        ...,
        title="Relevance of proposal",
        description="Importance and contribution of the proposal to the thesis.",
    )
    year_of_completion: int = Field(
        ...,
        title="Year of completion",
        description="The year when the thesis is expected to be completed.",
    )


class Investigator(ProposalUser):
    """An investigator on a proposal."""

    affiliation: Institution = Field(
        ..., title="Affiliation", description="Affiliation of the investigator"
    )
    is_pc: bool = Field(
        ...,
        title="Principle Contact",
        description="Is this investigator the Principal Contact?",
    )
    is_pi: bool = Field(
        ...,
        title="Principle Investigator",
        description="Is this investigator the Principal Investigator?",
    )
    has_approved_proposal: Optional[bool] = Field(
        ...,
        title="Has approved proposal?",
        description=(
            "Whether the investigator has approved the proposal. The value is null if"
            " the investigator has neither approved nor rejected the proposal yet"
        ),
    )
    thesis: Optional[Thesis] = Field(
        ..., title="Thesis", description="The thesis details"
    )


class ChargedTime(BaseModel):
    """Charged time, broken down by priority."""

    priority_0: int = Field(
        ..., title="P0 time", description="Charged priority 0 time, in seconds", ge=0
    )
    priority_1: int = Field(
        ..., title="P1 time", description="Charged priority 1 time, in seconds", ge=0
    )
    priority_2: int = Field(
        ..., title="P2 time", description="Charged priority 2 time, in seconds", ge=0
    )
    priority_3: int = Field(
        ..., title="P3 time", description="Charged priority 3 time, in seconds", ge=0
    )
    priority_4: int = Field(
        ..., title="P4 time", description="Charged priority 4 time, in seconds", ge=0
    )


class DataReleaseDate(BaseModel):
    """The release date when the observation data is scheduled to become public."""

    release_date: date = Field(
        ...,
        title="Data release date",
        description="Date when the proposal data is scheduled to become public",
    )


class ProprietaryPeriodUpdateRequest(BaseModel):
    """A request to update the proprietary period."""

    proprietary_period: int = Field(
        ...,
        ge=0,
        title="The proprietary period",
        description=(
            "The proprietary period, in months. The proprietary period starts at the"
            " end of the semester when the last observation was taken."
        ),
    )
    motivation: Optional[str] = Field(
        ...,
        title="Motivation",
        description="Motivation why the request should be granted",
    )


class ObservationComment(BaseModel):
    """Comment related to an observation of a proposal."""

    id: int
    author: str = Field(..., title="Author", description="Author of the comment")
    comment: str = Field(..., title="Comment", description="Text of the comment")
    comment_date: date = Field(
        ...,
        title="Time of creation",
        description="Date when the comment was made",
    )

    class Config:
        schema_extra = {
            "example": {
                "id": 123,
                "author": "Sipho Mangana",
                "comment": "Please check the position angle.",
                "comment_date": "2019-08-24",
            }
        }


class Comment(BaseModel):
    """Comment."""

    comment: str = Field(..., title="Comment", description="Text of the comment")

    class Config:
        schema_extra = {
            "example": {
                "comment": "Please check the finding chart",
            }
        }


class PartnerPercentage(BaseModel):
    """A percentage (for example of the requested time) for a partner."""

    partner: PartnerName = Field(..., title="SALT partner", description="SALT partner")
    percentage: float = Field(
        ...,
        ge=0,
        le=100,
        title="Percentage",
        description="Percentage between 0 and 100 (both inclusive)",
    )


class RequestedTime(BaseModel):
    """Time requested in a phase 1 proposal."""

    total_requested_time: int = Field(
        ...,
        title="Total requested time",
        description="Total requested time, in seconds",
    )
    minimum_useful_time: Optional[int] = Field(
        ...,
        title="Minimum useful time",
        description=(
            "Minimum time needed to produce meaningful science from the proposal, in"
            " seconds."
        ),
    )
    comment: Optional[str] = Field(
        None, title="Comment", description="Comment on the time requirements"
    )
    semester: Semester = Field(
        ..., title="Semester", description="Semester for which the time is requested"
    )
    distribution: List[PartnerPercentage] = Field(
        ...,
        title="Distribution among partners",
        description="Percentages of time requested from the different partners",
    )


class TimeAllocation(BaseModel):
    """A time allocation."""

    partner_name: PartnerName = Field(
        ...,
        title="SALT partner name",
        description=(
            "Name of the SALT partner whose Time Allocation Committee is allocating the"
            " time"
        ),
    )
    partner_code: PartnerCode = Field(
        ...,
        title="SALT partner code",
        description=(
            "Code of the SALT partner whose Time Allocation Committee is allocating the"
            " time"
        ),
    )
    tac_comment: Optional[str] = Field(
        ...,
        title="TAC comment",
        description="Comment by the Time Allocation Committee allocating the time",
    )
    priority_0: int = Field(
        ..., title="P0 time", description="Allocated priority 0 time, in seconds", ge=0
    )
    priority_1: Priority = Field(
        ..., title="P1 time", description="Allocated priority 1 time, in seconds", ge=0
    )
    priority_2: Priority = Field(
        ..., title="P2 time", description="Allocated priority 2 time, in seconds", ge=0
    )
    priority_3: Priority = Field(
        ..., title="P3 time", description="Allocated priority 3 time, in seconds", ge=0
    )
    priority_4: Priority = Field(
        ..., title="P4 time", description="Allocated priority 4 time, in seconds", ge=0
    )


class Proposal(BaseModel):
    """A proposal."""

    proposal_code: ProposalCode = Field(
        ..., title="Proposal code", description="Proposal code"
    )
    phase: Literal[1, 2] = Field(
        ...,
        title="Proposal phase",
        description="Proposal phase",
    )
    semester: Semester = Field(
        ...,
        title="Semester",
        description="Semester for which the proposal details are given",
    )
    investigators: List[Investigator] = Field(
        ..., title="Investigators", description="Investigators on the proposal"
    )
    requested_times: List[RequestedTime] = Field(
        ...,
        title="Requested times",
        description="Requested times for all semesters in the proposal.",
    )
    time_allocations: List[TimeAllocation] = Field(
        ...,
        title="Time allocations",
        description="Time allocations for the semester",
    )
    phase1_proposal_summary: Optional[str] = Field(
        ...,
        title="Proposal summary",
        description="URL of a pdf document containing the phase 1 proposal summary",
    )
    proposal_file: str = Field(
        ...,
        title="Proposal file",
        description=(
            "URL of the proposal file that can be imported into the Principal "
            "Investigator Proposal Tool"
        ),
    )


class PartnerRequestedPercentage(BaseModel):
    """
    Requested Percentage for a partner
    """

    partner_code: PartnerCode = Field(
        ..., title="Partner code", description="Partner code, such as IUCAA."
    )

    partner_name: PartnerName = Field(
        ..., title="Partner name ", description="Name of the partner."
    )

    requested_percentage: float = Field(
        ..., title="Percentage", description="Percentage requested from a partner."
    )


class ProposalContentType(str, Enum):
    """Content type for a proposal."""

    JSON = ("application/json",)
    PDF = ("application/pdf",)
    ZIP = "application/zip"


class ProposalListItem(BaseModel):
    """Item in a list of proposals."""

    id: int = Field(
        ..., title="Proposal id", description="Unique identifier of the proposal"
    )
    proposal_code: str = Field(..., title="Proposal code", description="Proposal code")
    semester: Semester = Field(
        ...,
        title="Semester",
        description="Semester for which the proposal was submitted",
    )
    title: str = Field(..., title="Title", description="Proposal title")
    phase: int = Field(
        ..., gt=0, lt=3, title="Proposal phase", description="Proposal phase"
    )
    status: ProposalStatus = Field(
        ..., title="Proposal status", description="Proposal status"
    )
    proposal_type: ProposalType = Field(
        ..., title="Proposal type", description="Proposal type"
    )
    principal_investigator: ProposalUser = Field(
        ..., title="Principal Investigator", description="Principal Investigator"
    )
    principal_contact: ProposalUser = Field(
        ..., title="Principal Contact", description="Principal Contact"
    )
    liaison_astronomer: Optional[FullName] = Field(
        ..., title="Liaison Astronomer", description="Liaison Astronomer"
    )


class ProposalStatusContent(BaseModel):
    """Content including a proposal status."""

    status: ProposalStatus = Field(
        ..., title="Proposal status", description="Proposal status"
    )


class SubmissionAcknowledgment(BaseModel):
    """Acknowledgment that a proposal submission has been received."""

    submission_id: int = Field(
        ...,
        title="Submission id",
        description="Unique identifier for a proposal submission",
    )

    class Config:
        schema_extra = {"example": {"submission_id": 41318}}


class ObservingConstraints(BaseModel):
    seeing: float = Field(..., title="Seeing", description="The seeing")
    transparency: str = Field(..., title="Transparency", description="The transparency")
    description: str = Field(
        ...,
        title="Description",
        description="The brief description of observing constraints",
    )


class TimeStatistics(BaseModel):
    """Time statistics for a proposal."""

    semester: str = Field(..., title="Semester", description="The semester")
    requested_time: int = Field(
        ..., title="Requested time", description="Requested time for the semester."
    )
    allocated_time: int = Field(
        ..., title="Allocated time", description="Allocated time for the semester"
    )
    observed_time: int = Field(
        ..., title="Observed time", description="Observed time for the semester"
    )

    class Config:
        schema_extra = {
            "example": {
                "semester": "2022-1",
                "requested_time": 19000,
                "allocated_time": 18000,
                "observed_time": 17000,
            }
        }


class BaseProgressReport(BaseModel):
    requested_time: Optional[int] = Field(
        ...,
        title="Requested time",
        description="Requested time per partner.",
    )

    maximum_seeing: Optional[float] = Field(
        ...,
        title="Seeing",
        description="The maximum seeing.",
    )
    transparency: Optional[str] = Field(
        ...,
        title="Transparency",
        description="The transparency.",
    )
    description_of_observing_constraints: Optional[str] = Field(
        ...,
        title="Description of observing constraints",
        description="The description of observing constraints.",
    )
    change_reason: Optional[str] = Field(
        ...,
        title="Time request change reasons",
        description="The reason why the time request has changed.",
    )
    summary_of_proposal_status: Optional[str] = Field(
        ...,
        title="Summary of proposal status",
        description="The summary of proposal status.",
    )
    strategy_changes: Optional[str] = Field(
        ...,
        title="Strategy changes",
        description="The strategy changes.",
    )


class ProposalProgress(BaseProgressReport):
    """
    Progress report for a proposal and semester. The semester is the semester for which
    the progress is reported. For example, if the semester is 2021-1, the report covers
    the observations up to and including the 2021-1 semester and it requests time for
    the 2021-2 semester.
    """

    semester: Optional[str] = Field(
        ...,
        title="Semester",
        description="The semester for this progress report.",
    )
    partner_requested_percentages: List[PartnerRequestedPercentage] = Field(
        ...,
        title="Partner",
        description="The partner from which time is requested.",
    )
    previous_time_requests: List[TimeStatistics] = Field(
        ...,
        title="Previous time requests",
        description="The request from previous semesters",
    )
    last_observing_constraints: Optional[ObservingConstraints] = Field(
        ...,
        title="Last requested observing conditions",
        description="The last observing conditions.",
    )

    proposal_progress_pdf: Optional[str] = Field(
        ...,
        title="Proposal progress report pdf",
        description="Proposal progress report pdf",
    )
    additional_pdf: Optional[str] = Field(
        ...,
        title="Proposal progress report pdf",
        description="Proposal progress report pdf",
    )


@as_form
class ProposalProgressInput(BaseProgressReport):
    partner_requested_percentages: str = Field(
        ...,
        title="Partner requested percentages",
        description=(
            "The list of requested percentages per partner, as pairs of "
            "partner and requested percentages. E.g 'RSA:50;POL:50;OTH:0'."
        ),
    )

    @validator("partner_requested_percentages")
    def partner_requested_percentages_valid(cls, v: str) -> str:
        # If the value is invalid, parsing it will raise an error.
        parse_partner_requested_percentages(v)
        return v
