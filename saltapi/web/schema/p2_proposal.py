from datetime import date
from typing import List, Optional

from pydantic import Field

from saltapi.web.schema.block import BlockSummary
from saltapi.web.schema.common import BlockVisit
from saltapi.web.schema.proposal import GeneralProposalInfo, ChargedTime, ObservationComment, Proposal


class P2GeneralProposalInfo(GeneralProposalInfo):
    """Phase 2 general proposal information for a semester."""

    data_release_date: Optional[date] = Field(
        ...,
        title="Data release date",
        description="Date when the proposal data is scheduled to become public",
    )

    summary_for_salt_astronomer: str = Field(
        ...,
        title="Summary for the SALT Astronomer",
        description=(
            "Brief summary with the essential information for the SALT Astronomer"
        ),
    )
    summary_for_night_log: str = Field(
        ...,
        title="Summary for the night log",
        description="Brief (one-line) summary to include in the observing night log",
    )
    is_self_activatable: bool = Field(
        ...,
        title="Can the proposal be self-activated?",
        description=(
            "Can the proposal be activated by the Principal Investigator or Principal"
            " Contact?"
        ),
    )

#type: ignore
class P2Proposal(Proposal):

    general_info: P2GeneralProposalInfo = Field(
        ...,
        title="General information",
        description="General proposal information for a semester",
    )
    blocks: List[BlockSummary] = Field(
        ..., title="Blocks", description="Blocks for the semester"
    )
    block_visits: List[BlockVisit] = Field(
        ...,
        title="Observations",
        description="Observations made for the proposal in any semester",
    )
    charged_time: ChargedTime = Field(
        ...,
        title="Charged time, by priority",
        description="Charged time, by priority, for the semester",
    )
    observation_comments: List[ObservationComment] = Field(
        ...,
        title="Observation comments",
        description="Comments related to observing the proposal",
    )
