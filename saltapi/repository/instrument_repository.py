from typing import Any, Dict, List

from sqlalchemy.engine import Connection

from saltapi.repository.bvit_repository import BvitRepository
from saltapi.repository.hrs_repository import HrsRepository
from saltapi.repository.nir_repository import NirRepository
from saltapi.repository.rss_repository import RssRepository
from saltapi.repository.salticam_repository import SalticamRepository
from saltapi.service.instrument import BVIT, HRS, NIR, RSS, Salticam
from saltapi.web.schema.rss import RssMaskType


class InstrumentRepository:
    def __init__(self, connection: Connection) -> None:
        self.salticam_repository = SalticamRepository(connection)
        self.rss_repository = RssRepository(connection)
        self.hrs_repository = HrsRepository(connection)
        self.bvit_repository = BvitRepository(connection)
        self.nir_repository = NirRepository(connection)

    def get_salticam(self, salticam_id: int) -> Salticam:
        """Return a Salticam setup."""
        return self.salticam_repository.get(salticam_id)

    def get_rss(self, rss_id: int) -> RSS:
        """Return an RSS setup."""
        return self.rss_repository.get(rss_id)

    def get_hrs(self, hrs_id: int) -> HRS:
        """Return an HRS setup."""
        return self.hrs_repository.get(hrs_id)

    def get_bvit(self, bvit_id: int) -> BVIT:
        """Return a BVIT setup."""
        return self.bvit_repository.get(bvit_id)

    def get_nir(self, nir_id: int) -> NIR:
        """Return a NIR setup."""
        return self.nir_repository.get(nir_id)

    def get_rss_masks_in_magazine(self, mask_types: List[RssMaskType]) -> List[str]:
        """The list of masks in the magazine."""
        return self.rss_repository.get_mask_in_magazine(mask_types)

    def get_mos_masks_metadata(
        self, from_semester: str, to_semester: str
    ) -> List[Dict[str, Any]]:
        """The list of MOS masks metadata."""
        return self.rss_repository.get_mos_masks_metadata(from_semester, to_semester)

    def get_mos_mask_metadata(self, barcode: str) -> Dict[str, Any]:
        """Get MOS mask metadata."""
        return self.rss_repository.get_mos_mask_metadata(barcode)

    def update_mos_mask_metadata(
        self, mos_mask_metadata: Dict[str, Any]
    ) -> None:
        """Update MOS mask metadata"""
        return self.rss_repository.update_mos_mask_metadata(mos_mask_metadata)

    def get_obsolete_rss_masks_in_magazine(
        self, mask_types: List[RssMaskType]
    ) -> List[str]:
        """The list of obsolete RSS masks."""
        return self.rss_repository.get_obsolete_rss_masks_in_magazine(mask_types)
