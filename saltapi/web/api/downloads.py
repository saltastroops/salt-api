import os

from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.responses import FileResponse

from saltapi.repository.unit_of_work import UnitOfWork
from saltapi.web import services
from saltapi.service.user import User
from saltapi.service.authentication_service import get_current_user


router = APIRouter(prefix="/downloads", tags=["Downloads"])

@router.get("/slit-mask-xml/{proposal_code}/{filename}", summary="Get a slit mask XML")
async def download_xml_file(
        proposal_code: str = Path(
            ...,
            title="Proposal code",
            description="The proposal code",
        ),
        filename: str = Path(
            ...,
            title="XML filename",
            description=(
                    "Name of the XML file, as a unique identifier and a "
                    "suffix, such as 1234.xml."
            ),
        ),
        user: User = Depends(get_current_user)
)-> FileResponse:

    with UnitOfWork() as unit_of_work:
        download_services = services.download_service(unit_of_work.connection)
        file_path = download_services.get_slit_mask_xml_path(proposal_code) / filename

        # Check if the file exists
        if not os.path.isfile(file_path):
            raise HTTPException(status_code=404, detail="File not found")

        # Serve the file as a response for download
        return FileResponse(file_path, media_type="application/xml", headers={"Content-Disposition": f"attachment; filename={filename}"})


@router.get("/slit-mask-plot/{proposal_code}/{filename}", summary="Get a slit mask plot file")
async def download_plot_file(
        proposal_code: str = Path(
            ...,
            title="Proposal code",
            description="The proposal code",
        ),
        filename: str = Path(
            ...,
            title="Plot filename",
            description=(
                    "Name of the plot file, as a unique identifier and a "
                    "suffix, such as 1234.jpg."
            ),
        ),
        user: User = Depends(get_current_user)
)-> FileResponse:

    with UnitOfWork() as unit_of_work:
        download_services = services.download_service(unit_of_work.connection)
        file_path = download_services.get_slit_mask_plot_path(proposal_code) / filename

        # Check if the file exists
        if not os.path.isfile(file_path):
            raise HTTPException(status_code=404, detail="File not found")

        # Determine media_type based on file extension
        if filename.endswith(".jpg") or filename.endswith(".jpeg"):
            media_type = "image/jpeg"
        elif filename.endswith(".png"):
            media_type = "image/png"
        elif filename.endswith(".svg"):
            media_type = "image/svg+xml"
        elif filename.endswith(".bmp"):
            media_type = "image/bmp"
        else:
            raise HTTPException(status_code=400, detail="Unsupported image format")

        # Serve the file as a response for download
        return FileResponse(file_path, media_type=media_type)