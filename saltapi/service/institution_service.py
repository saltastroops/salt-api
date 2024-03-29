from typing import Any, Dict, List

from saltapi.repository.institution_repository import InstitutionRepository
from saltapi.service.institution import Institution


class InstitutionService:
    def __init__(self, repository: InstitutionRepository):
        self.repository = repository

    def get_institutions(self) -> List[Dict[str, Any]]:
        institutions = self.repository.get_institutions()
        return institutions

    def create(self, new_institution_details: Dict[str, Any]) -> None:
        self.repository.create(new_institution_details)

    def get_institution_by_name_and_department(
        self, institution_name: str, department: str
    ) -> Institution:
        institution = self.repository.get_institution_by_name_and_department(
            institution_name, department
        )
        return institution
