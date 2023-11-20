from typing import List
from pydantic import BaseModel, Field


class FilterBlock(BaseModel):
    block_id: int = Field(..., title="Block id", description="The block id.")
    is_done: bool = Field(..., title="Are all block visit done", description="Are all block visit done.")


class Filter(BaseModel):
    """Filter item."""

    barcode: str = Field(..., title="Filter name", description="The filter name.")
    is_needed: bool = Field(
        ..., title="Is filter needed",
        description="Is there any block that still need to use this filter."
    )
    in_magazine: bool = Field(
        ..., title="Is filter in a magazine",
        description="Is the filter installed in the magazine."
    )
    blocks: int = Field(
        ..., title="Blocks using this filter.",
        description="The blocks using this filter."
    )
    proposals: List[str] = Field(
        ..., title="Proposal using this filter",
        description="The Proposal codes using this filter."
    )
