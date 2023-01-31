from typing import List, Optional

from pydantic import BaseModel, Field

from saltapi.web.schema.proposal import GeneralProposalInfo, Proposal
from saltapi.web.schema.target import Phase1Target


class Simulation(BaseModel):
    name: Optional[str] = Field(
        ..., title="Simulation name", description="The simulation name."
    )
    url: str = Field(
        ..., title="Simulation URL", description="The URL for the simulation file."
    )
    description: Optional[str] = Field(
        ..., title="Description", description="A Description of the simulation."
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
        description="Is the proposal only requesting priority 4 time?",
    )
    target_of_opportunity_reason: Optional[str] = Field(
        ..., title="ToO reason", description="Reason for ToO flag"
    )


class ScienceConfiguration(BaseModel):
    instrument: str = Field(..., title="Instrument", description="The instrument name.")
    mode: str = Field(
        ...,
        title="Configuration mode",
        description=(
            "The configuration mode. This is the filter for BVIT, the exposure mode for"
            " HRS, the grating for RSS and NIR, and the detector mode for Salticam."
        ),
    )
    simulations: List[Simulation] = Field(
        ..., title="Simulations", description="The simulations for the proposal."
    )


class P1Proposal(Proposal):
    """A phase 1 proposal."""

    general_info: P1GeneralProposalInfo = Field(
        ...,
        title="General information",
        description="General proposal information for a semester",
    )
    targets: Optional[List[Phase1Target]] = Field(
        ...,
        title="Targets",
        description="Targets for which observations are requested.",
    )
    science_configurations: List[ScienceConfiguration] = Field(
        title="Instruments configurations",
        description="The phase 1 instruments configurations.",
    )
    proposal_summary: str = Field(
        ...,
        title="Proposal summary",
        description="URL of a pdf document containing a proposal summary",
    )
