import subprocess
from pathlib import Path
from typing import Any, Dict, List

from fastapi import HTTPException

from saltapi.repository.instrument_repository import InstrumentRepository
from saltapi.settings import get_settings
from saltapi.web.schema.rss import RssMaskType


class InstrumentService:
    def __init__(self, instrument_repository: InstrumentRepository):
        self.instrument_repository = instrument_repository

    def get_rss_masks_in_magazine(self, mask_types: List[RssMaskType]) -> List[str]:
        """The list of masks in the magazine."""
        return self.instrument_repository.get_rss_masks_in_magazine(mask_types)

    def get_mos_masks_metadata(
        self, from_semester: str, to_semester: str
    ) -> List[Dict[str, Any]]:
        """The list of MOS masks metadata."""
        return self.instrument_repository.get_mos_masks_metadata(
            from_semester, to_semester
        )

    def get_mos_mask_metadata(self, barcode: str) -> Dict[str, Any]:
        """Get MOS mask metadata."""
        return self.instrument_repository.get_mos_mask_metadata(barcode)

    def update_mos_mask_metadata(self, mos_mask_metadata: Dict[str, Any]) -> None:
        """Update slit mask information"""
        return self.instrument_repository.update_mos_mask_metadata(mos_mask_metadata)

    def get_obsolete_rss_masks_in_magazine(
        self, mask_types: List[RssMaskType]
    ) -> List[str]:
        """The list of obsolete RSS masks."""
        return self.instrument_repository.get_obsolete_rss_masks_in_magazine(mask_types)

    def get_rss_slit_masks(
        self, exclude_mask_types: List[RssMaskType]
    ) -> List[Dict[str, Any]]:
        """The list of the RSS slit masks."""
        return self.instrument_repository.get_rss_slit_masks(exclude_mask_types)

    def get_filter_details(self, semesters: List[str]) -> List[Dict[str, Any]]:
        return self.instrument_repository.get_filter_details(semesters)

    def get_rss_mask_xml_file(self, barcode: str, proposal_code: str) -> Path:
        """Get the full path of an xml for a given MOS mask barcode."""
        xml_path_str = self.instrument_repository.get_xml_filename_by_barcode(barcode)
        xml_file = get_settings().proposals_dir / proposal_code / xml_path_str

        if not xml_file.exists():
            raise HTTPException(
                status_code=404, detail=f"Slit mask XML not found: {xml_file}"
            )

        return xml_file

    def generate_slitmask_gcode(
        self,
        barcode: str,
        proposal_code: str,
        tmp_file: Path,
        using_boxes_for_refstars: bool,
        refstar_boxsize: int,
        slow_cutting_power: float,
    ) -> Path:
        """Generate GCode for a slit mask and return the output file path."""

        xml_file = self.get_rss_mask_xml_file(barcode, proposal_code)
        settings = get_settings()

        cmd = [
            settings.java_command,
            "-jar",
            settings.xml_to_gcode_jar_path,
            f"--slow-cutting-power={slow_cutting_power}",
            f"--xml={xml_file}",
            f"--gcode={tmp_file}",
            f"--barcode={barcode}",
        ]
        if using_boxes_for_refstars:
            cmd.extend(
                ["--boxes-for-refstars", "--refstar-boxsize", str(refstar_boxsize)]
            )

        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError:
            raise HTTPException(status_code=500, detail="GCode generation failed")

        return tmp_file
