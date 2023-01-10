from typing import Any, Dict, List

from saltapi.repository.institution_repository import InstitutionRepository
from saltapi.service.institution import Institution, NewInstitutionDetails


class InstitutionService:
    def __init__(self, repository: InstitutionRepository):
        self.repository = repository

    def get_institutions(self) -> List[Dict[str, Any]]:
        institutions = self.repository.get_institutions()
        return institutions

    def create(self, new_institution_details: NewInstitutionDetails) -> None:
        self.repository.create(new_institution_details)

    def get_institution_by_name(self, institution_name: str) -> Institution:
        institution = self.repository.get_institution_by_name(institution_name)
        return institution
