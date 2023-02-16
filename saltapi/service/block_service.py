from typing import Any, Dict, Optional

import requests
from defusedxml import minidom

from saltapi.exceptions import AuthorizationError, ValidationError
from saltapi.repository.block_repository import BlockRepository
from saltapi.service.block import Block, BlockVisit
from saltapi.settings import get_settings


class BlockService:
    def __init__(self, block_repository: BlockRepository):
        self.block_repository = block_repository

    def get_block(self, block_id: int) -> Block:
        """
        Return the block content for a block id.
        """

        return self.block_repository.get(block_id)

    def get_block_status(self, block_id: int) -> Dict[str, Any]:
        """
        Return the block status for a block id.
        """

        return self.block_repository.get_block_status(block_id)

    def update_block_status(self, block_id: int, status: str, reason: str) -> None:
        """
        Set the block status for a block id.
        """

        allowed_status_list = ["Active", "On hold"]
        if status not in allowed_status_list:
            raise AuthorizationError()
        return self.block_repository.update_block_status(block_id, status, reason)

    def get_block_visit(self, block_visit_id: int) -> BlockVisit:
        """
        Return the block visit for a block visit id.
        """

        return self.block_repository.get_block_visit(block_visit_id)

    def update_block_visit_status(
        self,
        block_visit_id: int,
        status: str,
        reason: Optional[str],
    ) -> None:
        """
        Set the block visit status for a block visit id.
        """
        if status == "Rejected" and reason is None:
            raise ValidationError(
                'A reason is required for the block status value "Rejected"`.'
            )
        if status != "Rejected" and reason is not None:
            raise ValidationError(
                'No reason must be given for a block status other than "Rejected".'
            )
        return self.block_repository.update_block_visit_status(
            block_visit_id, status, reason
        )

    def get_next_scheduled_block(self) -> Block:
        """
        Get next scheduled block.
        """
        return self.block_repository.get_next_scheduled_block()

    def get_current_block(self) -> Optional[Block]:
        """
        Return the currently observed block.

        None is returned if there is no currently observed block.
        """
        file = requests.get(get_settings().tcs_icd_url)
        xml_file = minidom.parseString(file.text)
        elements = xml_file.getElementsByTagName("String")
        block_id = None
        for els in elements:
            # This will give a NodeList item
            name = els.getElementsByTagName("Name")
            # Which needs to be converted to a DOM Element by calling item(0)
            if name.item(0).firstChild.data == "block id":
                value = els.getElementsByTagName("Val")
                try:
                    block_id = value.item(0).firstChild.data
                except AttributeError:
                    pass  # block has no block ID
        if not block_id:
            return None
        return self.block_repository.get(block_id)
