from dataclasses import dataclass
from typing import Any


@dataclass()
class NewInstitutionDetails:
    institution_name: str
    department: str
    address: str
    url: str


Institution = Any
