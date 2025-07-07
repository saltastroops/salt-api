from typing import List, Optional

from pydantic import BaseModel, Field


class PoolBlock(BaseModel):
    id: int = Field(..., title="Block id", description="The block id")
    name: str = Field(..., title="Block name", description="The block name")
    priority: int = Field(
        ..., title="Block's priority", description="The priority of the block"
    )
    maximum_lunar_phase: float = Field(
        ..., title="Maximum lunar phase", description="The maximum lunar phase"
    )
    n_visits: str = Field(
        ...,
        title="Number of visits",
        description="The number of visits required by the block",
    )
    n_done: str = Field(
        ...,
        title="Number of visits done",
        description="The number of visits done for the block",
    )
    status: str = Field(..., title="Block status", description="The Block status")
    observation_time: str = Field(
        ...,
        title="Observation time",
        description="The time required to observe this block.",
    )
    total_observed_time: str = Field(
        ..., title="Total observed time", description="The total observed time"
    )
    is_observable_tonight: bool = Field(
        ...,
        title="Is block visible to night",
        description="Determine weather the block will be visible to night",
    )


class PoolTimes(BaseModel):
    priority: int = Field(
        ...,
        title="Pool priority",
        description="The pools priority",
    )
    assigned_time: float = Field(
        ...,
        title="Assigned time",
        description="The time assigned to the pool",
    )
    used_time: float = Field(
        ..., title="Total used time", description="The total used time"
    )


class PoolRule(BaseModel):
    rule: str = Field(
        ...,
        title="Pool rule",
        description="The pool's rule",
    )
    rule_parameter: Optional[int] = Field(
        ..., title="Parameter for the rule", description="The parameter for the rule"
    )


class Pool(BaseModel):
    """Pool in a proposal."""

    id: int = Field(..., title="Pool id", description="The pool id")
    name: str = Field(..., title="Pool name", description="The pool name")
    pool_rules: List[PoolRule] = Field(
        ..., title="Pool short rule", description="The pool's short rule"
    )

    blocks: List[PoolBlock] = Field(
        ...,
        title="Pool blocks",
        description="The blocks in the pool",
    )
    pool_times: List[PoolTimes] = Field(
        ..., title="Pool allocation", description="The pool's time allocations"
    )
