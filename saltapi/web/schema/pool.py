from typing import List

from pydantic import BaseModel, Field


class PoolBlock(BaseModel):
    id: int = Field(
        ...,
        title="Block id",
        description="The block id"
    )
    name: str = Field(
        ...,
        title="Block name",
        description="The block name"
    )
    priority: int = Field(
        ...,
        title="Block's priority",
        description="The priority of the block"
    )
    maximum_lunar_phase: float = Field(
        ...,
        title="Maximum lunar phase",
        description="The maximum lunar phase"
    )
    n_visits: str = Field(
        ...,
        title="Number of visits",
        description="The number of visits required by the block"
    )
    n_done: str = Field(
        ...,
        title="Number of visits done",
        description="The number of visits done for the block"
    )
    status: str = Field(
        ...,
        title="Block status",
        description="The Block status"
    )
    observation_time: str = Field(
        ...,
        title="Observation time",
        description="The time required to observe this block."
    )
    total_observed_time: str = Field(
        ...,
        title="Total observed time",
        description="The total observed time"
    )
    is_observable_tonight: bool = Field(
        ...,
        title="Is block visible to night",
        description="Determine weather the block will be visible to night"
    )


class PoolAllocations(BaseModel):
    priority: int = Field(
        ...,
        title="Pool priority",
        description="The pools priority",
    )
    assigned_time: float = Field(
        ...,
        title="Preferred exposure time",
        description="Preferred (corrected) exposure time, in seconds",
    )
    used_time: float = Field(
        ...,
        title="Total used time",
        description="The total used time"
    )


class Pool(BaseModel):
    """RSS arc bible entry."""

    id: int = Field(
        ...,
        title="Pool id",
        description="The pool id"
    )
    name: str = Field(
        ...,
        title="Pool name",
        description="The pool name"
    )
    description: str = Field(
        ...,
        title="Pool description",
        description="Describing that type of a pool it is."
    )

    blocks: List[PoolBlock] = Field(
        ...,
        title="Original exposure time",
        description="Original exposure time, in seconds",
    )
    allocations: List[PoolAllocations] = Field(
        ...,
        title="Pool allocation",
        description="The pool's time allocations"
    )
