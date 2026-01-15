from typing import Any, Dict, List, Optional

from saltapi.repository.pipt_repository import PiptRepository
from saltapi.service.user import User


class PiptService:
    def __init__(self, pipt_repository: PiptRepository) -> None:
        self.pipt_repository = pipt_repository

    def get_pipt_news_for_days(self, days: int) -> List[Dict[str, Any]]:
        return self.pipt_repository.get_pipt_news_for_days(days)

    def get_proposal_constraints(
        self, proposal_code: str, semester: str = None
    ) -> List[Dict[str, Any]]:
        return self.pipt_repository.get_proposal_constraints(proposal_code, semester)

    def get_nir_flat_details(self) -> Dict[str, Any]:
        """
        Return full flat field calibration details.
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
        Return the arc calibration details for non-SMI RSS setups.
        """
        exposure_times = self.pipt_repository.get_rss_exposure_times()
        allowed_lamp_setups = self.pipt_repository.get_rss_allowed_lamps()
        preferred_lamp_setups = self.pipt_repository.get_rss_preferred_lamps()

        return {
            "exposure_times": exposure_times,
            "allowed_lamps": allowed_lamp_setups,
            "preferred_lamps": preferred_lamp_setups,
        }

    def get_rss_ring_details(self) -> Dict:
        """Return calibration regions and lines for non-SMI RSS setups."""
        calibration_regions = self.pipt_repository.get_rss_calibration_regions()
        calibration_lines = self.pipt_repository.get_rss_calibration_lines()

        return {
            "fp_calibration_regions": calibration_regions,
            "fp_calibration_lines": calibration_lines,
        }

    def get_smi_flat_details(self) -> Dict[str, Any]:
        """
        Return the flat field calibration details for non-SMI RSS setups.
        """
        entries = self.pipt_repository.get_smi_flat_details()
        return {"entries": entries}

    def get_smi_arc_details(self) -> Dict[str, Any]:
        """
        Return the arc calibration details for non-SMI RSS setups.
        """
        allowed_lamp_setups = self.pipt_repository.get_smi_allowed_lamp_setups()
        preferred_lamp_setups = self.pipt_repository.get_smi_preferred_lamp_setups()
        exposures = self.pipt_repository.get_smi_arc_details()

        return {
            "allowed_lamp_setups": allowed_lamp_setups,
            "preferred_lamp_setups": preferred_lamp_setups,
            "exposures": exposures,
        }

    def get_previous_proposals_info(
        self,
        user_id: int,
        from_semester: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Return a list of previous proposals for the given user starting from
        the specified semester (e.g. "2024-1"). If not provided, defaults to
        3 semesters ago.
        """
        return self.pipt_repository.get_previous_proposals_info(
            user_id=user_id,
            from_semester=from_semester,
        )

    def get_block_visits(self, proposal_code: str) -> List[Dict[str, Any]]:
        """
        Return a list of block visits for a given proposal code.
        """
        return self.pipt_repository.get_block_visits(proposal_code)

    def get_proposals(
        self,
        user: User,
        phase: int,
        limit: Optional[int] = None,
        descending: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        Fetch proposals, optionally filtered by phase.
        """
        return self.pipt_repository.get_proposals(
            user=user,
            phase=phase,
            limit=limit,
            descending=descending,
        )

    def get_partners(self) -> List[Dict[str, Any]]:
        """Fetch the partner information."""
        return self.pipt_repository.get_partners()

    def get_investigator(
        self, email: str, preferred_institute: Optional[str]
    ) -> dict[str, Any]:
        """Fetch the investigator."""
        return self.pipt_repository.get_investigator(email, preferred_institute)

    def get_current_version(self) -> Dict[str, Any]:
        """Fetch the current PIPT version."""
        return self.pipt_repository.get_current_version()
