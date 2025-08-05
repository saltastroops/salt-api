from typing import Any, Dict, List

from saltapi.repository.pipt_repository import PiptRepository


class PiptService:
    def __init__(self, pipt_repository: PiptRepository) -> None:
        self.pipt_repository = pipt_repository

    def get_pipt_news_for_days(self, days: int) -> List[Dict[str, Any]]:
        return self.pipt_repository.get_pipt_news_for_days(days)

    def get_proposal_constraints(
        self, proposal_code: str, year: int = None, semester: int = None
    ) -> List[Dict[str, Any]]:
        return self.pipt_repository.get_proposal_constraints(
            proposal_code, year, semester
        )

    def get_nir_flat_details(self, only_checksum: bool) -> Dict[str, Any]:
        """
        Returns either the checksum or the full flat-field calibration details with checksum.
        """
        checksum = self.pipt_repository.get_nir_flat_checksum()

        if only_checksum:
            return {"checksum": checksum}

        entries = self.pipt_repository.get_nir_flat_details()
        return {"checksum": checksum, "entries": entries}

    def get_nir_arc_details(self, only_checksum: bool) -> Dict[str, Any]:
        """
        Returns either the checksum or the full arc calibration details with checksum.
        """
        checksum = self.pipt_repository.get_nir_arc_checksum()

        if only_checksum:
            return {"checksum": checksum}

        exposures = self.pipt_repository.get_exposures()
        allowed_lamp_setups = self.pipt_repository.get_allowed_nir_lamp_setups()
        preferred_lamp_setups = self.pipt_repository.get_preferred_nir_lamp_setups()

        return {
            "checksum": checksum,
            "exposures": exposures,
            "allowed_lamp_setups": allowed_lamp_setups,
            "preferred_lamp_setups": preferred_lamp_setups,
        }
