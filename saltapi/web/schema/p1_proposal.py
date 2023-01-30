from enum import Enum
from typing import Optional, List, Literal

from pydantic import BaseModel, Field

from saltapi.service.proposal import ProposalCode
from saltapi.web.schema.common import Semester
from saltapi.web.schema.proposal import Investigator, RequestedTime, TimeAllocation, \
    GeneralProposalInfo, Proposal
from saltapi.web.schema.target import Phase1Target
from saltapi.web.schema.user import FullName


class ThesisType(str, Enum):
    MASTERS = "Masters",
    PHD = "PhD"


class Simulation(BaseModel):
    name: Optional[str] = Field(
        ...,
        title="Simulation name",
        description="The simulation name."
    )
    path: str = Field(
        ...,
        title="Simulation path",
        description="The path to the simulation file."
    )
    description: Optional[str] = Field(
        ...,
        title="Description",
        description="A Description of the simulation."
    )


class StudentThesis(BaseModel):
    student: FullName = Field(
        ...,
        title="Student",
        description="The student doing thesis"
    )
    thesis_type: ThesisType = Field(
        ...,
        title="Thesis type",
        description="The thesis type"
    )
    relevance_of_proposal: Optional[str] = Field(
        ...,
        title="Relevance of proposal",
        description="Importance and contribution of the proposal too the thesis."
    )
    year_of_completion: str = Field(
        ...,
        title="Year of completion",
        description="The year when the thesis is expected to be completed."
    )



class P1GeneralProposalInfo(GeneralProposalInfo):
    """Phase 1 general proposal information for a semester."""
    is_time_restricted: bool = Field(
        ...,
        title="Are there restrictions for the observing times?",
        description="Are there restrictions for the observing times?",
    )
    is_priority4: bool = Field(
        ...,
        title="Is the proposal a priority 4 proposal?",
        description=(
            "Is the proposal only requesting priority 4 time?"
        ),
    )
    is_self_activatable: bool = Field(
        ...,
        title="Can the proposal be self-activated?",
        description=(
            "Can the proposal be activated by the Principal Investigator or Principal"
            " Contact?"
        ),
    )
    thesis_students: List[StudentThesis] = Field(
        ...,
        title="Students",
        description="The list of student doing thesis on this proposal"

    )
    target_of_opportunity_reason: Optional[str] = Field(
        ...,
        title="ToO reason",
        description="Reason for ToO flag"
    )



class ScienceConfiguration(BaseModel):
    instrument: str = Field(
        ...,
        title="Instrument",
        description="The instrument name."
    )
    mode: str = Field(
        ...,
        title="Configuration mode",
        description=("The configuration mode. This is the filter for BVIT, the exposure mode for HRS,"
                     " the grating for RSS and NIR, and the detector mode for Salticam.")
    )
    simulations: List[Simulation] = Field(
        ...,
        title="Simulations",
        description="The simulations for the proposal."
    )

class P1Proposal(Proposal):
    """A phase 1 proposal."""

    general_info: P1GeneralProposalInfo = Field(
        ...,
        title="General information",
        description="General proposal information for a semester",
    )
    investigators: List[Investigator] = Field(
        ..., title="Investigators", description="Investigators on the proposal"
    )
    targets: Optional[List[Phase1Target]] = Field(
        ...,
        title="Targets",
        description=(
            "Targets for which observations are requested."
        ),
    )
    requested_times: List[RequestedTime] = Field(
        ...,
        title="Requested times",
        description=(
            "Requested times for all semesters in the proposal."
        ),
    )
    time_allocations: List[TimeAllocation] = Field(
        ...,
        title="Time allocations",
        description="Time allocations for the semester",
    )
    science_configurations: List[ScienceConfiguration] = Field(
        title="Instruments configurations",
        description="The phase 1 instruments configurations."
    )
