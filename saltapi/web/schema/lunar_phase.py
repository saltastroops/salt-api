from typing import List

from pydantic import BaseModel, Field


class LunarPhase(BaseModel):
    target: str = Field(..., description="Name of the target")
    phase: float = Field(..., description="Maximum lunar phase")


class LunarPhaseList(BaseModel):
    proposal_code: str = Field(..., description="Proposal code used in the query")
    phases: List[LunarPhase] = Field(..., description="List of target lunar phases")
