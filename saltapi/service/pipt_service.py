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

    def get_nir_flat_details(self) -> Dict[str, Any]:
        """
        Returns full flat-field calibration details.
        """

        entries = self.pipt_repository.get_nir_flat_details()
        return {"entries": entries}

    def get_nir_arc_details(self) -> Dict[str, Any]:
        """
        Returns full arc calibration details.
        """

        exposures = self.pipt_repository.get_exposures()
        allowed_lamp_setups = self.pipt_repository.get_allowed_nir_lamp_setups()
        preferred_lamp_setups = self.pipt_repository.get_preferred_nir_lamp_setups()

        return {
            "exposures": exposures,
            "allowed_lamp_setups": allowed_lamp_setups,
            "preferred_lamp_setups": preferred_lamp_setups,
        }

    def get_rss_arc_details(self) -> Dict[str, list[dict]]:
        """
        Returns the arc calibration details for RSS.
        """
        exposure_times = self.pipt_repository.get_rss_exposure_times()
        allowed_lamp_setups = self.pipt_repository.get_rss_allowed_lamps()
        preferred_lamp_setups = self.pipt_repository.get_rss_preferred_lamps()

        return {
            "exposure_times": exposure_times,
            "allowed_lamps": allowed_lamp_setups,
            "preferred_lamps": preferred_lamp_setups,
        }

    def get_rss_ring_details(self, version: str = "1") -> Dict:
        calibration_regions = self.pipt_repository.get_rss_calibration_regions(version)

        if version == "2":
            calibration_lines = self.pipt_repository.get_rss_calibration_lines()
            return {
                "fp_calibration_regions": calibration_regions,
                "fp_calibration_lines": calibration_lines,
            }
        else:
            return {"ring_details": calibration_regions}

    def get_smi_flat_details(self) -> Dict[str, Any]:
        """
        Returns full flat-field calibration details for SMI.
        """
        entries = self.pipt_repository.get_smi_flat_details()
        return {"entries": entries}

    def get_smi_arc_details(self) -> Dict[str, Any]:
        """
        Returns full arc calibration details for SMI.
        """
        allowed_lamp_setups = self.pipt_repository.get_smi_allowed_lamp_setups()
        preferred_lamp_setups = self.pipt_repository.get_smi_preferred_lamp_setups()
        exposures = self.pipt_repository.get_smi_arc_details()

        return {
            "allowed_lamp_setups": allowed_lamp_setups,
            "preferred_lamp_setups": preferred_lamp_setups,
            "exposures": exposures,
        }
