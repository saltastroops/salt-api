from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Literal, Optional, cast, get_args

import pytz
from astropy.coordinates import Angle
from sqlalchemy import text
from sqlalchemy.engine import Connection
from sqlalchemy.exc import IntegrityError, NoResultFound

from saltapi.exceptions import NotFoundError
from saltapi.repository.instrument_repository import InstrumentRepository
from saltapi.repository.target_repository import TargetRepository
from saltapi.service.block import Block
from saltapi.settings import get_settings
from saltapi.web.schema.block import BlockStatusValue
from saltapi.web.schema.common import BlockRejectionReason


TECH_PROBLEMS = {
    BlockRejectionReason.INSTRUMENT_TECHNICAL_PROBLEMS,
    BlockRejectionReason.TELESCOPE_TECHNICAL_PROBLEMS,
}


class BlockRepository:
    def __init__(
        self,
        connection: Connection,
    ) -> None:
        self.target_repository = TargetRepository(connection)
        self.instrument_repository = InstrumentRepository(connection)
        self.connection = connection

    def get(self, block_id: int) -> Block:
        """
        Return the block content for a block id.
        """

        # Avoid blocks with subblocks or subsubblocks.
        if self._has_subblock_or_subsubblock_iterations(block_id):
            error = (
                "Blocks which have subblock or subsubblock iterations are not supported"
            )
            raise ValueError(error)

        stmt = text(
            """
SELECT B.Block_Id                      AS block_id,
       BC.BlockCode                    AS code,
       B.Block_Name                    AS name,
       PC.Proposal_Code                AS proposal_code,
       P.SubmissionDate                AS submission_date,
       CONCAT(S.Year, '-', S.Semester) AS semester,
       BS.BlockStatus                  AS status,
       B.Priority                      AS priority,
       PR.Ranking                      AS ranking,
       B.WaitDays                      AS wait_period,
       B.NVisits                       AS requested_observations,
       B.NDone                         AS accepted_observations,
       B.NAttempted                    AS rejected_observations,
       B.Comments                      AS comment,
       B.MinSeeing                     AS minimum_seeing,
       B.MaxSeeing                     AS maximum_seeing,
       T.Transparency                  AS transparency,
       B.MaxLunarPhase                 AS maximum_lunar_phase,
       B.MinLunarAngularDistance       AS minimum_lunar_distance,
       B.ObsTime                       AS observation_time,
       B.OverheadTime                  AS overhead_time,
       BP.MoonProbability              AS moon_probability,
       BP.CompetitionProbability       AS competition_probability,
       BP.ObservabilityProbability     AS observability_probability,
       BP.SeeingProbability            AS seeing_probability,
       BP.AveRanking                   AS average_ranking,
       BP.TotalProbability             AS total_probability,
       B.BlockStatusReason             AS reason,
       P.SubmissionDate                AS latest_submission_date
FROM Block B
         JOIN BlockStatus BS ON B.BlockStatus_Id = BS.BlockStatus_Id
         LEFT JOIN PiRanking PR ON B.PiRanking_Id = PR.PiRanking_Id
         JOIN Transparency T ON B.Transparency_Id = T.Transparency_Id
         JOIN Proposal P ON B.Proposal_Id = P.Proposal_Id
         JOIN ProposalCode PC ON P.ProposalCode_Id = PC.ProposalCode_Id
         JOIN Semester S ON P.Semester_Id = S.Semester_Id
         LEFT JOIN BlockProbabilities BP ON B.Block_Id = BP.Block_Id
         LEFT JOIN BlockCode BC ON B.BlockCode_Id = BC.BlockCode_Id
WHERE B.Block_Id = :block_id;
        """
        )
        result = self.connection.execute(stmt, {"block_id": block_id})

        row = result.one()

        observing_conditions = {
            "minimum_seeing": row.minimum_seeing,
            "maximum_seeing": row.maximum_seeing,
            "transparency": row.transparency,
            "minimum_lunar_distance": float(row.minimum_lunar_distance),
            "maximum_lunar_phase": float(row.maximum_lunar_phase),
        }
        observation_probabilities = {
            "moon": row.moon_probability,
            "competition": row.competition_probability,
            "observability": None
            if row.observability_probability is None
            else 0
            if row.observability_probability < 0
            else row.observability_probability,
            "seeing": row.seeing_probability,
            "average_ranking": row.average_ranking,
            "total": row.total_probability,
        }

        block = {
            "id": row.block_id,
            "code": row.code,
            "name": row.name,
            "proposal_code": row.proposal_code,
            "submission_date": pytz.utc.localize(row.submission_date),
            "semester": row.semester,
            "status": {
                "value": row.status if row.status != "On Hold" else "On hold",
                "reason": row.reason,
            },
            "priority": row.priority,
            "ranking": row.ranking,
            "wait_period": row.wait_period,
            "requested_observations": row.requested_observations,
            "accepted_observations": row.accepted_observations,
            "rejected_observations": row.rejected_observations,
            "comment": row.comment,
            "observing_conditions": observing_conditions,
            "observation_time": row.observation_time,
            "overhead_time": row.overhead_time,
            "observation_probabilities": observation_probabilities,
            "observing_windows": self._observing_windows(block_id),
            "block_visits": self._block_visits(block_id),
            "observations": self._pointings(block_id),
            "latest_submission_date": pytz.utc.localize(row.latest_submission_date),
        }

        return block

    def get_block_status(self, block_id: int) -> Dict[str, Any]:
        """
        Return the block status for a block id.
        """
        stmt = text(
            """
SELECT BS.BlockStatus AS value, B.BlockStatusReason AS reason
FROM BlockStatus BS
         JOIN Block B ON BS.BlockStatus_Id = B.BlockStatus_Id
WHERE B.Block_Id = :block_id
        """
        )

        result = self.connection.execute(stmt, {"block_id": block_id})

        row = result.one()

        value = row.value
        if value == "On Hold":
            value = "On hold"
        status = {"value": value, "reason": row.reason}

        return status

    def update_block_status(
        self, block_id: int, value: str, reason: Optional[str]
    ) -> None:
        """
        Update the status of a block.
        """
        if value == "On hold":
            value = "On Hold"
        stmt = text(
            """
UPDATE Block B
SET B.BlockStatus_Id = (SELECT BS.BlockStatus_Id
                        FROM BlockStatus BS
                        WHERE BS.BlockStatus = :status),
    B.BlockStatusReason = :reason
WHERE B.Block_Id = :block_id;
    """
        )
        try:
            result = self.connection.execute(
                stmt, {"block_id": block_id, "status": value, "reason": reason}
            )
        except IntegrityError:
            raise ValueError("Unknown block status")
        if not result.rowcount:
            raise NotFoundError("Unknown block id")

    def get_proposal_code_for_block_id(self, block_id: int) -> str:
        """
        Return proposal code for a block id:
        """
        stmt = text(
            """
SELECT PC.Proposal_code
FROM ProposalCode PC
         JOIN Block B ON PC.ProposalCode_Id = B.ProposalCode_Id
WHERE B.Block_Id = :block_id;
    """
        )
        result = self.connection.execute(
            stmt,
            {"block_id": block_id},
        )

        try:
            return str(result.scalar_one())
        except NoResultFound:
            raise NotFoundError()

    def get_block_visit(self, block_visit_id: int) -> Dict[str, str]:
        """
        Return the block visits for a block visit id.
        """
        stmt = text(
            """
SELECT BV.BlockVisit_Id     AS id,
       NI.Date              AS night,
       BVS.BlockVisitStatus AS status,
       BRR.RejectedReason   AS rejection_reason
FROM BlockVisit BV
    LEFT JOIN BlockRejectedReason BRR
                   ON BV.BlockRejectedReason_Id = BRR.BlockRejectedReason_Id
    JOIN NightInfo NI ON BV.NightInfo_Id = NI.NightInfo_Id
    JOIN BlockVisitStatus BVS ON BV.BlockVisitStatus_Id = BVS.BlockVisitStatus_Id
WHERE BV.BlockVisit_Id = :block_visit_id
  AND BVS.BlockVisitStatus NOT IN ('Deleted');
        """
        )
        try:
            result = self.connection.execute(stmt, {"block_visit_id": block_visit_id})
            row = result.one()
            block_visit = {
                "id": row.id,
                "night": row.night,
                "status": row.status,
                "rejection_reason": row.rejection_reason,
            }
            return block_visit
        except NoResultFound:
            raise NotFoundError("Unknown block visit id")

    def get_observation_time(self, block_visit_id: int) -> float:
        """
        Retrieve the scheduled observation time for a given block visit.

        Parameters
        ----------
        block_visit_id : int
           The unique identifier of the block visit.

        Returns
        -------
        float
           Observation time in seconds (or database time unit).

        Raises
        ------
        NotFoundError
           If no block visit is found for the given ID.
        """

        stmt  = text("""
SELECT B.ObsTime  AS obs_time 
FROM Block B 
    JOIN BlockVisit BV ON B.Block_Id=BV.Block_Id 
WHERE BlockVisit_Id=:block_visit_id
                     """)
        try:
            return self.connection.execute(stmt, {"block_visit_id": block_visit_id}).scalar_one()
        except NoResultFound:
            raise NotFoundError(f"No observation time for block_visit_id: {block_visit_id}")

    def get_night_info_id_for_block_visit(self, block_visit_id: int) -> int:
        """
        Retrieve the NightInfo ID associated with a block visit.

        Parameters
        ----------
        block_visit_id : int
            The block visit identifier.

        Returns
        -------
        int
            NightInfo primary key ID.

        Raises
        ------
        NotFoundError
            If the block visit does not exist.
        """

        stmt  = text("""
SELECT NightInfo_Id AS night_info_id FROM BlockVisit WHERE BlockVisit_Id=:block_visit_id      
        """)
        try:
            result = self.connection.execute(stmt, {"block_visit_id": block_visit_id})
            row = result.one()
            return row.night_info_id
        except NoResultFound:
            raise NotFoundError(f"No NightInfo for block_visit_id: {block_visit_id}")

    def get_night_info_times(self, night_info_id: int) -> dict[str, Any]:
        """
        Fetch time accounting values for a given night.

        Parameters
        ----------
        night_info_id : int
            NightInfo table primary key.

        Returns
        -------
        dict[str, float]
            Dictionary containing:
            - science_time
            - lost_time_to_weather
            - lost_time_to_problems

        Raises
        ------
        NotFoundError
            If NightInfo record does not exist.
        """

        stmt  = text("""
SELECT 
    ScienceTime         AS science_time, 
    TimeLostToWeather   AS lost_time_to_weather, 
    TimeLostToProblems  AS lost_time_to_problems
FROM NightInfo
WHERE NightInfo_Id=:night_info_id
                     """)
        try:
            result = self.connection.execute(stmt, {"night_info_id": night_info_id})
            row = result.one()
            return {
                "science_time": row.science_time,
                "lost_time_to_weather": row.lost_time_to_weather,
                "lost_time_to_problems": row.lost_time_to_problems,
            }
        except NoResultFound:
            raise NotFoundError(f"NightInfo not found: {night_info_id}")

    def update_used_times(self, block_visit_id: int, new_status: str, new_rejection_reason: str):
        """
        Update nightly time accounting when a block visit status changes.

        This adjusts:
        - ScienceTime
        - TimeLostToWeather
        - TimeLostToProblems

        Parameters
        ----------
        block_visit_id : int
            Block visit identifier.
        new_status : str
            New block visit status ("Accepted" or "Rejected").
        new_rejection_reason : str
            Rejection reason code (if rejected).

        Notes
        -----
        This method handles transitions between:
        - Accepted → Rejected
        - Rejected → Accepted
        - Rejected → Rejected (reason change)
        """
        block_visit = self.get_block_visit(block_visit_id)
        observation_time = self.get_observation_time(block_visit_id)
        night_info_id = self.get_night_info_id_for_block_visit(block_visit_id)
        current_times = self.get_night_info_times(night_info_id)

        science_time = current_times["science_time"]
        lost_time_to_weather = current_times["lost_time_to_weather"]
        lost_time_to_problems = current_times["lost_time_to_problems"]

        current_rejection_reason = block_visit["rejection_reason"]
        current_status = block_visit["status"]

        technical_problems = new_rejection_reason in TECH_PROBLEMS

        # Rejected → Rejected (change reason)
        if new_status == "Rejected" and current_status == "Rejected":
            if technical_problems and current_rejection_reason == BlockRejectionReason.OBSERVING_CONDITIONS_NOT_MET:
                lost_time_to_weather -= observation_time
                lost_time_to_problems += observation_time
            if (current_rejection_reason in TECH_PROBLEMS
                    and new_rejection_reason == BlockRejectionReason.OBSERVING_CONDITIONS_NOT_MET):
                lost_time_to_weather += observation_time
                lost_time_to_problems -= observation_time

        # Accepted → Rejected
        if new_status == "Rejected" and current_status == "Accepted":
            science_time -= observation_time
            if technical_problems:
                lost_time_to_problems += observation_time
            if current_rejection_reason == BlockRejectionReason.OBSERVING_CONDITIONS_NOT_MET:
                lost_time_to_weather += observation_time

        # Rejected → Accepted
        if new_status == "Accepted" and current_status == "Rejected":
            science_time += observation_time
            if technical_problems:
                lost_time_to_problems -= observation_time
            if current_rejection_reason == BlockRejectionReason.OBSERVING_CONDITIONS_NOT_MET:
                lost_time_to_weather -= observation_time

        stmt = text("""
UPDATE NightInfo 
SET 
    ScienceTime=:science_time, 
    TimeLostToWeather=:lost_time_to_weather, 
    TimeLostToProblems=:lost_time_to_problems
WHERE NightInfo_Id=:night_info_id       
        """)
        self.connection.execute(
            stmt, {
                "night_info_id": night_info_id,
                "science_time": science_time,
                "lost_time_to_weather": lost_time_to_weather,
                "lost_time_to_problems": lost_time_to_problems
            }
        )

    def update_block_attempts_and_status(self, block_visit_id: int, status: str):
        """
         Update block-level attempt counters and block completion status.

        This function updates the latest Block record for the same semester and
        block code as the given block visit. It adjusts:

        - NDone       : Number of successful visits
        - NAttempted  : Number of attempted visits
        - BlockStatus : ACTIVE or COMPLETED

        The logic depends on the transition of the block visit status:

        - Accepted → Rejected: decrement NDone, increment NAttempted
        - Rejected → Accepted: increment NDone, decrement NAttempted
        - Rejected → Rejected: no change

        If all required visits are completed (NDone == NVisits), the block is marked
        as COMPLETED. If a completed block is later rejected, it is set back to ACTIVE.

        Parameters
        ----------
        block_visit_id : int
            The BlockVisit identifier used to locate the latest Block instance.
        status : str
            New block visit status ("Accepted" or "Rejected").

        Notes
        -----
        This function does NOT update BlockVisit records. It only updates Block-level
        accounting fields and block lifecycle status.
        """

        # Get latest block for the same semester + block code
        stmt_get = text("""
SELECT
    B.Block_Id AS block_id,
    B.NDone AS n_done,
    B.NVisits AS n_visits,
    B.NAttempted AS n_attempted,
    BS.BlockStatus AS block_status
FROM Block AS B
         JOIN Proposal AS P ON B.Proposal_Id = P.Proposal_Id
    JOIN BlockStatus AS BS ON BS.BlockStatus_Id = B.BlockStatus_Id
WHERE P.Semester_Id = (
    SELECT P1.Semester_Id
    FROM Proposal AS P1
             JOIN Block AS B1 ON P1.Proposal_Id = B1.Proposal_Id
             JOIN BlockVisit AS BV1 ON B1.Block_Id = BV1.Block_Id
    WHERE BV1.BlockVisit_Id = :block_visit_id
)
  AND B.BlockCode_Id = (
    SELECT B2.BlockCode_Id
    FROM Block AS B2
             JOIN BlockVisit AS BV2 USING (Block_Id)
    WHERE BV2.BlockVisit_Id = :block_visit_id
)
ORDER BY B.Block_Id DESC 
    LIMIT 1
        """)
        result = self.connection.execute(stmt_get, {"block_visit_id": block_visit_id})
        row = result.one()
        latest_block_id = row["block_id"]
        n_done = row.n_done
        n_attempted = row.n_attempted
        current_visit = self.get_block_visit(block_visit_id)

        # Update counters
        if current_visit["status"] == "Rejected" and status == "Rejected":
            pass
        else:
            if status == "Rejected":
                n_done -= 1
                n_attempted += 1
            else:
                n_done += 1
                n_attempted -= 1

        # Update block status
        block_status = row["block_status"]

        if block_status == BlockStatusValue.COMPLETED and status == "Rejected":
            block_status = BlockStatusValue.ACTIVE
        if status == "Accepted" and n_done == row["n_visits"]:
            block_status = BlockStatusValue.COMPLETED

        # Update SDB table Block
        stmt_update = text("""
UPDATE Block B
SET B.NDone = :n_done, 
    B.NAttempted = :n_attempted,
    B.BlockStatus_Id = (SELECT BS.BlockStatus_Id
                        FROM BlockStatus BS
                        WHERE BS.BlockStatus = :status)
WHERE B.Block_Id = :block_id 
        """)
        self.connection.execute(
            stmt_update, {
                "n_done": n_done,
                "n_attempted": n_attempted,
                "status": block_status,
                "block_id": latest_block_id
            }
        )

    def update_block_visit_status(
        self, block_visit_id: int, status: str, rejection_reason: Optional[str]
    ) -> None:
        """
         Update the status and rejection reason of a BlockVisit.

        This method performs three operations:

        1. Updates nightly time accounting (science time, weather loss, technical loss).
        2. Updates block-level counters and block status via
           `update_block_attempts_and_status`.
        3. Updates the BlockVisit status and rejection reason in the database.

        Parameters
        ----------
        block_visit_id : int
            Unique identifier of the block visit.
        status : str
            New visit status (e.g. "Accepted", "Rejected").
        rejection_reason : Optional[str]
            Reason for rejection, if the status is "Rejected".

        Raises
        ------
        NotFoundError
            If the block visit does not exist.
        ValueError
            If the status or rejection reason is invalid.

        Notes
        -----
        This function is the main entry point for changing a visit state.
        It coordinates visit-level, block-level, and night-level accounting updates.
        """

        if not self._block_visit_exists(block_visit_id):
            raise NotFoundError(f"Unknown block visit id: {block_visit_id}")
        try:
            block_visit_status_id = self._block_visit_status_id(status)
            block_rejected_reason_id = (
                self._block_rejection_reason_id(rejection_reason)
                if rejection_reason
                else None
            )
        except NoResultFound:
            raise ValueError(f"Unknown block visit status: {status}")

        # update used time for the night
        self.update_used_times(block_visit_id, status, rejection_reason)

        # update the visit attempts and block Status
        self.update_block_attempts_and_status(block_visit_id, status)
        stmt = text(
            """
UPDATE BlockVisit BV
SET BV.BlockVisitStatus_Id = :block_visit_status_id,
    BV.BlockRejectedReason_Id = :block_rejected_reason_id
WHERE BV.BlockVisit_Id = :block_visit_id
AND BV.BlockVisitStatus_Id NOT IN (SELECT BVS2.BlockVisitStatus_Id
                                    FROM BlockVisitStatus AS BVS2
                                    WHERE BVS2.BlockVisitStatus = 'Deleted');
        """
        )
        self.connection.execute(
            stmt,
            {
                "block_visit_id": block_visit_id,
                "block_visit_status_id": block_visit_status_id,
                "block_rejected_reason_id": block_rejected_reason_id,
            },
        )

    def _block_visit_status_id(self, status: str) -> int:
        stmt = text(
            """
SELECT BVS.BlockVisitStatus_Id AS id
FROM BlockVisitStatus BVS
WHERE BVS.BlockVisitStatus = :status
        """
        )
        result = self.connection.execute(stmt, {"status": status})
        return cast(int, result.scalar_one())

    def _block_rejection_reason_id(self, rejection_reason: str) -> int:
        stmt = text(
            """
SELECT BRR.BlockRejectedReason_Id AS id
FROM BlockRejectedReason BRR
WHERE BRR.RejectedReason = :rejected_reason
        """
        )
        result = self.connection.execute(stmt, {"rejected_reason": rejection_reason})
        return cast(int, result.scalar_one())

    def _block_visit_exists(self, block_visit_id: int) -> bool:
        stmt = text(
            """
SELECT COUNT(*) FROM BlockVisit WHERE BlockVisit_Id = :block_visit_id
        """
        )
        result = self.connection.execute(stmt, {"block_visit_id": block_visit_id})

        return cast(int, result.scalar_one()) > 0

    def get_proposal_code_for_block_visit_id(self, block_visit_id: int) -> str:
        """
        Return proposal code for a block visit id:
        """
        stmt = text(
            """
SELECT PC.Proposal_code
FROM ProposalCode PC
         JOIN Block B ON PC.ProposalCode_Id = B.ProposalCode_Id
         JOIN BlockVisit BV ON BV.Block_Id = B.Block_Id
         JOIN BlockVisitStatus BVS ON BV.BlockVisitStatus_Id = BVS.BlockVisitStatus_Id
WHERE BV.BlockVisit_Id = :block_visit_id
  AND BVS.BlockVisitStatus NOT IN ('Deleted');
        """
        )
        result = self.connection.execute(
            stmt,
            {"block_visit_id": block_visit_id},
        )

        try:
            return cast(str, result.scalar_one())
        except NoResultFound:
            raise NotFoundError()

    def _block_visits(self, block_id: int) -> List[Dict[str, Any]]:
        """
        Return the executed observations.
        """
        stmt = text(
            """
SELECT BV.BlockVisit_Id     AS id,
       NI.Date              AS night,
       BVS.BlockVisitStatus AS status,
       BRR.RejectedReason   AS rejection_reason
FROM BlockVisit BV
         JOIN BlockVisitStatus BVS ON BV.BlockVisitStatus_Id = BVS.BlockVisitStatus_Id
         LEFT JOIN BlockRejectedReason BRR
                   ON BV.BlockRejectedReason_Id = BRR.BlockRejectedReason_Id
         JOIN NightInfo NI ON BV.NightInfo_Id = NI.NightInfo_Id
         JOIN Block B ON BV.Block_Id IN (
    SELECT B1.Block_Id
    FROM Block B1
    WHERE B1.BlockCode_Id = B.BlockCode_Id
)
WHERE B.Block_Id = :block_id
  AND BVS.BlockVisitStatus IN ('Accepted', 'Rejected');
        """
        )
        result = self.connection.execute(stmt, {"block_id": block_id})
        block_visits = [
            {
                "id": row.id,
                "night": row.night,
                "status": row.status,
                "rejection_reason": row.rejection_reason,
            }
            for row in result
        ]

        return block_visits

    def _observing_windows(self, block_id: int) -> List[Dict[str, datetime]]:
        """
        Return the observing windows.
        """
        stmt = text(
            """
SELECT BVW.VisibilityStart AS start, BVW.VisibilityEnd AS end
FROM BlockVisibilityWindow BVW
WHERE BVW.Block_Id = :block_id
ORDER BY BVW.VisibilityStart;
        """
        )
        result = self.connection.execute(stmt, {"block_id": block_id})
        return [
            {"start": pytz.utc.localize(row.start), "end": pytz.utc.localize(row.end)}
            for row in result
        ]

    def _finder_charts(self, block_id: int, pointing_id: int) -> List[Dict[str, Any]]:
        stmt = text(
            """
SELECT FC.FindingChart_Id AS finding_chart_id,
       FC.Comments        AS comments,
       FC.ValidFrom       AS valid_from,
       FC.ValidUntil      AS valid_until,
       FC.Path            AS path
FROM FindingChart FC
WHERE FC.Pointing_Id = :pointing_id
ORDER BY ValidFrom, FindingChart_Id
        """
        )
        result = self.connection.execute(stmt, {"pointing_id": pointing_id})

        finder_charts = [
            {
                "id": row.finding_chart_id,
                "comment": row.comments,
                "valid_from": pytz.utc.localize(row.valid_from)
                if row.valid_from
                else None,
                "valid_until": pytz.utc.localize(row.valid_until)
                if row.valid_until
                else None,
                "path": row.path,
            }
            for row in result
        ]

        # Get the finder chart file sizes and URLs
        proposal_code = self.get_proposal_code_for_block_id(block_id)
        SizeType = Literal["original", "thumbnail"]
        for fc in finder_charts:
            files = []
            for size in get_args(SizeType):
                files.extend(
                    [
                        {
                            "size": size,
                            "url": url,
                        }
                        for url in self._finder_chart_urls(
                            finder_chart_id=fc["id"],
                            path_from_db=fc["path"],
                            proposal_code=proposal_code,
                            size=size,
                        )
                    ]
                )
            fc["files"] = files
            del fc["path"]

        return finder_charts

    def _finder_chart_urls(
        self,
        finder_chart_id: int,
        path_from_db: str,
        proposal_code: str,
        size: Literal["original", "thumbnail"],
    ) -> List[str]:
        included_dir = get_settings().proposals_dir / proposal_code / Path(path_from_db).parent
        prefix = ""
        size_identifier = ""
        if size == "original":
            pass
        elif size == "thumbnail":
            prefix = "Thumbnail"
            size_identifier = "-thumbnail"
        else:
            raise ValueError(f"Unsupported finder chart size: {size}")

        # Collect all the finder chart files with the correct size
        name = Path(path_from_db).stem
        files = list(included_dir.glob(f"{prefix}{name}.*"))

        # Return the URLs for the files
        return [
            f"/finder-charts/{finder_chart_id}{size_identifier}{suffix}"
            for suffix in (".jpg", ".pdf", ".png")
            if any(file.suffix.lower() == suffix for file in files)
        ]

    def _time_restrictions(
        self, pointing_id: int
    ) -> Optional[List[Dict[str, datetime]]]:
        """
        Return the time restrictions.
        """
        stmt = text(
            """
SELECT DISTINCT TR.ObsWindowStart AS start, TR.ObsWindowEnd AS end
FROM TimeRestricted TR
         JOIN Pointing P ON TR.Pointing_Id = P.Pointing_Id
WHERE P.Pointing_Id = :pointing_id
ORDER BY TR.ObsWindowStart;
        """
        )
        result = self.connection.execute(stmt, {"pointing_id": pointing_id})
        restrictions = [
            {"start": pytz.utc.localize(row.start), "end": pytz.utc.localize(row.end)}
            for row in result
        ]

        return restrictions if len(restrictions) else None

    def _phase_constraints(self, pointing_id: int) -> Optional[List[Dict[str, float]]]:
        """
        Return the phase constraints.
        """
        stmt = text(
            """
SELECT PC.PhaseStart AS start, PC.PhaseEnd AS end
FROM PhaseConstraint PC
WHERE PC.Pointing_Id = :pointing_id
ORDER BY PC.PhaseStart;
        """
        )
        result = self.connection.execute(stmt, {"pointing_id": pointing_id})
        constraints = [dict(row) for row in result]

        return constraints if len(constraints) else None

    def _pointings(self, block_id: int) -> List[Dict[str, Any]]:
        """
        Return the pointings.
        """
        stmt = text(
            """
SELECT P.Pointing_Id                                                  AS pointing_id,
       P.ObsTime                                                      AS observation_time,
       P.OverheadTime                                                 AS overhead_time,
       TCOC.Observation_Order                                         AS observation_order,
       TCOC.TelescopeConfig_Order                                     AS telescope_config_order,
       TCOC.PlannedObsConfig_Order                                    AS planned_obsconfig_order,
       O.Target_Id                                                    AS target_id,
       TC.PositionAngle                                               AS position_angle,
       TC.FixedAngle                                                  AS fixed_angle,
       TC.UseParallacticAngle                                         AS use_parallactic_angle,
       TC.Iterations                                                  AS tc_iterations,
       DP.DitherPatternDescription                                    AS dp_description,
       DP.NHorizontalTiles                                            AS dp_horizontal_tiles,
       DP.NVerticalTiles                                              AS dp_vertical_tiles,
       DP.Offsetsize                                                  AS dp_offset_size,
       DP.NSteps                                                      AS dp_steps,
       CONCAT(GS.RaH, ':', GS.RaM, ':', GS.RaS / 1000)                AS gs_ra,
       CONCAT(GS.DecSign, GS.DecD, ':', GS.DecM, ':', GS.DecS / 1000) AS gs_dec,
       GS.Equinox                                                     AS gs_equinox,
       GS.Mag                                                         AS gs_magnitude,
       L.Lamp                                                         AS pc_lamp,
       CF.CalFilter                                                   AS pc_calibration_filter,
       GM.GuideMethod                                                 AS pc_guide_method,
       PCT.Type                                                       AS pc_type,
       PC.CalScreenIn                                                 AS pc_calibration_screen_in,
       OC.SalticamPattern_Id                                          AS salticam_pattern_id,
       OC.RssPattern_Id                                               AS rss_pattern_id,
       OC.HrsPattern_Id                                               AS hrs_pattern_id,
       OC.BvitPattern_Id                                              AS bvit_pattern_id,
       OC.NirPattern_Id                                               AS nir_pattern_id
FROM TelescopeConfigObsConfig TCOC
         JOIN Pointing P ON TCOC.Pointing_Id = P.Pointing_Id
         JOIN Block B ON P.Block_Id = B.Block_Id
         JOIN TelescopeConfig TC ON TCOC.Pointing_Id = TC.Pointing_Id AND
                                    TCOC.Observation_Order = TC.Observation_Order AND
                                    TCOC.TelescopeConfig_Order =
                                    TC.TelescopeConfig_Order
         LEFT JOIN DitherPattern DP ON TC.DitherPattern_Id = DP.DitherPattern_Id
         LEFT JOIN GuideStar GS ON TC.GuideStar_Id = GS.GuideStar_Id
         JOIN Observation O ON TCOC.Pointing_Id = O.Pointing_Id AND
                               TCOC.Observation_Order = O.Observation_Order
         JOIN Target T ON O.Target_Id = T.Target_Id
         JOIN ObsConfig OC ON TCOC.PlannedObsConfig_Id = OC.ObsConfig_Id
         JOIN PayloadConfig PC ON OC.PayloadConfig_Id = PC.PayloadConfig_Id
         LEFT JOIN Lamp L ON PC.Lamp_Id = L.Lamp_Id
         LEFT JOIN CalFilter CF ON PC.CalFilter_Id = CF.CalFilter_Id
         LEFT JOIN GuideMethod GM ON PC.GuideMethod_Id = GM.GuideMethod_Id
         LEFT JOIN PayloadConfigType PCT
                   ON PC.PayloadConfigType_Id = PCT.PayloadConfigType_Id
WHERE B.Block_Id = :block_id
ORDER BY TCOC.Pointing_Id, TCOC.Observation_Order, TCOC.TelescopeConfig_Order,
         TCOC.PlannedObsConfig_Order;
        """
        )
        result = self.connection.execute(stmt, {"block_id": block_id})

        # collect the pointings
        pointing_groups = self._group_by_pointing_id(result)

        # avoid pointings with multiple observations
        for pointing_rows in pointing_groups:
            if self._has_multiple_observations(pointing_rows[0].pointing_id):
                error = (
                    "Blocks containing a pointing with multiple observations are "
                    "not supported."
                )
                raise ValueError(error)

        # create the pointings
        pointings: List[Dict[str, Any]] = []
        for pointing_rows in pointing_groups:
            pointing = {
                "target": self.target_repository.get(pointing_rows[0].target_id),
                "finder_charts": self._finder_charts(
                    block_id, pointing_rows[0].pointing_id
                ),
                "time_restrictions": self._time_restrictions(
                    pointing_rows[0].pointing_id
                ),
                "phase_constraints": self._phase_constraints(
                    pointing_rows[0].pointing_id
                ),
                "telescope_configurations": self._telescope_configurations(
                    pointing_rows
                ),
                "observation_time": pointing_rows[0].observation_time,
                "overhead_time": pointing_rows[0].overhead_time
                if pointing_rows[0].overhead_time
                else None,
            }
            pointings.append(pointing)

        return pointings

    def _group_by_pointing_id(self, rows: Iterable[Any]) -> List[List[Any]]:
        """
        Group rows obtained in the _pointings method by pointing order.
        """
        previous_pointing_id = None
        current_pointing_rows: List[Any] = []
        pointings = []
        for row in rows:
            if row.pointing_id != previous_pointing_id:
                current_pointing_rows = []
                pointings.append(current_pointing_rows)
            current_pointing_rows.append(row)
            previous_pointing_id = row.pointing_id

        return pointings

    def _dither_pattern(self, row: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Return the dither pattern.
        """
        if row["dp_horizontal_tiles"] is None:
            return None

        return {
            "horizontal_tiles": row["dp_horizontal_tiles"],
            "vertical_tiles": row["dp_vertical_tiles"],
            "offset_size": float(row["dp_offset_size"]),
            "steps": row["dp_steps"],
            "description": row["dp_description"],
        }

    def _guide_star(self, row: Any) -> Optional[Dict[str, Any]]:
        """
        Return the guide star.
        """

        ra = Angle(f"{row.gs_ra} hours").degree
        dec = Angle(f"{row.gs_dec} degrees").degree

        if ra == 0 and dec == 0:
            return None

        return {
            "right_ascension": float(ra),
            "declination": float(dec),
            "equinox": row.gs_equinox,
            "magnitude": row.gs_magnitude,
        }

    def _telescope_configurations(self, pointing_rows: List[Any]) -> List[Any]:
        """
        Get the list of telescope configurations for database rows belonging to a
        pointing.
        """
        # Group the rows by telescope config
        previous_telescope_config_order = None
        current_telescope_config_rows: List[Any] = []
        tc_groups = []
        for row in pointing_rows:
            if row.telescope_config_order != previous_telescope_config_order:
                current_telescope_config_rows = []
                tc_groups.append(current_telescope_config_rows)
            current_telescope_config_rows.append(row)

            previous_telescope_config_order = row.telescope_config_order

        # Create the telescope configurations
        telescope_configs = []
        for tc_group in tc_groups:
            row = tc_group[0]
            tc = {
                "iterations": row["tc_iterations"],
                "position_angle": row["position_angle"],
                "is_position_angle_fixed": row["fixed_angle"] or 0,
                "use_parallactic_angle": row["use_parallactic_angle"],
                "dither_pattern": self._dither_pattern(row),
                "guide_star": self._guide_star(row),
                "payload_configurations": [
                    self._payload_configuration(row) for row in tc_group
                ],
            }
            telescope_configs.append(tc)

        return telescope_configs

    def _payload_configuration(self, payload_config_row: Any) -> Dict[str, Any]:
        payload_config = {
            "payload_configuration_type": payload_config_row.pc_type,
            "use_calibration_screen": True
            if payload_config_row.pc_calibration_screen_in
            else False,
            "lamp": payload_config_row.pc_lamp,
            "calibration_filter": payload_config_row.pc_calibration_filter,
            "guide_method": payload_config_row.pc_guide_method,
            "instruments": self._instruments(payload_config_row),
        }

        return payload_config

    def _instruments(
        self, payload_config_row: Any
    ) -> Dict[str, Optional[List[Dict[str, Any]]]]:
        if payload_config_row.salticam_pattern_id is not None:
            salticam_setups: Optional[List[Dict[str, Any]]] = self._salticam_setups(
                payload_config_row.salticam_pattern_id
            )
        else:
            salticam_setups = None
        if payload_config_row.rss_pattern_id is not None:
            rss_setups: Optional[List[Dict[str, Any]]] = self._rss_setups(
                payload_config_row.rss_pattern_id
            )
        else:
            rss_setups = None
        if payload_config_row.hrs_pattern_id is not None:
            hrs_setups: Optional[List[Dict[str, Any]]] = self._hrs_setups(
                payload_config_row.hrs_pattern_id
            )
        else:
            hrs_setups = None
        if payload_config_row.bvit_pattern_id is not None:
            bvit_setups: Optional[List[Dict[str, Any]]] = self._bvit_setups(
                payload_config_row.bvit_pattern_id
            )
        else:
            bvit_setups = None
        if payload_config_row.nir_pattern_id is not None:
            nir_setups: Optional[List[Dict[str, Any]]] = self._nir_setups(
                payload_config_row.nir_pattern_id
            )
        else:
            nir_setups = None

        instruments = {
            "salticam": salticam_setups,
            "rss": rss_setups,
            "hrs": hrs_setups,
            "bvit": bvit_setups,
            "nir": nir_setups,
        }

        return instruments

    def _salticam_setups(self, salticam_pattern_id: int) -> List[Dict[str, Any]]:
        stmt = text(
            """
SELECT S.Salticam_Id AS salticam_id
FROM Salticam S
         JOIN SalticamPatternDetail SPD ON S.Salticam_Id = SPD.Salticam_Id
WHERE SPD.SalticamPattern_Id = :salticam_pattern_id
ORDER BY SPD.SalticamPattern_Order
        """
        )
        result = self.connection.execute(
            stmt, {"salticam_pattern_id": salticam_pattern_id}
        )
        return [
            self.instrument_repository.get_salticam(row.salticam_id) for row in result
        ]

    def _rss_setups(self, rss_pattern_id: int) -> List[Dict[str, Any]]:
        stmt = text(
            """
SELECT R.Rss_Id AS rss_id
FROM Rss R
         JOIN RssPatternDetail RPD ON R.Rss_Id = RPD.Rss_Id
WHERE RPD.RssPattern_Id = :rss_pattern_id
ORDER BY RPD.RssPattern_Order
        """
        )
        result = self.connection.execute(stmt, {"rss_pattern_id": rss_pattern_id})
        return [self.instrument_repository.get_rss(row.rss_id) for row in result]

    def _hrs_setups(self, hrs_pattern_id: int) -> List[Dict[str, Any]]:
        stmt = text(
            """
SELECT H.Hrs_Id AS hrs_id
FROM Hrs H
         JOIN HrsPatternDetail HPD ON H.Hrs_Id = HPD.Hrs_Id
WHERE HPD.HrsPattern_Id = :hrs_pattern_id
ORDER BY HPD.HrsPattern_Order
        """
        )
        result = self.connection.execute(stmt, {"hrs_pattern_id": hrs_pattern_id})
        return [self.instrument_repository.get_hrs(row.hrs_id) for row in result]

    def _bvit_setups(self, bvit_pattern_id: int) -> List[Dict[str, Any]]:
        stmt = text(
            """
SELECT B.Bvit_Id AS bvit_id
FROM Bvit B
         JOIN BvitPatternDetail BPD ON B.Bvit_Id = BPD.Bvit_Id
WHERE BPD.BvitPattern_Id = :bvit_pattern_id
ORDER BY BPD.BvitPattern_Order
        """
        )
        result = self.connection.execute(stmt, {"bvit_pattern_id": bvit_pattern_id})
        return [self.instrument_repository.get_bvit(row.bvit_id) for row in result]

    def _nir_setups(self, nir_pattern_id: int) -> List[Dict[str, Any]]:
        stmt = text(
            """
SELECT N.Nir_Id AS nir_id
FROM Nir N
         JOIN NirPatternDetail NPD ON N.Nir_Id = NPD.Nir_Id
WHERE NPD.NirPattern_Id = :nir_pattern_id
ORDER BY NPD.NirPattern_Order
        """
        )
        result = self.connection.execute(stmt, {"nir_pattern_id": nir_pattern_id})
        return [self.instrument_repository.get_nir(row.nir_id) for row in result]

    def _has_subblock_or_subsubblock_iterations(self, block_id: int) -> bool:
        """
        Check whether a block contains subblocks or subsubblocks with multiple
        iterations.
        """

        stmt = text(
            """
SELECT COUNT(*) AS c
FROM Pointing P
         JOIN SubBlock SB ON P.Block_Id = SB.Block_Id
         JOIN SubSubBlock SSB
              ON P.Block_Id = SSB.Block_Id AND P.SubBlock_Order = SSB.SubBlock_Order AND
                 P.SubSubBlock_Order = SSB.SubSubBlock_Order
         JOIN Block B ON P.Block_Id = B.Block_Id
WHERE B.Block_Id = :block_id
  AND (SB.Iterations > 1 OR SSB.Iterations > 1)
        """
        )
        result = self.connection.execute(stmt, {"block_id": block_id})
        return cast(bool, result.scalar_one() > 0)

    def _has_multiple_observations(self, pointing_id: int) -> bool:
        """
        Check whether a pointing contains multiple observations.
        """
        stmt = text(
            """
SELECT COUNT(DISTINCT Observation_Order) AS c
FROM TelescopeConfigObsConfig TCOC
WHERE TCOC.Pointing_Id = :pointing_id
        """
        )
        result = self.connection.execute(stmt, {"pointing_id": pointing_id})
        return cast(bool, result.scalar_one() > 1)

    def _get_scheduled_block_id(self) -> Optional[int]:
        """
        Get the id of the block scheduled next.
        """
        stmt = text("SELECT Block_Id FROM schedule")
        result = self.connection.execute(stmt)
        block_id = result.one_or_none()
        if block_id:
            return cast(int, block_id)
        return None

    def get_next_scheduled_block(self) -> Optional[Block]:
        """
        Get the block scheduled next.
        """
        block_id = self._get_scheduled_block_id()
        if block_id:
            return self.get(block_id)
        return None

    def get_proposal_codes_for_block_visits(
        self, block_visit_ids: List[int]
    ) -> List[str]:
        """
        Get the proposal codes for a list of block visit ids.
        """
        stmt = text(
            """
SELECT DISTINCT PC.Proposal_code
FROM ProposalCode PC
         JOIN Block B ON PC.ProposalCode_Id = B.ProposalCode_Id
         JOIN BlockVisit BV ON BV.Block_Id = B.Block_Id
         JOIN BlockVisitStatus BVS ON BV.BlockVisitStatus_Id = BVS.BlockVisitStatus_Id
WHERE BV.BlockVisit_Id IN :block_visit_ids
  AND BVS.BlockVisitStatus NOT IN ('Deleted');
        """
        )
        result = self.connection.execute(
            stmt,
            {"block_visit_ids": block_visit_ids},
        )

        try:
            return list(result.scalars())
        except NoResultFound:
            raise NotFoundError()
