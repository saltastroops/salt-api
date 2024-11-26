from typing import List, Dict, Any

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query

from saltapi.repository.unit_of_work import UnitOfWork
from saltapi.service.authentication_service import get_current_user
from saltapi.service.user import User
from saltapi.web import services
from saltapi.web.schema.common import Semester
from saltapi.web.schema.rss import (
    MosBlock,
    MosMaskMetadata,
    RssMaskType,
    UpdateMosMaskMetadata, RssMask,
)

router = APIRouter(tags=["Instrument"])


@router.get(
    "/rss/masks-in-magazine",
    summary="Get current RSS masks in the magazine",
    response_model=List[str],
)
def get_rss_masks_in_magazine(
    mask_types: List[RssMaskType] = Query(
        [], title="Mask type", description="The mask type.", alias="mask-type"
    ),
) -> List[str]:
    """
    Returns the list of masks in the magazine, optionally filtered by mask types.

    The following mask types values are possible.

    Mask Type | Description
    --- | ---
    Longslit | Longslit
    Imaging | Imaging mask
    MOS | Mask for multi-object spectroscopy
    Engineering | Engineering mask.
    """
    with UnitOfWork() as unit_of_work:
        instrument_service = services.instrument_service(unit_of_work.connection)
        return instrument_service.get_rss_masks_in_magazine(mask_types)


@router.get(
    "/rss/mos-mask-metadata",
    summary="Get MOS data",
    response_model=List[MosBlock],
    status_code=200,
)
def get_mos_masks_metadata(
    user: User = Depends(get_current_user),
    from_semester: Semester = Query(
        "2000-1",
        alias="from",
        description="Only include MOS masks for this semester and later.",
        title="From semester",
    ),
    to_semester: Semester = Query(
        "2099-2",
        alias="to",
        description="Only include MOS masks for this semester and earlier.",
        title="To semester",
    ),
) -> List[Dict[str, Any]]:
    """
    Get the list of blocks using MOS.
    """
    with UnitOfWork() as unit_of_work:
        if from_semester > to_semester:
            raise HTTPException(
                status_code=400,
                detail="The from semester must not be later than the to semester.",
            )
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_view_mos_mask_metadata(user)

        instrument_service = services.instrument_service(unit_of_work.connection)
        mos_blocks = instrument_service.get_mos_masks_metadata(
            from_semester, to_semester
        )
        return  mos_blocks


@router.patch(
    "/rss/mos-mask-metadata/{barcode}",
    summary="Update MOS mask metadata",
    response_model=MosMaskMetadata,
    status_code=200,
)
def update_mos_mask_metadata(
    mos_mask_metadata: UpdateMosMaskMetadata = Body(
        ..., title="The Slit mask", description="Semester"
    ),
    barcode: str = Path(..., title="Barcode", description="The barcode of slit mask"),
    user: User = Depends(get_current_user),
) -> MosMaskMetadata:
    """
    Update MOS mask metadata.
    """
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_update_mos_mask_metadata(user)

        instrument_service = services.instrument_service(unit_of_work.connection)
        args = dict(mos_mask_metadata)
        args["barcode"] = barcode
        instrument_service.update_mos_mask_metadata(args)

        unit_of_work.connection.commit()

        mask_metadata = instrument_service.get_mos_mask_metadata(barcode)
        return MosMaskMetadata(**mask_metadata)


@router.get(
    "/rss/obsolete-masks-in-magazine",
    summary="Get the RSS masks in the magazine that are no longer needed",
    response_model=List[str],
)
def get_obsolete_rss_masks_in_magazine(
    mask_types: List[RssMaskType] = Query(
        [],
        title="Mask types",
        description="The mask types to check.",
        alias="mask-type",
    ),
    user: User = Depends(get_current_user),
) -> List[str]:
    """
    Returns the list of obsolete RSS masks.
    """
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_view_obsolete_masks_in_magazine(user)

        instrument_service = services.instrument_service(unit_of_work.connection)
        return instrument_service.get_obsolete_rss_masks_in_magazine(mask_types)

@router.get(
    "/rss/slit-masks",
    summary="Get the RSS slit masks.",
    response_model=List[RssMask],
)
def get_rss_slit_masks(
        exclude_mask_types: List[RssMaskType] = Query(
            [],
            title="Mask types",
            description="The mask types to exclude",
            alias="exclude-mask-type",
        ),
        user: User = Depends(get_current_user),
) -> List[Dict[str, Any]]:
    """
    Returns the list of RSS slit masks.
    """
    with UnitOfWork() as unit_of_work:
        permission_service = services.permission_service(unit_of_work.connection)
        permission_service.check_permission_to_view_rss_masks(user)

        instrument_service = services.instrument_service(unit_of_work.connection)
        return instrument_service.get_rss_slit_masks(exclude_mask_types)
