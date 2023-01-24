from typing import Optional

from pydantic import BaseModel, Field

from saltapi.web.schema.common import PartnerCode, PartnerName


class Institution(BaseModel):
    """An institution."""

    institution_id: int = Field(
        ...,
        title="Institution id",
        description="Unique identifier of the institution.",
    )
    partner_code: PartnerCode = Field(
        ...,
        title="SALT partner code",
        description="Code of the SALT Partner",
    )
    partner_name: PartnerName = Field(
        ...,
        title="SALT partner name",
        description="Name of the SALT Partner",
    )
    name: str = Field(..., title="Name", description="Name of the institution")
    department: Optional[str] = Field(
        None, title="Department", description="Department of the institution"
    )


class NewInstitutionDetails(BaseModel):
    """New institution details."""

    institution_name: str = Field(..., title="Institution name", description="Name of the institution")
    department: str = Field(..., title="Department", description="Department of the institution")
    address: str = Field(..., title="Address", description="Address of the institution")
    url: str = Field(..., title="URL", description="URL of the institution")
