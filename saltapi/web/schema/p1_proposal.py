from typing import List, Optional

from pydantic import BaseModel, Field

from saltapi.web.schema.common import ObservationProbabilities, Ranking
from saltapi.web.schema.proposal import GeneralProposalInfo, Proposal
from saltapi.web.schema.target import Target


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


class P1Observation(BaseModel):
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
    target: Target = Field(
        ...,
        title="Target",
        description="Target of observations.",
    )


class P1Proposal(Proposal):
    """A phase 1 proposal."""

    general_info: P1GeneralProposalInfo = Field(
        ...,
        title="General information",
        description="General proposal information for a semester",
    )
    observations: Optional[List[P1Observation]] = Field(
        ...,
        title="Targets",
        description="Targets for which observations are requested.",
    )
    science_configurations: List[ScienceConfiguration] = Field(
        title="Instruments configurations",
        description="The phase 1 instruments configurations.",
    )
