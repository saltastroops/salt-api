import re
from datetime import date, datetime
from enum import Enum, IntEnum
from typing import Any, Callable, Dict, Generator, List, Optional, Union

from pydantic import BaseModel, Field

from app.models.general import Semester


class TextContent(BaseModel):
    """
    The text content of a proposal.

    Fields
    ------
    semester:
        Semester to which the text content belongs.
    title:
        Proposal title.
    abstract:
        Proposal abstract.
    read_me:
        Instructions for the observer.
    nightlog_summary:
        Brief (one-line) summary to include in the nightlog.
    """

    semester: Semester
    title: str
    abstract: str
    read_me: str
    nightlog_summary: str


class Partner(BaseModel):
    """
    A SALT partner.

    Fields
    ------
    code:
        Partner code, such as IUCAA or RSA.
    name:
        Partner name.
    """

    code: str
    name: str


class Institute(BaseModel):
    """
    An institute, optionally with a department.

    Fields
    ------
    partner:
        SALT Partner to which the institute belongs.
    name:
        Institute name.
    department:
        Department within the institute.
    home_page:
        URL of the institute's (or department's) home page.
    """

    partner: Partner
    name: str
    department: Optional[str]
    home_page: str


class PersonalDetails(BaseModel):
    """
    Personal details.

    Fields
    ------
    given_name:
        The given ("first") name(s).
    family_name:
        The family ("last") name.
    email:
        The preferred email address.
    """

    given_name: str
    family_name: str
    email: str


class Investigator(BaseModel):
    """
    An investigator on a proposal.

    Fields
    ------
    is_pc:
        Whether the investigator is the Principal Contact.
    is_pi:
        Whether the investigator is the Principal Investigator.
    personal_details:
        Personal details of the investigator, which may differ from the ones given in
        the proposal.
    affiliation:
        Affiliation of the investigator (for the proposal).
    """

    is_pc: bool
    is_pi: bool
    personal_details: PersonalDetails
    affiliation: Institute


class TimeAllocation(BaseModel):
    """
    A time allocation by a partner.

    Fields
    ------
    partner:
        SALT partner that allocated the time.
    semester:
        Semester to which the time allocation belongs.
    tac_comment:
        An (optional) comment made by the TAC on the proposal for which this time
        allocation was made.
    priority_0:
        Allocated priority 0 time.
    priority_1:
        Allocated priority 1 time.
    priority_2:
        Allocated priority 2 time.
    priority_3:
        Allocated priority 3 time.
    priority_4:
        Allocated priority 4 time.
    """

    semester: Semester
    partner: Partner
    tac_comment: Optional[str]
    priority_0: int
    priority_1: int
    priority_2: int
    priority_3: int
    priority_4: int


class ObservedTime(BaseModel):
    """
    Time spent on observing (a proposal) in a semester

    Fields
    ------
    semester:
        Semester for which the time was spent. This is semester whose time allocation
        was used. The actual observations may have been made in the previous semester,
        if there was a gap in the observing queue.
    priority_0:
        Priority 0 time used for observing, in seconds.
    priority_1:
        Priority 1 time used for observing, in seconds.
    priority_2:
        Priority 2 time used for observing, in seconds.
    priority_3:
        Priority 3 time used for observing, in seconds.
    priority_4:
        Priority 4 time used for observing, in seconds.
    """

    semester: Semester
    priority_0: int
    priority_1: int
    priority_2: int
    priority_3: int
    priority_4: int


class BlockVisit(BaseModel):
    """
    A block visit, i.e. an observation made for a block.

    Fields
    ------
    block_visit_id:
        Database id of the block visit.
    block_id:
        Database id of the observed block.
    block_name:
        Name of the observed block.
    observed_time:
        he nominal time spent on making the observation. This is the time charged for,
        and may differ from the actual time spent.
    semester:
        Semester to which the block visit belongs. This is the semester whose time
        allocation was used. As an observation may be made before the semester starts
        (if there are gaps in the observation queue), the semester is not necessarily
        the semester to which the observation night belongs.
    priority:
       Priority of the block.
    max_lunar_phase:
       The maximum lunar phase allowed for the observation. The lunar phase is the
       illuminated fraction of the Moon, as a percentage. It is taken to be 0 if the
       Moon is below the horizon.
    target_name:
       Names of the observed target.
    observation_night:
       Date of the observation night. This is the date when the night starts, i.e. all
       observation done during the same night have the same observation night date.
    status:
       Status of the observation, such "Accepted" or "Rejected".
    rejection_reason:
       Reason why the observation has been rejected.
    """

    block_visit_id: int
    block_id: int
    block_name: str
    observed_time: str
    priority: str
    max_lunar_phase: str
    target_name: str
    observation_night: date
    semester: Semester
    status: str
    rejection_reason: Optional[str]


class PartnerPercentage(BaseModel):
    """
    A percentage (for example of the requested time) for a partner.
    """

    partner: Partner
    percentage: int = Field(ge=0, le=100)


class Phase1Target(BaseModel):
    """
    Target details in a Phase 1 proposal.

    Fields
    ------
    name:
        Target name.
    right_ascension:
        Right ascension, in degrees.
    declination:
        Declination, in degrees.
    equinox:
        Equinox for the target coordinates.
    horizons_identifier:
        Identifier in the Horizons database for solar system targets.
    minimum_magnitude:
        Minimum magnitude of the target.
    maximum_magnitude:
        Maximum magnitude.
    target_type:
        Target type (broad category).
    target_subtype:
        Target subtype.
    is_optional:
        Whether the target is optional. i.e. whether it is part of a pool of targets
        from which only a subset needs to be observed.
    n_visits:
        The number of observations requested for the target.
    max_lunar_phase:
        The maximum lunar phase allowed for an observation of the target. The lunar
        phase is the illuminated fraction of the Moon, as a percentage. It is taken to
        be 0 if the Moon is below the horizon.
    ranking:
        Importance attributed by the Principal Investigator to observations of this
        target relative to other observations for the same proposal.
    night_count:
        The number of nights when the target can be observed, given the requested
        observation time and observation constraints.
    TODO: Comment on probabilities
    """

    name: str
    right_ascension: float
    declination: float
    equinox: float
    horizons_identifier: Optional[str]
    minimum_magnitude: float
    maximum_magnitude: float
    target_type: str
    target_subtype: str
    is_optional: bool
    n_visits: int
    max_lunar_phase: float
    ranking: str
    night_count: int
    moon_probability: Optional[int]
    competition_probability: Optional[int]
    observability_probability: Optional[int]
    seeing_probability: Optional[int]


class RequestedTime(BaseModel):
    """
    Time requested for a proposal in a phase 1 proposal or a progress report.

    Fields
    ------
    total_requested_time:
        The total requested time, in seconds.
    minimum_useful_time:
        The minimum time needed to prode meaningful science from the proposal, in
        seconds.
    time_comment:
        Comment on the time requirements.
    semester:
        Semester for which the time is requested.
    distribution:
        Percentages of time requested from the different partners.
    """

    total_requested_time: int
    minimum_useful_time: Optional[int]
    comment: Optional[str]
    semester: Semester
    distribution: List[PartnerPercentage]


class BaseProposal(BaseModel):
    """
    Base model for phase 1 and phase 2 proposals.

    Fields
    ------
    text_content:
        Text content of the proposal.
    investigators:
        Investigators on the proposal.
    """

    text_content: List[TextContent]
    investigators: List[Investigator]


class Phase1Proposal(BaseProposal):
    """
    A phase 1 proposal.

    Fields
    ------
    phase:
        Proposal phase. Must be 1.
    targets:
        Targets for which observations are requested.
    requested_time:
        Time requested for the proposal.
    """

    phase: int = Field(gt=0, lt=2)
    targets: List[Phase1Target]
    requested_time: List[RequestedTime]


class Phase2Proposal(BaseProposal):
    """
    A phase 2 proposal.

    Fields
    ------
    phase:
        Proposal phase. Must be 2.
    block_visits:
        Block visits (observations made) for the proposal.
    observed_time
    """

    phase: int = Field(gt=1, lt=3)
    block_visits: List[BlockVisit]
    observed_time: List[ObservedTime]
    time_allocations: List[TimeAllocation]


# -------------------------


class Message(BaseModel):
    message: str = Field(..., title="Message", description="Message")

    class Config:
        schema_extra = {"example": {"message": "This is a message."}}


class ProposalCode(str):
    """
    A string denoting a semester, such as "2021-2-SCI-017".

    The string must consist of a four-digit year (between 2000 and 2099) followed by a
    dash, the semester ("1" or "2"), another dash, a combination of uppercase letters
    and underscores (which must start and end with a letter), another dash and three
    digits.
    """

    # Based on https://pydantic-docs.helpmanual.io/usage/types/#custom-data-types
    proposal_code_regex = r"20\d{2}-[12]-[A-Z][A-Z_]*[A-Z]-\d{3}"

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[[str], str], None, None]:
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[Any, Any]) -> None:
        field_schema.update(
            pattern=ProposalCode.proposal_code_regex, examples=["2021-2-SCI-017"]
        )

    @classmethod
    def validate(cls, v: str) -> str:
        if not isinstance(v, str):
            raise TypeError("string required")
        m = re.match(SemesterString.semester_regex, v)
        if not m:
            raise ValueError("incorrect proposal code format")
        return v


class SemesterString(str):
    """
    A string denoting a semester, such as "2021-2" or "2022-1".

    The string must consist of a four-digit year (between 2000 and 2099) followed by a
    dash and "1" or "2".
    """

    # Based on https://pydantic-docs.helpmanual.io/usage/types/#custom-data-types
    semester_regex = r"20\d{2}-[12]"

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[[str], str], None, None]:
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[Any, Any]) -> None:
        field_schema.update(
            pattern=SemesterString.semester_regex, examples=["2021-2", "2022-1"]
        )

    @classmethod
    def validate(cls, v: str) -> str:
        if not isinstance(v, str):
            raise TypeError("string required")
        m = re.match(SemesterString.semester_regex, v)
        if not m:
            raise ValueError("incorrect semester format")
        return v


class ProposalListItem(BaseModel):
    """
    Item in a list of proposals.
    """

    proposal_code: str = Field(..., title="Proposal code", description="Proposal code")

    class Config:
        schema_extra = {"example": {"proposal_code": "2021-1-SCI-074"}}


class SubmissionAcknowledgment(BaseModel):
    """
    Acknowledgment that a proposal submission has been received.
    """

    submission_id: int = Field(
        ...,
        title="Submission id",
        description="Unique identifier for a proposal submission",
    )

    class Config:
        schema_extra = {"example": {"submission_id": 41318}}


class ProposalContentType(str, Enum):
    JSON = ("application/json",)
    PDF = ("application/pdf",)
    ZIP = "application/zip"


class ProposalStatus(str, Enum):
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


class ProposalStatusContent(BaseModel):
    """
    Content including a proposal status.
    """

    status: ProposalStatus = Field(
        ..., title="Proposal status", description="Proposal status"
    )


class ProposalContent(BaseModel):
    """
    Helper class.

    mypy does not like if a Union is used as the value of FastAPI's response_model in a
    path operation's decorator, so Union[Phase1Proposal, Phase2Proposal] cannot be used.
    This class can used instead.
    """

    __root__: Union[Phase1Proposal, Phase2Proposal]


class ObservationComment(BaseModel):
    """
    Comment related to an observation of a proposal.
    """

    author: str = Field(..., title="Author", description="Author of the comment")
    comment: str = Field(..., title="Comment", description="Text of the comment")
    madeAt: datetime = Field(
        ...,
        title="Time of creation",
        description="Date amd time when the comment was made",
    )

    class Config:
        schema_extra = {
            "example": {
                "author": "Sipho Mangana",
                "comment": "Please check the position angle.",
                "madeAt": "2019-08-24T14:15:22Z",
            }
        }


class ProgressReport(BaseModel):
    """
    Progress report for a proposal and semester. The semester is the semester for which
    the progress is reported. For example, if the semester is 2021-1, the report covers
    the observations up to and including the 2021-1 semester and it requests time for
    the 2021-2 semester.
    """

    dummy: str


class Priority(IntEnum):
    P0 = 0
    P1 = 1
    P2 = 2
    P3 = 3
    P4 = 4


class ObservedTarget(BaseModel):
    id: int = Field(
        ..., title="Target id", description="Unique identifier of the target"
    )
    name: str = Field(..., title="Target name", description="Target name")


class ObservationStatus(str, Enum):
    ACCEPTED = "Accepted"
    REJECTED = "Rejected"


class Observation(BaseModel):
    id: int = Field(
        ..., title="Observation id", description="Unique identifier of the observation"
    )
    observation_time: int = Field(
        ...,
        title="observation time",
        description="Time charged for the observation, in seconds",
    )
    block_id: int = Field(
        ..., title="Block id", description="Unique identifier of the observed block"
    )
    priority: Priority = Field(
        ..., title="Priority", description="Priority of the observed block"
    )
    max_lunar_phase: float = Field(
        ...,
        title="Maximum lunar phase",
        description="Maximum lunar phase which was allowed for the observation, "
        "as the percentage of lunar illumination",
    )
    targets: List[ObservedTarget] = Field(
        ..., title="Observed targets", description="Observed targets"
    )
    observation_night: date = Field(
        ...,
        title="Observation night",
        description="Start date of the night when the observation was made",
    )
    status: ObservationStatus = Field(
        ...,
        title="Observation status",
        description="Status of the observation, "
        "i.e. whether it has been accepted or rejected",
    )
    rejection_reason: Optional[str] = Field(
        None,
        title="Rejection reason",
        description="Reason why the observation has been rejected",
    )


class DataReleaseDate(BaseModel):
    release_date: date = Field(
        ...,
        title="Data release date",
        description="Date when the proposal data is scheduled to become public",
    )


class DataReleaseDateUpdate(BaseModel):
    release_date: date = Field(
        ...,
        title="Data release date",
        description="Requested date when the proposal data should become public",
    )
    motivation: date = Field(
        ...,
        title="Motivation",
        description="Motivation why the request should be granted",
    )