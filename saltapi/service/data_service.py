from typing import List

from saltapi.repository.data_repository import DataRepository
from saltapi.repository.proposal_repository import ProposalRepository
from saltapi.repository.user_repository import UserRepository


class DataService:
    def __init__(
        self,
        data_repository: DataRepository,
        proposal_repository: ProposalRepository,
        user_repository: UserRepository,
    ):
        self.data_repository = data_repository
        self.proposal_repository = proposal_repository
        self.user_repository = user_repository

    def request_data(
        self,
        user_id: int,
        proposal_code: str,
        block_visit_ids: List[int],
        data_formats: List[str],
    ) -> None:
        """
        Create an observation data request.
        """

        # In case of gravitational wave event proposals the user should be the
        # gravitational wave event user.
        proposal_type = self.proposal_repository.get_proposal_type(proposal_code)
        if proposal_type == "Gravitational Wave Event":
            gw_user = self.user_repository.get_by_username("gw")
            user_id = gw_user.id

        self.data_repository.request_data(
            user_id=user_id,
            proposal_code=proposal_code,
            block_visit_ids=block_visit_ids,
            data_formats=data_formats,
        )
