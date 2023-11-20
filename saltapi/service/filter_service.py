from typing import List

from saltapi.repository.filter_repository import FilterRepository


class FilterService:
    def __init__(self, filter_repository: FilterRepository):
        self.filter_repository = filter_repository

    def get_filters_details(self, semesters: List[str]):
        return self.filter_repository.get_filters_details(semesters)
