from typing import List, Optional, Union, Literal
from pydantic import BaseModel, Field
from datetime import date, datetime

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


class Submission(BaseModel):
    submission_date: datetime = Field(
        ..., title="Submission date and time", description="The date of proposal submission."
    )
    submission_number: int = Field(
        ..., title="Submission number", description="The number of proposal submission."
    )


class P1GeneralProposalInfo(GeneralProposalInfo):
    """Phase 1 general proposal information for a semester."""

    is_time_restricted: bool = Field(
        ...,
        title="Are there restrictions for the observing times?",
        description="Are there restrictions for the observing times?",
    )
    is_priority_4: bool = Field(
        ...,
        title="Is the proposal a priority 4 proposal?",
        description="Is the proposal only requesting priority 4 time?",
    )
    target_of_opportunity_reason: Optional[str] = Field(
        ..., title="ToO reason", description="Reason for ToO flag"
    )
    phase_1_submissions: List[Submission] = Field(
        ..., title="Phase 1 submissions", description="The submissions of the phase 1 proposals"
    )
    phase_1_submission_deadline: Optional[date] = Field(
        ..., title="Phase 1 submission deadline", description="The deadline of submitting a phase 1 proposal"
    )



class P1RssModeConfiguration(BaseModel):
    grating: Optional[str] = Field(..., title="Grating", description=" The grating")
    mask_type: Optional[str] = Field(
        ..., title="Mask type", description="The mask type"
    )
    polarimetry_pattern_name: Optional[str] = Field(
        ...,
        title="Polarimetry pattern name",
        description="The polarimetry pattern name",
    )
    fabry_perot_mode: Optional[str] = Field(
        ..., title="Fabry-Pérot mode", description="The Fabry-Pérot mode"
    )


class Filter(BaseModel):
    name: str = Field(..., title="Filter name", description="The filter name")
    description: str = Field(
        ..., title="Filter description", description="The filter description"
    )


class P1Bvit(BaseModel):
    instrument: Literal["BVIT"] = Field(
        ..., title="Instrument name", description="The instrument name"
    )
    filter: Filter = Field(
        ..., title="List of Filters", description="The list of configured filters"
    )


class P1Hrs(BaseModel):
    instrument: Literal["HRS"] = Field(
        ..., title="Instrument name", description="The instrument name"
    )
    detector_mode: str = Field(
        ..., title="Detector mode", description="The detector mode"
    )
    simulations: List[Simulation] = Field(
        ..., title="Simulations", description="The simulations for the proposal."
    )


class P1Nir(BaseModel):
    instrument: Literal["NIR"] = Field(
        ..., title="Instrument name", description="The instrument name"
    )
    grating: str = Field(..., title="Grating", description="The grating")
    simulations: List[Simulation] = Field(
        ..., title="Simulations", description="The simulations for the proposal."
    )


class P1Rss(BaseModel):
    instrument: Literal["RSS"] = Field(
        ..., title="Instrument name", description="The instrument name"
    )
    mode: str = Field(
        ..., title="Configuration mode", description="The configuration mode"
    )
    detector_mode: str = Field(
        ..., title="Detector mode", description="The detector mode"
    )
    rss_mode_configuration: P1RssModeConfiguration = Field(
        ..., title="RSS mode configuratio", description="The RSS mode configurations"
    )
    simulations: List[Simulation] = Field(
        ..., title="Simulations", description="The simulations for the proposal."
    )


class P1Salticam(BaseModel):
    instrument: Literal["SALTICAM"] = Field(
        ..., title="Instrument name", description="The instrument name"
    )
    detector_mode: str = Field(
        ..., title="Detector mode", description="The detector mode"
    )
    filters: List[Filter] = Field(
        ..., title="List of Filters", description="The list of configured filters"
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
    science_configurations: List[
        Union[P1Bvit, P1Hrs, P1Nir, P1Rss, P1Salticam]
    ] = Field(
        title="Instruments configurations",
        description="The phase 1 instruments configurations.",
    )
