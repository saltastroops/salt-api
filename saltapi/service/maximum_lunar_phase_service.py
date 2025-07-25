from typing import Any, Dict

from saltapi.repository.maximum_lunar_phase_repository import \
    LunarPhaseRepository


class MaximumLunarPhaseService:
    def __init__(self, maximum_lunar_phase_repository: LunarPhaseRepository) -> None:
        self.maximum_lunar_phase_repository = maximum_lunar_phase_repository

    def get_maximum_lunar_phases(self, proposal_code: str) -> Dict[str, Any]:
        return self.maximum_lunar_phase_repository.get_by_proposal_code(proposal_code)
