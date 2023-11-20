from typing import List, Set

from sqlalchemy import text
from sqlalchemy.engine import Connection
from sqlalchemy.exc import NoResultFound

from saltapi.exceptions import NotFoundError


class FilterRepository:
    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def get_filters_in_magazine(self):
        """
        Get all the filters that are in the magazine.
        """
        stmt = text("""
SELECT Barcode 
FROM RssCurrentFilters RCF 
    JOIN RssFilter RF ON RF.RssFilter_Id=RCF.RssFilter_Id
        """)
        try:
            result = self.connection.execute(stmt)
            return list(result.scalars())

        except NoResultFound:
            raise NotFoundError(f"Failed to fetch filter that are currently on the magazine")

    def get_filters_in_use(self, semesters: List[str]):
        """
        Get all the RSS filters that are in use.
        """
        stmt = text("""
SELECT DISTINCT RF.Barcode
FROM RssFilter RF
    JOIN RssConfig RC ON RF.RssFilter_Id = RC.RssFilter_Id
    JOIN Rss R ON RC.RssConfig_Id = R.RssConfig_Id
    JOIN RssPatternDetail RPD ON R.Rss_Id = RPD.Rss_Id
    JOIN RssPattern RP ON RPD.RssPattern_Id = RP.RssPattern_Id
    JOIN ObsConfig OC ON RP.RssPattern_Id = OC.RssPattern_Id
    JOIN TelescopeConfigObsConfig TCOC ON OC.ObsConfig_Id = TCOC.PlannedObsConfig_Id
    JOIN Pointing P ON TCOC.Pointing_Id = P.Pointing_Id
    JOIN Block B ON P.Block_Id = B.Block_Id
    JOIN BlockStatus BS ON B.BlockStatus_Id = BS.BlockStatus_Id
    JOIN Proposal Pr ON B.Proposal_Id = Pr.Proposal_Id
    JOIN Semester S ON Pr.Semester_Id = S.Semester_Id
WHERE CONCAT(S.`Year`, '-', S.Semester) IN :semesters
    AND (BlockStatus = 'Active' OR BlockStatus = 'On Hold')
    AND NVisits >= NDone;
        """)
        try:
            result = self.connection.execute(stmt, {"semesters": tuple(semesters)})
            return list(result.scalars())

        except NoResultFound:
            raise NotFoundError(f"Failed to fetch filters that are in use.")

    def _filter_proposals(self, semesters: List[str], relevant_filters: Set[str]):
        stmt = text("""
SELECT DISTINCT
    RF.Barcode AS barcode, 
    NVisits <= NDone as done,
    B.Block_Id AS block_id,
    PC.Proposal_Code AS proposal_code
FROM RssFilter RF
    JOIN RssConfig RC ON RF.RssFilter_Id = RC.RssFilter_Id
    JOIN Rss R ON RC.RssConfig_Id = R.RssConfig_Id
    JOIN RssPatternDetail RPD ON R.Rss_Id = RPD.Rss_Id
    JOIN RssPattern RP ON RPD.RssPattern_Id = RP.RssPattern_Id
    JOIN ObsConfig OC ON RP.RssPattern_Id = OC.RssPattern_Id
    JOIN TelescopeConfigObsConfig TCOC ON OC.ObsConfig_Id = TCOC.PlannedObsConfig_Id
    JOIN Pointing P ON TCOC.Pointing_Id = P.Pointing_Id
    JOIN Block B ON P.Block_Id = B.Block_Id
    JOIN BlockStatus BS ON B.BlockStatus_Id = BS.BlockStatus_Id
    JOIN Proposal Pr ON B.Proposal_Id = Pr.Proposal_Id
    JOIN ProposalCode PC ON PC.ProposalCode_Id = Pr.ProposalCode_Id
    JOIN Semester S ON Pr.Semester_Id = S.Semester_Id
WHERE CONCAT(S.`Year`, '-', S.Semester) IN :semesters
    AND RF.Barcode IN :relevant_filters
    AND (BlockStatus = 'Active' OR BlockStatus = 'On Hold')
        """)

        try:
            results = self.connection.execute(stmt, {"semesters": tuple(semesters), "relevant_filters": tuple(relevant_filters)})
            return [
                {
                    "barcode": row.barcode,
                    "block": {
                        "is_done": row.done,
                        "block_id": row.block_id
                    },
                    "proposal_code": row.proposal_code
                } for row in results
            ]

        except NoResultFound:
            raise NotFoundError(f"Failed to fetch filters that are in use.")

    def _filter_in_magazine_keys(self):
        return {_filter: {"barcode": _filter, "blocks": 0, "proposals": set(), "is_needed": False, "in_magazine": True}
                for _filter in self.get_filters_in_magazine()}

    def _filter_in_use_keys(self, semesters: List[str]):
        filter_in_magazine = self._filter_in_magazine_keys()
        return {
            _filter: {
                "barcode": _filter,
                "blocks": 0,
                "proposals": set(),
                "is_needed": False,
                "in_magazine": _filter in filter_in_magazine
            } for _filter in self.get_filters_in_use(semesters)}

    def get_filters_details(self, semesters: List[str]):
        filters_of_interest = {**self._filter_in_magazine_keys(), **self._filter_in_use_keys(semesters)}

        relevant_filters = set(filters_of_interest.keys())

        blocks = self._filter_proposals(semesters, relevant_filters)

        for block in blocks:
            barcode = block["barcode"]
            proposal_code = block["proposal_code"]
            _block = block["block"]
            filters_of_interest[barcode]["proposals"].add(proposal_code)
            filters_of_interest[barcode]["blocks"] += 1

            if not block["block"]["is_done"]:
                filters_of_interest[barcode]["is_needed"] = True

        return list(filters_of_interest.values())





