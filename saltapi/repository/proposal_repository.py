import hashlib
import pathlib
import re
from collections import defaultdict
from datetime import date, datetime, time
from typing import Any, DefaultDict, Dict, List, Optional, cast

import pytz
from dateutil.relativedelta import relativedelta
from sqlalchemy import text
from sqlalchemy.engine import Connection
from sqlalchemy.exc import NoResultFound

from saltapi.exceptions import NotFoundError, ValidationError
from saltapi.service.proposal import Proposal, ProposalListItem
from saltapi.service.user import User
from saltapi.settings import get_settings
from saltapi.util import (
    TimeInterval,
    next_semester,
    normalised_hrs_mode,
    partner_name,
    semester_end,
    semester_of_datetime,
    semester_start,
    target_coordinates,
    target_magnitude,
    target_period_ephemeris,
    target_proper_motion,
    target_type,
    tonight,
)


class ProposalRepository:
    EXCLUDED_BLOCK_STATUS_VALUES = ["Deleted", "Superseded"]

    def __init__(self, connection: Connection):
        self.connection = connection

    def _list(
        self, username: str, from_semester: str, to_semester: str, limit: int
    ) -> List[ProposalListItem]:
        """
        Return a list of proposal summaries.
        """
        stmt = text(
            """
SELECT DISTINCT P.Proposal_Id                   AS id,
                PC.Proposal_Code                AS proposal_code,
                CONCAT(S.Year, '-', S.Semester) AS semester,
                PT.Title                        AS title,
                P.Phase                         AS phase,
                PS.Status                       AS status,
                PGI.StatusComment               AS comment,
                T.ProposalType                  AS proposal_type,
                Leader.PiptUser_Id              AS pi_user_id,
                Leader.FirstName                AS pi_given_name,
                Leader.Surname                  AS pi_family_name,
                Leader.Email                    AS pi_email,
                Contact.PiptUser_Id             AS pc_user_id,
                Contact.FirstName               AS pc_given_name,
                Contact.Surname                 AS pc_family_name,
                Contact.Email                   AS pc_email,
                Astronomer.PiptUser_Id          AS la_user_id,
                Astronomer.FirstName            AS la_given_name,
                Astronomer.Surname              AS la_family_name
FROM Proposal P
         JOIN ProposalCode PC ON P.ProposalCode_Id = PC.ProposalCode_Id
         JOIN ProposalGeneralInfo PGI ON PC.ProposalCode_Id = PGI.ProposalCode_Id
         JOIN ProposalText PT ON PC.ProposalCode_Id = PT.ProposalCode_Id AND
                                 P.Semester_Id = PT.Semester_Id
         JOIN Semester S ON P.Semester_Id = S.Semester_Id
         JOIN ProposalStatus PS ON PGI.ProposalStatus_Id = PS.ProposalStatus_Id
         JOIN ProposalType T ON PGI.ProposalType_Id = T.ProposalType_Id
         JOIN ProposalContact C ON PC.ProposalCode_Id = C.ProposalCode_Id
         LEFT JOIN ProposalInactiveReason PIR
                   ON PGI.ProposalInactiveReason_Id = PIR.ProposalInactiveReason_Id
         LEFT JOIN Investigator Astronomer
                   ON C.Astronomer_Id = Astronomer.Investigator_Id
         JOIN Investigator Contact ON C.Contact_Id = Contact.Investigator_Id
         JOIN Investigator Leader ON C.Leader_Id = Leader.Investigator_Id
         JOIN ProposalInvestigator PI ON PC.ProposalCode_Id = PI.ProposalCode_Id
         JOIN Investigator I ON PI.Investigator_Id = I.Investigator_Id
         JOIN PiptUser PU ON I.PiptUser_Id = PU.PiptUser_Id
         LEFT JOIN P1RequestedTime P1RT ON P.Proposal_Id = P1RT.Proposal_Id
         LEFT JOIN MultiPartner MP ON PC.ProposalCode_Id = MP.ProposalCode_Id AND
                                      S.Semester_Id = MP.Semester_Id
         LEFT JOIN PiptUserTAC PUT ON MP.Partner_Id = PUT.Partner_Id
         LEFT JOIN PiptUser TACUser ON PUT.PiptUser_Id = TACUser.PiptUser_Id
WHERE P.Current = 1
  AND S.Semester_Id IN (SELECT S2.Semester_Id
                        FROM Semester AS S2
                        WHERE CONCAT(S2.Year, '-', S2.Semester)
                                  BETWEEN :from_semester AND :to_semester)
  AND PS.Status != 'Deleted'
  AND (
    -- The user is an investigator on the proposal
            PU.Username = :username
        OR
        -- Proposal is requesting time from TAC to which the user belongs
            (TACUser.Username = :username AND MP.ReqTimePercent > 0)
        OR
        -- The proposal is a Gravitational Wave Event and the user is affiliated to
        -- a SALT partner
            (T.ProposalType = 'Gravitational Wave Event' AND (
                    (SELECT COUNT(*)
                     FROM Partner PUser
                              JOIN Institute IUser
                                   ON PUser.Partner_Id = IUser.Partner_Id
                              JOIN Investigator I2User
                                   ON IUser.Institute_Id = I2User.Institute_Id
                              JOIN PiptUser PUUser
                                   ON I2User.PiptUser_Id = PUUser.PiptUser_Id
                     WHERE PUUser.Username = :username
                       AND PUser.Partner_Code != 'OTH') > 0)
                )
        OR
        -- The user is allowed to view all proposals
            (
                    (SELECT COUNT(*)
                     FROM PiptUserSetting PUSRights
                              JOIN PiptSetting PSRights
                                   ON PUSRights.PiptSetting_Id = PSRights.PiptSetting_Id
                              JOIN PiptUser PURights
                                   ON PUSRights.PiptUser_Id = PURights.PiptUser_Id
                     WHERE PURights.Username = :username
                       AND PSRights.PiptSetting_Name = 'RightProposals'
                       AND PUSRights.Value >= 2) > 0
                )
        OR
        -- The user has been granted permission to view the proposal
            (
                    (SELECT COUNT(*)
                     FROM ProposalPermissionGrant PPG
                              JOIN PiptUser U ON PPG.Grantee_Id = U.PiptUser_Id
                              JOIN ProposalPermission PP ON PPG.ProposalPermission_Id =
                                                            PP.ProposalPermission_Id
                     WHERE U.Username = :username
                       AND PPG.ProposalCode_Id = PC.ProposalCode_Id
                        AND PP.ProposalPermission = 'View') > 0
                )
    )
ORDER BY P.Proposal_Id DESC
LIMIT :limit;
        """
        )
        result = self.connection.execute(
            stmt,
            {
                "username": username,
                "from_semester": from_semester,
                "to_semester": to_semester,
                "limit": limit,
            },
        )

        proposals = [
            {
                "id": row.id,
                "proposal_code": row.proposal_code,
                "semester": row.semester,
                "title": row.title,
                "phase": row.phase,
                "status": {"value": row.status, "comment": row.comment},
                "proposal_type": self._map_proposal_type(row.proposal_type),
                "principal_investigator": {
                    "id": row.pi_user_id,
                    "given_name": row.pi_given_name,
                    "family_name": row.pi_family_name,
                    "email": row.pi_email,
                },
                "principal_contact": {
                    "id": row.pc_user_id,
                    "given_name": row.pc_given_name,
                    "family_name": row.pc_family_name,
                    "email": row.pc_email,
                },
                "liaison_astronomer": self._liaison_astronomer(row),
            }
            for row in result
        ]

        return proposals

    @staticmethod
    def _liaison_astronomer(row: Any) -> Optional[Dict[str, str]]:
        if row.la_given_name is None:
            return None

        astronomer = {
            "given_name": row.la_given_name,
            "family_name": row.la_family_name,
        }

        return astronomer

    def list(
        self,
        username: str,
        from_semester: str = "2000-1",
        to_semester: str = "2099-2",
        limit: int = 1000000,
    ) -> List[Dict[str, Any]]:
        """
        Return a list of proposal summaries.

        The from and to semester are inclusive. The "from" semester must not be later
        than the "to" semester.
        """

        if not re.match(r"^\d{4}-\d$", from_semester):
            raise ValueError(f"Illegal semester format: {from_semester}")
        if not re.match(r"^\d{4}-\d$", to_semester):
            raise ValueError(f"Illegal semester format: {to_semester}")

        if semester_start(from_semester) > semester_start(to_semester):
            raise ValueError(
                "The from semester must not be later than the to semester."
            )

        if limit < 0:
            raise ValueError("The limit must not be negative.")

        return self._list(
            username=username,
            from_semester=from_semester,
            to_semester=to_semester,
            limit=limit,
        )

    def _get(
        self,
        proposal_code: str,
        semester: Optional[str],
        phase: Optional[int],
    ) -> Proposal:
        """
        Return the proposal content for a semester.
        """
        if semester is None:
            semester = self._latest_submission_semester(proposal_code)
        if phase is None:
            phase = self._latest_submission_phase(proposal_code)

        general_info = self._general_info(proposal_code, semester)

        # Replace the proprietary period with the data release date
        block_visits = self._block_visits(proposal_code)
        proprietary_period = general_info["proprietary_period"]
        general_info["proprietary_period"] = {
            "period": proprietary_period,
            "maximum_period": self.maximum_proprietary_period(proposal_code),
            "start_date": self.proprietary_period_start_date(block_visits),
        }
        general_info["current_submission"] = self._latest_submission_date(proposal_code)
        general_info["data_release_date"] = self._data_release_date(
            proprietary_period, block_visits
        )

        requested_times = self._get_requested_times(proposal_code)
        # A Phase 2-only proposal has no requested times
        summary_url = (
            f"/proposals/{proposal_code}-phase1-summary.pdf"
            if len(requested_times)
            else None
        )
        proposal: Dict[str, Any] = {
            "proposal_code": proposal_code,
            "semester": semester,
            "phase": phase,
            "general_info": general_info,
            "investigators": self._investigators(proposal_code),
            "blocks": self._blocks(proposal_code, semester),
            "block_visits": block_visits,
            "time_allocations": self.time_allocations(proposal_code, semester),
            "charged_time": self.charged_time(proposal_code, semester),
            "observation_comments": self.get_observation_comments(proposal_code),
            "targets": self._get_phase_one_targets(proposal_code),
            "requested_times": requested_times,
            "science_configurations": self._get_science_configurations(proposal_code),
            "phase1_proposal_summary": summary_url,
            "proposal_file": f"/proposals/{proposal_code}.zip",
        }
        return proposal

    def get(
        self,
        proposal_code: str,
        semester: Optional[str] = None,
        phase: Optional[int] = None,
    ) -> Proposal:
        try:
            return self._get(
                proposal_code=proposal_code, semester=semester, phase=phase
            )
        except NoResultFound:
            raise NotFoundError()

    def _semesters(self, proposal_code: str) -> List[str]:
        """
        Return an ordered list of the semesters for which this a proposal has been
        submitted.
        """
        stmt = text(
            """
SELECT DISTINCT CONCAT(S.Year, '-', S.Semester) AS semester
FROM Semester S
         JOIN Proposal P ON S.Semester_Id = P.Semester_Id
         JOIN ProposalCode PC ON P.ProposalCode_Id = PC.ProposalCode_Id
WHERE PC.Proposal_Code = :proposal_code
ORDER BY S.Year, S.Semester;
        """
        )
        result = self.connection.execute(stmt, {"proposal_code": proposal_code})
        return list(result.scalars())

    def list_of_semesters(self, proposal_code: str) -> List[str]:
        result = self._semesters(proposal_code)

        semesters = sorted(result, reverse=True)

        return semesters

    def get_proposal_type(self, proposal_code: str) -> str:
        stmt = text(
            """
SELECT PT.ProposalType AS proposal_type
FROM ProposalType PT
         JOIN ProposalGeneralInfo PGI ON PT.ProposalType_Id = PGI.ProposalType_Id
         JOIN ProposalCode PC ON PGI.ProposalCode_Id = PC.ProposalCode_Id
WHERE PC.Proposal_Code = :proposal_code
            """
        )
        result = self.connection.execute(stmt, {"proposal_code": proposal_code})
        proposal_type = result.scalar_one_or_none()
        if not proposal_type:
            raise NotFoundError()

        return self._map_proposal_type(proposal_type)

    def _latest_submission_semester(self, proposal_code: str) -> str:
        """
        Return the semester for which the latest submission was made.
        """
        stmt = text(
            """
SELECT CONCAT(S.Year, '-', S.Semester) AS semester
FROM Proposal P
         JOIN ProposalCode PC ON P.ProposalCode_Id = PC.ProposalCode_Id
         JOIN Semester S ON P.Semester_Id = S.Semester_Id
WHERE PC.Proposal_Code = :proposal_code
  AND P.Current = 1
ORDER BY S.Year DESC, S.Semester DESC
LIMIT 1
        """
        )
        result = self.connection.execute(stmt, {"proposal_code": proposal_code})
        return cast(str, result.scalar_one())

    def _latest_submission_phase(self, proposal_code: str) -> int:
        """Return the proposal phase of the latest submission."""
        stmt = text(
            """
SELECT P.Phase
FROM Proposal P
         JOIN ProposalCode PC ON P.ProposalCode_Id = PC.ProposalCode_Id
WHERE Proposal_Code = :proposal_code
ORDER BY P.Submission DESC
LIMIT 1
        """
        )
        result = self.connection.execute(stmt, {"proposal_code": proposal_code})
        return cast(int, result.scalar_one())

    def _first_submission_date(self, proposal_code: str) -> datetime:
        """
        Return the date and time when the first submission was made.
        """
        stmt = text(
            """
SELECT P.SubmissionDate AS submission_date
FROM Proposal P
         JOIN ProposalCode PC ON P.ProposalCode_Id = PC.ProposalCode_Id
WHERE PC.Proposal_Code = :proposal_code
  AND P.Submission = 1;
        """
        )
        result = self.connection.execute(stmt, {"proposal_code": proposal_code})
        dt = result.scalar_one()
        if type(dt) == date:
            dt = datetime.combine(dt, time.min)
        return cast(datetime, dt)

    def _latest_submission_date(self, proposal_code: str) -> datetime:
        """Return the date and time when the latest submission was made."""
        stmt = text(
            """
SELECT P.SubmissionDate
FROM Proposal P
         JOIN ProposalCode PC ON P.ProposalCode_Id = PC.ProposalCode_Id
WHERE PC.Proposal_Code = :proposal_code
ORDER BY P.Submission DESC
LIMIT 1
        """
        )
        result = self.connection.execute(stmt, {"proposal_code": proposal_code})
        return cast(datetime, result.scalar_one())

    def _latest_submission(self, proposal_code: str) -> int:
        """
        Return the submission number of the latest submission for any semester.
        """
        stmt = text(
            """
SELECT Submission
FROM Proposal P
         JOIN ProposalCode PC ON P.ProposalCode_Id = PC.ProposalCode_Id
WHERE P.Current = 1
  AND PC.Proposal_Code = :proposal_code
ORDER BY Submission DESC
LIMIT 1
        """
        )
        result = self.connection.execute(stmt, {"proposal_code": proposal_code})
        return cast(int, result.scalar())

    @staticmethod
    def _map_proposal_type(db_proposal_type: str) -> str:
        if db_proposal_type == "Director Discretionary Time (DDT)":
            return "Director's Discretionary Time"

        return db_proposal_type

    def _general_info(self, proposal_code: str, semester: str) -> Dict[str, Any]:
        """
        Return general proposal information for a semester.
        """
        year, sem = semester.split("-")
        stmt = text(
            """
SELECT PT.Title                            AS title,
       PT.Abstract                         AS abstract,
       PT.ReadMe                           AS summary_for_salt_astronomer,
       PT.NightlogSummary                  AS summary_for_night_log,
       P.Submission                        AS submission_number,
       T.ProposalType                      AS proposal_type,
       PS.Status                           AS status,
       PGI.StatusComment                   AS comment,
       PGI.ActOnAlert                      AS target_of_opportunity,
       P.TotalReqTime                      AS total_requested_time,
       PGI.ProprietaryPeriod               AS proprietary_period,
       I.PiptUser_Id                       AS astronomer_user_id,
       I.FirstName                         AS astronomer_given_name,
       I.Surname                           AS astronomer_family_name,
       I.Email                             AS astronomer_email,
       PGI.TimeRestricted                  AS is_time_restricted,
       P1T.Reason						   AS too_reason,
       I.PiptUser_Id                       AS liaison_salt_astronomer_id,
       IF(PGI.P4 IS NOT NULL,
          PGI.P4,
          0)                               AS is_p4,
       IF(PSA.PiPcMayActivate IS NOT NULL,
          PSA.PiPcMayActivate,
          0)                               AS self_activatable
FROM Proposal P
         JOIN Semester S ON P.Semester_Id = S.Semester_Id
         JOIN ProposalCode PC ON P.ProposalCode_Id = PC.ProposalCode_Id
         JOIN ProposalText PT ON
            PC.ProposalCode_Id = PT.ProposalCode_Id AND S.Semester_Id = PT.Semester_Id
         JOIN ProposalGeneralInfo PGI ON PC.ProposalCode_Id = PGI.ProposalCode_Id
         JOIN ProposalType T ON PGI.ProposalType_Id = T.ProposalType_Id
         JOIN ProposalStatus PS ON PGI.ProposalStatus_Id = PS.ProposalStatus_Id
         JOIN ProposalContact C ON PC.ProposalCode_Id = C.ProposalCode_Id
         LEFT JOIN Investigator I ON C.Astronomer_Id = I.Investigator_Id
         LEFT JOIN ProposalSelfActivation PSA ON P.ProposalCode_Id = PSA.ProposalCode_Id
         LEFT JOIN P1ToO P1T ON P.ProposalCode_Id = P1T.ProposalCode_Id
WHERE PC.Proposal_Code = :proposal_code
  AND P.Current = 1
  AND S.Year = :year
  AND S.Semester = :semester
        """
        )
        result = self.connection.execute(
            stmt, {"proposal_code": proposal_code, "year": year, "semester": sem}
        )
        row = result.one()

        info = {
            "title": row.title,
            "abstract": row.abstract,
            "summary_for_salt_astronomer": row.summary_for_salt_astronomer,
            "summary_for_night_log": row.summary_for_night_log,
            "submission_number": row.submission_number,
            "status": {"value": row.status, "comment": row.comment},
            "proposal_type": self._map_proposal_type(row.proposal_type),
            "is_target_of_opportunity": row.target_of_opportunity,
            "total_requested_time": row.total_requested_time,
            "proprietary_period": row.proprietary_period,
            "is_time_restricted": row.is_time_restricted != 0,
            "is_priority4": row.is_p4 != 0,
            "is_self_activatable": row.self_activatable != 0,
            "target_of_opportunity_reason": row.too_reason,
        }

        if info["proposal_type"] == "Director Discretionary Time (DDT)":
            info["proposal_type"] = "Director's Discretionary Time"

        if row.astronomer_email:
            info["liaison_salt_astronomer"] = {
                "id": row.liaison_salt_astronomer_id,
                "given_name": row.astronomer_given_name,
                "family_name": row.astronomer_family_name,
            }
        else:
            info["liaison_salt_astronomer"] = None

        info["first_submission"] = self._first_submission_date(proposal_code)
        info["submission_number"] = self._latest_submission(proposal_code)
        info["semesters"] = self._semesters(proposal_code)

        return info

    def _investigators(self, proposal_code: str) -> List[Dict[str, Any]]:
        """
        Return the list of investigators.

        The list is ordered by family nme and given name.
        """
        stmt = text(
            """
SELECT
    PU.PiptUser_Id          AS id,
    I.FirstName             AS given_name,
    I.Surname               AS family_name,
    I.Email                 AS email,
    P.Partner_Code          AS partner_code,
    P.Partner_Name          AS partner_name,
    `IN`.InstituteName_Name AS institution_name,
    I2.Institute_Id         AS institution_id,
    I2.Department           AS department,
    PI.InvestigatorOkay     AS approved,
    PI.ApprovalCode         AS approval_code,
    ThesisType		       AS thesis_type,
    ThesisDescr		       AS relevance_of_proposal,
    CompletionYear	       AS year_of_completion
FROM ProposalInvestigator PI
    JOIN Investigator I ON PI.Investigator_Id = I.Investigator_Id
    JOIN PiptUser PU ON I.PiptUser_Id = PU.PiptUser_Id
    JOIN Institute I2 ON I.Institute_Id = I2.Institute_Id
    JOIN Partner P ON I2.Partner_Id = P.Partner_Id
    JOIN InstituteName `IN` ON I2.InstituteName_Id = `IN`.InstituteName_Id
    JOIN ProposalCode PC ON PI.ProposalCode_Id = PC.ProposalCode_Id
    LEFT JOIN P1Thesis PT ON PC.ProposalCode_Id = PT.ProposalCode_Id
        AND PT.Student_Id = I.Investigator_Id
    LEFT JOIN ThesisType TT ON PT.ThesisType_Id = TT.ThesisType_Id
WHERE PC.Proposal_Code = :proposal_code
ORDER BY I.Surname, I.FirstName
        """
        )
        result = self.connection.execute(stmt, {"proposal_code": proposal_code})
        investigators = [dict(row) for row in result]

        pi_id = self._principal_investigator_user_id(proposal_code)
        pc_id = self._principal_contact_user_id(proposal_code)

        for investigator in investigators:
            investigator["is_pi"] = investigator["id"] == pi_id
            investigator["is_pc"] = investigator["id"] == pc_id

            partner_code = investigator["partner_code"]
            investigator["affiliation"] = {
                "partner_code": partner_code,
                "partner_name": investigator["partner_name"],
                "institution_id": investigator["institution_id"],
                "name": investigator["institution_name"],
                "department": investigator["department"],
            }
            if investigator["thesis_type"]:
                investigator["thesis"] = {
                    "thesis_type": investigator["thesis_type"],
                    "relevance_of_proposal": investigator["relevance_of_proposal"],
                    "year_of_completion": investigator["year_of_completion"],
                }
            else:
                investigator["thesis"] = None
            del investigator["partner_code"]
            del investigator["partner_name"]
            del investigator["institution_id"]
            del investigator["institution_name"]
            del investigator["department"]
            del investigator["thesis_type"]
            del investigator["relevance_of_proposal"]
            del investigator["year_of_completion"]

            if investigator["approved"] == 1:
                investigator["has_approved_proposal"] = True
            elif (
                investigator["approval_code"] is None
                or investigator["approval_code"] == ""
            ):
                investigator["has_approved_proposal"] = False
            else:
                investigator["has_approved_proposal"] = None

            del investigator["approved"]
            del investigator["approval_code"]
        return investigators

    def _principal_investigator_user_id(self, proposal_code: str) -> int:
        """
        Return the user id of the Principal Investigator.
        """
        stmt = text(
            """
SELECT I.PiptUser_Id
FROM ProposalContact PC
         JOIN Investigator I ON PC.Leader_Id = I.Investigator_Id
         JOIN ProposalCode P ON PC.ProposalCode_Id = P.ProposalCode_Id
WHERE P.Proposal_Code = :proposal_code
        """
        )
        result = self.connection.execute(stmt, {"proposal_code": proposal_code})
        return cast(int, result.scalar_one())

    def _principal_contact_user_id(self, proposal_code: str) -> int:
        """
        Return the user id of the Principal Contact.
        """
        stmt = text(
            """
SELECT I.PiptUser_Id
FROM ProposalContact PC
         JOIN Investigator I ON PC.Contact_Id = I.Investigator_Id
         JOIN ProposalCode P ON PC.ProposalCode_Id = P.ProposalCode_Id
WHERE P.Proposal_Code = :proposal_code
        """
        )
        result = self.connection.execute(stmt, {"proposal_code": proposal_code})
        return cast(int, result.scalar_one())

    def _blocks(self, proposal_code: str, semester: str) -> List[Dict[str, Any]]:
        """
        Return the blocks for a semester.
        """
        year, sem = semester.split("-")
        stmt = text(
            """
SELECT B.Block_Id                      AS id,
       CONCAT(S.Year, '-', S.Semester) AS semester,
       B.Block_Name                    AS name,
       BS.BlockStatus                  AS status,
       B.BlockStatusReason             AS reason,
       B.ObsTime                       AS observation_time,
       B.Priority                      AS priority,
       B.NVisits                       AS requested_observations,
       B.NDone                         AS accepted_observations,
       B.NAttempted                    AS rejected_observations,
       B.MinSeeing                     AS minimum_seeing,
       B.MaxSeeing                     AS maximum_seeing,
       T.Transparency                  AS transparency,
       B.MinLunarAngularDistance       AS minimum_lunar_distance,
       B.MaxLunarPhase                 AS maximum_lunar_phase
FROM Block B
         JOIN Transparency T ON B.Transparency_Id = T.Transparency_Id
         JOIN BlockStatus BS ON B.BlockStatus_Id = BS.BlockStatus_Id
         JOIN Proposal P ON B.Proposal_Id = P.Proposal_Id
         JOIN Semester S ON P.Semester_Id = S.Semester_Id
         JOIN ProposalCode PC ON B.ProposalCode_Id = PC.ProposalCode_Id
WHERE BS.BlockStatus NOT IN :excluded_status_values
  AND PC.Proposal_Code = :proposal_code
  AND S.Year = :year
  AND S.Semester = :semester
        """
        )
        result = self.connection.execute(
            stmt,
            {
                "excluded_status_values": self.EXCLUDED_BLOCK_STATUS_VALUES,
                "proposal_code": proposal_code,
                "year": year,
                "semester": sem,
            },
        )

        blocks = [
            {
                "id": row.id,
                "semester": row.semester,
                "name": row.name,
                "status": {
                    "value": row.status if row.status != "On Hold" else "On hold",
                    "reason": row.reason,
                },
                "observation_time": row.observation_time,
                "priority": row.priority,
                "requested_observations": row.requested_observations,
                "accepted_observations": row.accepted_observations,
                "rejected_observations": row.rejected_observations,
                "observing_conditions": {
                    "minimum_seeing": row.minimum_seeing,
                    "maximum_seeing": row.maximum_seeing,
                    "transparency": row.transparency,
                    "minimum_lunar_distance": row.minimum_lunar_distance,
                    "maximum_lunar_phase": row.maximum_lunar_phase,
                },
            }
            for row in result
        ]
        block_instruments = self._block_instruments(proposal_code)

        tonight_interval = tonight()
        remaining_nights_start = tonight_interval.end
        remaining_nights_end = semester_end(semester)
        remaining_nights_interval = TimeInterval(
            start=remaining_nights_start, end=remaining_nights_end
        )
        block_observable_tonight = self._block_observable_nights(
            proposal_code, semester, tonight_interval
        )
        block_remaining_nights = self._block_observable_nights(
            proposal_code, semester, remaining_nights_interval
        )

        for b in blocks:
            b["instruments"] = block_instruments[b["id"]]
            b["is_observable_tonight"] = block_observable_tonight.get(b["id"], False)
            b["remaining_nights"] = block_remaining_nights.get(b["id"], 0)

        return blocks

    def _block_visits(self, proposal_code: str) -> List[Dict[str, Any]]:
        """
        Return the executed observations (including observations in the queue) for all
        semesters.

        The observations are ordered by block name and observation night.
        """
        stmt = text(
            """
SELECT BV.BlockVisit_Id                            AS id,
       BV.Block_Id                                 AS block_id,
       B.Block_Name                                AS block_name,
       B.ObsTime                                   AS observation_time,
       B.Priority                                  AS priority,
       B.MaxLunarPhase                             AS maximum_lunar_phase,
       NI.Date                                     AS night,
       BVS.BlockVisitStatus                        AS status,
       BRR.RejectedReason                          AS rejection_reason
FROM BlockVisit BV
         JOIN BlockVisitStatus BVS ON BV.BlockVisitStatus_Id = BVS.BlockVisitStatus_Id
         LEFT JOIN BlockRejectedReason BRR
                   ON BV.BlockRejectedReason_Id = BRR.BlockRejectedReason_Id
         JOIN NightInfo NI ON BV.NightInfo_Id = NI.NightInfo_Id
         JOIN Block B ON BV.Block_Id = B.Block_Id
         JOIN ProposalCode PC ON B.ProposalCode_Id = PC.ProposalCode_Id
WHERE PC.Proposal_Code = :proposal_code
  AND BVS.BlockVisitStatus != 'Deleted'
ORDER BY B.Block_Name, NI.Date
        """
        )
        result = self.connection.execute(stmt, {"proposal_code": proposal_code})
        block_visits = [
            {
                "id": row.id,
                "block_id": row.block_id,
                "block_name": row.block_name,
                "observation_time": row.observation_time,
                "priority": row.priority,
                "maximum_lunar_phase": row.maximum_lunar_phase,
                "night": row.night,
                "status": row.status,
                "rejection_reason": row.rejection_reason,
            }
            for row in result
        ]

        block_targets = self._block_targets(proposal_code)
        for block_visit in block_visits:
            block_visit["targets"] = block_targets[block_visit["block_id"]]

        return block_visits

    def _block_targets(self, proposal_code: str) -> Dict[int, List[str]]:
        """
        Return the dictionary of block ids and lists of targets contained in the blocks
        for all semesters.
        """
        separator = "::::"
        stmt = text(
            """
SELECT B.Block_Id       AS block_id,
       GROUP_CONCAT(
            DISTINCT T.Target_Name ORDER BY T.Target_Name SEPARATOR :separator
        )               AS targets
FROM Target T
         JOIN Observation O ON T.Target_Id = O.Target_Id
         JOIN Pointing P ON O.Pointing_Id = P.Pointing_Id
         JOIN Block B ON P.Block_Id = B.Block_Id
         JOIN BlockStatus BS ON B.BlockStatus_Id = BS.BlockStatus_Id
         JOIN ProposalCode PC ON B.ProposalCode_Id = PC.ProposalCode_Id
WHERE PC.Proposal_Code = :proposal_code
GROUP BY B.Block_Id
        """
        )
        result = self.connection.execute(
            stmt,
            {
                "separator": separator,
                "proposal_code": proposal_code,
            },
        )
        return {row.block_id: row.targets.split(separator) for row in result}

    def _block_salticam_configurations(
        self, proposal_code: str
    ) -> Dict[int, Dict[str, List[str]]]:
        """
        Return the dictionary of block ids and Salticam configurations contained in the
        blocks.

        A block is only included in the dictionary if it is using Salticam. There is
        only one mode, which is an empty string.
        """
        stmt = text(
            """
SELECT B.Block_Id AS block_id
FROM ObsConfig OC
         JOIN PayloadConfig PC ON OC.PayloadConfig_Id = PC.PayloadConfig_Id
         JOIN PayloadConfigType PCT
            ON PC.PayloadConfigType_Id = PCT.PayloadConfigType_Id
         JOIN TelescopeConfigObsConfig TCOC
            ON OC.ObsConfig_Id = TCOC.PlannedObsConfig_Id
         JOIN Pointing P ON TCOC.Pointing_Id = P.Pointing_Id
         JOIN Block B ON P.Block_Id = B.Block_Id
         JOIN ProposalCode C ON B.ProposalCode_Id = C.ProposalCode_Id
WHERE C.Proposal_Code = :proposal_code
  AND OC.SalticamPattern_Id IS NOT NULL
  AND PCT.Type != 'Acquisition'
        """
        )
        result = self.connection.execute(
            stmt,
            {
                "proposal_code": proposal_code,
            },
        )
        return {row.block_id: {"modes": [""]} for row in result}

    def _block_rss_configurations(
        self, proposal_code: str
    ) -> Dict[int, Dict[str, List[str]]]:
        """
        Return the dictionary of block ids and a dictionary of RSS configurations contained in the
        blocks.

        A block is only included in the dictionary if it is using RSS. The configurations are
        ordered alphabetically for every block.
        """
        separator = "::::"
        stmt = text(
            """
SELECT B.Block_Id AS block_id,
       GROUP_CONCAT(DISTINCT RM.Mode ORDER BY RM.Mode SEPARATOR :separator) AS modes,
       GROUP_CONCAT(DISTINCT RG.Grating ORDER BY RG.Grating SEPARATOR :separator) AS gratings,
       GROUP_CONCAT(DISTINCT RF.Barcode  ORDER BY RF.Barcode  SEPARATOR :separator) AS filters
FROM RssMode RM
         JOIN RssConfig RC ON RM.RssMode_Id = RC.RssMode_Id
         JOIN Rss R ON RC.RssConfig_Id = R.RssConfig_Id
         JOIN RssFilter RF ON RC.RssFilter_Id = RF.RssFilter_Id
         JOIN RssPatternDetail RPD ON R.Rss_Id = RPD.Rss_Id
         JOIN RssPattern RP ON RPD.RssPattern_Id = RP.RssPattern_Id
         JOIN ObsConfig OC ON RP.RssPattern_Id = OC.RssPattern_Id
         JOIN TelescopeConfigObsConfig TCOC
            ON OC.ObsConfig_Id = TCOC.PlannedObsConfig_Id
         JOIN Pointing P ON TCOC.Pointing_Id = P.Pointing_Id
         JOIN Block B ON P.Block_Id = B.Block_Id
         JOIN ProposalCode PC ON B.ProposalCode_Id = PC.ProposalCode_Id
         LEFT JOIN RssSpectroscopy RS ON RC.RssSpectroscopy_Id = RS.RssSpectroscopy_Id
         LEFT JOIN RssGrating RG ON RS.RssGrating_Id = RG.RssGrating_Id
WHERE PC.Proposal_Code = :proposal_code
GROUP BY B.Block_Id
        """
        )
        result = self.connection.execute(
            stmt,
            {
                "separator": separator,
                "proposal_code": proposal_code,
            },
        )
        return {
            row.block_id: {
                "modes": row.modes.split(separator),
                "gratings": row.gratings.split(separator) if row.gratings else None,
                "filters": row.filters.split(separator) if row.filters else None,
            }
            for row in result
        }

    def _block_hrs_configurations(
        self, proposal_code: str
    ) -> Dict[int, Dict[str, List[str]]]:
        """
        Return the dictionary of block ids and a dictionary of HRS configurations contained in the
        blocks.

        A block is only included in the dictionary if it is using HRS. The modes are
        ordered alphabetically for every block.
        """
        separator = "::::"
        stmt = text(
            """
SELECT B.Block_Id AS block_id,
       GROUP_CONCAT(
            DISTINCT HM.ExposureMode ORDER BY HM.ExposureMode SEPARATOR :separator
        ) AS modes
FROM HrsMode HM
         JOIN HrsConfig HC ON HM.HrsMode_Id = HC.HrsMode_Id
         JOIN Hrs H ON HC.HrsConfig_Id = H.HrsConfig_Id
         JOIN HrsPatternDetail HPD ON H.Hrs_Id = HPD.Hrs_Id
         JOIN HrsPattern HP ON HPD.HrsPattern_Id = HP.HrsPattern_Id
         JOIN ObsConfig OC ON HP.HrsPattern_Id = OC.HrsPattern_Id
         JOIN TelescopeConfigObsConfig TCOC
         ON OC.ObsConfig_Id = TCOC.PlannedObsConfig_Id
         JOIN Pointing P ON TCOC.Pointing_Id = P.Pointing_Id
         JOIN Block B ON P.Block_Id = B.Block_Id
         JOIN ProposalCode PC ON B.ProposalCode_Id = PC.ProposalCode_Id
WHERE PC.Proposal_Code = :proposal_code
GROUP BY B.Block_Id
        """
        )
        result = self.connection.execute(
            stmt,
            {
                "separator": separator,
                "proposal_code": proposal_code,
            },
        )

        return {
            row.block_id: {
                "modes": [mode.title() for mode in row.modes.split(separator)]
            }
            for row in result
        }

    def _block_bvit_configurations(
        self, proposal_code: str
    ) -> Dict[int, Dict[str, List[str]]]:
        """
        Return the dictionary of block ids and a dictionary of BVIT configurations contained in the
        blocks.

        A block is only included in the dictionary if it is using BVIT. There is only
        one mode, which is an empty string.
        """
        stmt = text(
            """
SELECT B.Block_Id AS block_id
FROM ObsConfig OC
         JOIN TelescopeConfigObsConfig TCOC
         ON OC.ObsConfig_Id = TCOC.PlannedObsConfig_Id
         JOIN Pointing P ON TCOC.Pointing_Id = P.Pointing_Id
         JOIN Block B ON P.Block_Id = B.Block_Id
         JOIN ProposalCode C ON B.ProposalCode_Id = C.ProposalCode_Id
WHERE C.Proposal_Code = :proposal_code
  AND OC.BvitPattern_Id IS NOT NULL
        """
        )
        result = self.connection.execute(
            stmt,
            {
                "excluded_status_values": self.EXCLUDED_BLOCK_STATUS_VALUES,
                "proposal_code": proposal_code,
            },
        )
        return {row.block_id: {"modes": [""]} for row in result}

    def _block_instruments(self, proposal_code: str) -> Dict[int, List[Dict[str, Any]]]:
        """
        Return the dictionary of block ids and dictionaries of instruments configurations.
        """
        salticam_configurations = self._block_salticam_configurations(proposal_code)
        rss_configurations = self._block_rss_configurations(proposal_code)
        hrs_configurations = self._block_hrs_configurations(proposal_code)
        bvit_configurations = self._block_bvit_configurations(proposal_code)
        instruments: DefaultDict[int, List[Dict[str, Any]]] = defaultdict(list)
        for block_id, c in salticam_configurations.items():
            instruments[block_id].append({"name": "Salticam", "modes": c["modes"]})
        for block_id_, c_ in rss_configurations.items():
            instruments[block_id_].append(
                {
                    "name": "RSS",
                    "modes": c_["modes"],
                    "gratings": c_["gratings"],
                    "filters": c_["filters"],
                }
            )
        for block_id, c in hrs_configurations.items():
            instruments[block_id].append({"name": "HRS", "modes": c["modes"]})
        for block_id, c in bvit_configurations.items():
            instruments[block_id].append({"name": "BVIT", "modes": c["modes"]})
        return instruments

    def time_allocations(
        self, proposal_code: str, semester: str
    ) -> List[Dict[str, Any]]:
        """
        Return the time allocations and TAC comments for a semester.
        """
        allocations = self._allocations(proposal_code, semester)
        comments = self._tac_comments(proposal_code, semester)
        partner_codes = set([alloc["partner_code"] for alloc in allocations])
        partner_codes.update(comments.keys())

        # combine the time allocations and comments by partner
        combined: Dict[str, Dict[str, Any]] = {
            partner_code: {
                "partner_code": partner_code,
                "partner_name": partner_name(partner_code),
                "priority_0": 0,
                "priority_1": 0,
                "priority_2": 0,
                "priority_3": 0,
                "priority_4": 0,
                "tac_comment": None,
            }
            for partner_code in partner_codes
        }
        for partner_code, comment in comments.items():
            combined[partner_code]["tac_comment"] = comment
        for alloc in allocations:
            combined[alloc["partner_code"]][f"priority_{alloc['priority']}"] = alloc[
                "time_allocation"
            ]

        return list(combined.values())

    def _allocations(self, proposal_code: str, semester: str) -> List[Dict[str, Any]]:
        """
        Return the time allocations for a semester.
        """
        year, sem = semester.split("-")
        stmt = text(
            """
SELECT P.Partner_Code    AS partner_code,
       PA.Priority       AS priority,
       SUM(PA.TimeAlloc) AS time_allocation
FROM PriorityAlloc PA
         JOIN MultiPartner MP ON PA.MultiPartner_Id = MP.MultiPartner_Id
         JOIN ProposalCode PC ON MP.ProposalCode_Id = PC.ProposalCode_Id
         JOIN Semester S ON MP.Semester_Id = S.Semester_Id
         JOIN Partner P ON MP.Partner_Id = P.Partner_Id
WHERE PC.Proposal_Code = :proposal_code
  AND S.Year = :year
  AND S.Semester = :semester
GROUP BY PA.MultiPartner_Id, PA.Priority
        """
        )
        result = self.connection.execute(
            stmt, {"proposal_code": proposal_code, "year": year, "semester": sem}
        )
        return [
            {
                "partner_code": row.partner_code,
                "priority": row.priority,
                "time_allocation": int(row.time_allocation),
            }
            for row in result
        ]

    def _tac_comments(self, proposal_code: str, semester: str) -> Dict[str, str]:
        """
        Return the TAC comments for a semester.
        """
        year, sem = semester.split("-")
        stmt = text(
            """
SELECT P.Partner_Code AS partner_code,
       TPC.TacComment AS tac_comment
FROM TacProposalComment TPC
         JOIN MultiPartner MP ON TPC.MultiPartner_Id = MP.MultiPartner_Id
         JOIN Partner P ON MP.Partner_Id = P.Partner_Id
         JOIN ProposalCode PC ON MP.ProposalCode_Id = PC.ProposalCode_Id
         JOIN Semester S ON MP.Semester_Id = S.Semester_Id
WHERE PC.Proposal_Code = :proposal_code
  AND S.Year = :year
  AND S.Semester = :semester
        """
        )
        result = self.connection.execute(
            stmt, {"proposal_code": proposal_code, "year": year, "semester": sem}
        )
        return {
            row.partner_code: row.tac_comment if row.tac_comment else None
            for row in result
        }

    def charged_time(self, proposal_code: str, semester: str) -> Dict[str, int]:
        year, sem = semester.split("-")
        stmt = text(
            """
SELECT B.Priority AS priority, SUM(B.ObsTime) AS charged_time
FROM BlockVisit BV
    JOIN BlockVisitStatus BVS ON BV.BlockVisitStatus_Id = BVS.BlockVisitStatus_Id
    JOIN Block B ON BV.Block_Id = B.Block_Id
    JOIN Proposal P ON B.Proposal_Id = P.Proposal_Id
    JOIN ProposalCode PC ON B.ProposalCode_Id = PC.ProposalCode_Id
    JOIN Semester S ON P.Semester_Id = S.Semester_Id
WHERE PC.Proposal_Code = :proposal_code
    AND S.Year = :year
    AND S.Semester = :semester
    AND BVS.BlockVisitStatus = 'Accepted'
GROUP BY B.Priority
        """
        )
        result = self.connection.execute(
            stmt, {"proposal_code": proposal_code, "year": year, "semester": sem}
        )

        priority_charged_time: Dict[str, int] = {f"priority_{p}": 0 for p in range(5)}
        for row in result:
            priority_charged_time[f"priority_{row.priority}"] = int(row.charged_time)

        return priority_charged_time

    def _block_observable_nights(
        self, proposal_code: str, semester: str, interval: TimeInterval
    ) -> Dict[int, int]:
        """
        Return the number of nights in an interval when blocks are observable.

        The function returns a dictionary of block ids and number of nights. Blocks are
        included if they belong to the specified proposal and semester.

        The start and end time in the interval should be timezone sensitive and should
        be given as UTC times.

        This function check observability by checking whether the start times of
        observing windows lie in the given interval.

        Blocks may have multiple observing windows in a night. If so, only one of them
        is counted.
        """
        year, sem = semester.split("-")

        # There may be multiple observing windows for a block in a night. But if we
        # shift all times by 12 hours, all windows in the same night end up with the
        # same date. The number of nights is then the number of distinct dates.
        stmt = text(
            """
SELECT B.Block_Id                                                           AS block_id,
       COUNT(DISTINCT DATE(DATE_SUB(BVW.VisibilityStart, INTERVAL 12 HOUR))) AS nights
FROM BlockVisibilityWindow BVW
         JOIN BlockVisibilityWindowType BVWT
         ON BVW.BlockVisibilityWindowType_Id = BVWT.BlockVisibilityWindowType_Id
         JOIN Block B ON BVW.Block_Id = B.Block_Id
         JOIN Proposal P ON B.Proposal_Id = P.Proposal_Id
         JOIN ProposalCode PC ON P.ProposalCode_Id = PC.ProposalCode_Id
         JOIN Semester S ON P.Semester_Id = S.Semester_Id
WHERE PC.Proposal_Code = :proposal_code
  AND S.Year = :year
  AND S.Semester = :semester
  AND BVW.VisibilityStart BETWEEN :start AND :end
  AND BVWT.BlockVisibilityWindowType='Strict'
GROUP BY B.Block_Id
        """
        )
        result = self.connection.execute(
            stmt,
            {
                "proposal_code": proposal_code,
                "year": year,
                "semester": sem,
                "start": interval.start,
                "end": interval.end,
            },
        )
        return {int(row.block_id): int(row.nights) for row in result}

    def get_observation_comments(self, proposal_code: str) -> List[Dict[str, Any]]:
        """
        Return the proposal comments ordered by the time when they were made.
        """
        stmt = text(
            """
SELECT PC.ProposalComment_Id               AS id,
       PC.CommentDate                      AS comment_date,
       CONCAT(I.FirstName, ' ', I.Surname) AS author,
       PC.ProposalComment                  AS comment
FROM ProposalComment PC
         JOIN Investigator I ON PC.Investigator_Id = I.Investigator_Id
         JOIN ProposalCode P ON PC.ProposalCode_Id = P.ProposalCode_Id
WHERE P.Proposal_Code = :proposal_code
ORDER BY PC.CommentDate, PC.ProposalComment_Id
        """
        )
        result = self.connection.execute(stmt, {"proposal_code": proposal_code})
        return [dict(row) for row in result]

    def add_observation_comment(
        self, proposal_code: str, comment: str, user: User
    ) -> Dict[str, Any]:
        istmt = text(
            """
INSERT INTO ProposalComment(
    ProposalCode_Id,
    CommentDate,
    Investigator_Id,
    ProposalComment
)
VALUES (
    (SELECT ProposalCode_Id FROM ProposalCode WHERE Proposal_Code = :proposal_code),
    :date,
    (SELECT Investigator_Id FROM PiptUser WHERE Username = :username),
    :comment
)
    """
        )
        comment_date = date.today()
        insert_results = self.connection.execute(
            istmt,
            {
                "proposal_code": proposal_code,
                "username": user.username,
                "comment": comment,
                "date": comment_date,
            },
        )
        sstmt = text(
            """
SELECT PC.ProposalComment_Id               AS id,
       PC.CommentDate                      AS comment_date,
       CONCAT(I.FirstName, ' ', I.Surname) AS author,
       PC.ProposalComment                  AS comment
FROM ProposalComment PC
         JOIN Investigator I ON PC.Investigator_Id = I.Investigator_Id
         JOIN ProposalCode P ON PC.ProposalCode_Id = P.ProposalCode_Id
WHERE PC.ProposalComment_Id = :proposal_comment_id
    """
        )
        select_results = self.connection.execute(
            sstmt, {"proposal_comment_id": insert_results.lastrowid}
        )

        return dict(select_results.one())

    def get_proposal_status(self, proposal_code: str) -> Dict[str, Any]:
        """
        Return the proposal status for a proposal.
        """
        stmt = text(
            """
SELECT
    PS.Status 			AS `status`,
    PGI.StatusComment 	AS `comment`
FROM ProposalGeneralInfo PGI
         JOIN ProposalStatus PS ON PS.ProposalStatus_Id = PGI.ProposalStatus_Id
         JOIN ProposalCode PC ON PGI.ProposalCode_Id = PC.ProposalCode_Id
WHERE PC.Proposal_Code = :proposal_code
        """
        )
        result = self.connection.execute(stmt, {"proposal_code": proposal_code})
        try:
            row = result.one()

            status = {"value": row.status, "comment": row.comment}

            return status

        except NoResultFound:
            raise NotFoundError()

    def _proposal_inactive_reason_id(self, inactive_reason: str) -> int:
        stmt = text(
            """
SELECT PIR.ProposalInactiveReason_Id AS id
FROM ProposalInactiveReason PIR
WHERE PIR.InactiveReason = :inactive_reason
        """
        )
        result = self.connection.execute(stmt, {"inactive_reason": inactive_reason})
        return cast(int, result.scalar_one())

    def update_proposal_status(
        self, proposal_code: str, status: str, status_comment: Optional[str] = None
    ) -> None:
        """
        Update the status of a proposal.
        """

        # We could query for the status and reason ids within the UPDATE query, but then it would
        # not be clear whether a failing query is due to a wrong proposal code or a
        # wrong status or reason value.
        try:
            status_id = self._proposal_status_id(status)
        except NoResultFound:
            raise ValueError(f"Unknown proposal status: {status}")

        try:
            proposal_code_id = self._get_proposal_code_id(proposal_code)
        except NoResultFound:
            raise ValueError(f"Unknown proposal code: {proposal_code}")

        stmt = text(
            """
UPDATE ProposalGeneralInfo  PGI
SET
    PGI.ProposalStatus_Id = :status_id,
    PGI.StatusComment = :status_comment
WHERE ProposalCode_Id = :proposal_code_id;
        """
        )
        result = self.connection.execute(
            stmt,
            {
                "proposal_code_id": proposal_code_id,
                "status_id": status_id,
                "status_comment": status_comment,
            },
        )
        if not result.rowcount:
            raise NotFoundError()

    def _proposal_status_id(self, status: str) -> int:
        """
        Return the id of a proposal status value.
        """
        stmt = text(
            """
SELECT PS.ProposalStatus_Id
FROM ProposalStatus PS
WHERE PS.Status = :status
        """
        )
        result = self.connection.execute(stmt, {"status": status})
        return cast(int, result.scalar_one())

    def is_self_activatable(self, proposal_code: str) -> bool:
        """
        Check whether the proposal may be activated by the Principal Investigator and
        Principal Contact.
        """
        stmt = text(
            """
SELECT PSA.PiPcMayActivate
FROM ProposalSelfActivation PSA
         JOIN ProposalCode PC ON PSA.ProposalCode_Id = PC.ProposalCode_Id
WHERE PC.Proposal_Code = :proposal_code;
        """
        )
        result = self.connection.execute(stmt, {"proposal_code": proposal_code})
        try:
            one = result.scalar_one_or_none()
        except NoResultFound:
            raise NotFoundError(f"No such proposal code: {proposal_code}")

        return bool(cast(int, one) if one is not None else 0 > 0)

    def get_current_version(self, proposal_code: str) -> int:
        """
        Return the current version (number) of a proposal.

        Parameters
        ----------
        proposal_code: str
            The proposal code.

        Returns
        -------
        int
            The proposal version.
        """
        stmt = text(
            """
SELECT MAX(Submission) AS version
FROM Proposal P
JOIN ProposalCode PC ON P.ProposalCode_Id = PC.ProposalCode_Id
WHERE PC.Proposal_Code = :proposal_code
        """
        )
        result = self.connection.execute(stmt, {"proposal_code": proposal_code})
        version = result.scalar_one()
        if version is None:
            raise NotFoundError(f"No such proposal code: {proposal_code}")

        return cast(int, version)

    def get_current_phase1_version(self, proposal_code: str) -> Optional[int]:
        """
        Return the current version (number) of a proposal.

        Parameters
        ----------
        proposal_code: str
            The proposal code.

        Returns
        -------
        int
            The proposal version.
        """
        stmt = text(
            """
SELECT COUNT(Submission) AS version
FROM Proposal P
JOIN ProposalCode PC ON P.ProposalCode_Id = PC.ProposalCode_Id
WHERE PC.Proposal_Code = :proposal_code AND P.Phase = 1
        """
        )
        result = self.connection.execute(stmt, {"proposal_code": proposal_code})
        current_version = result.scalar_one()
        if current_version == 0:
            return None

        return cast(int, current_version)

    @staticmethod
    def generate_proposal_progress_filename(
        file_content: bytes, is_supplementary: bool = False
    ) -> str:
        hash_md = hashlib.md5(file_content).hexdigest()  # nosec
        if is_supplementary:
            return f"ProposalProgressSupplementary-{hash_md}.pdf"

        return f"ProposalProgressReport-{hash_md}.pdf"

    def insert_or_update_proposal_progress(
        self,
        progress_report_data: Dict[str, Any],
        proposal_code: str,
        semester: str,
        filenames: Dict[str, Optional[str]],
    ) -> None:
        """
        Insert or update the proposal progress information.
        """
        stmt = text(
            """
INSERT INTO ProposalProgress (
    ProposalCode_Id,
    Semester_Id,
    TimeRequestChangeReasons,
    StatusSummary,
    StrategyChanges,
    ReportPath,
    SupplementaryPath,
    SubmissionDate
)
VALUES(
    (SELECT ProposalCode_Id FROM ProposalCode WHERE Proposal_Code = :proposal_code),
    (SELECT Semester_Id FROM Semester WHERE CONCAT(`Year`, '-', Semester) = :semester),
    :change_reason,
    :summary_of_proposal_status,
    :strategy_changes,
    :report_path,
    :supplementary_path,
    NOW()
) ON DUPLICATE KEY UPDATE
    TimeRequestChangeReasons = :change_reason,
    StatusSummary = :summary_of_proposal_status,
    StrategyChanges = :strategy_changes,
    ReportPath = :report_path,
    SupplementaryPath = :supplementary_path,
    SubmissionDate = NOW()
;
        """
        )
        result = self.connection.execute(
            stmt,
            {
                "proposal_code": proposal_code,
                "semester": semester,
                "change_reason": progress_report_data["change_reason"],
                "summary_of_proposal_status": progress_report_data[
                    "summary_of_proposal_status"
                ],
                "strategy_changes": progress_report_data["strategy_changes"],
                "report_path": filenames["proposal_progress_filename"],
                "supplementary_path": filenames["additional_pdf_filename"],
            },
        )
        if not result.rowcount:
            raise NotFoundError()

    def _reset_partner_requested_time_and_percentages(
        self, proposal_code: str, semester: str, requested_time: int
    ) -> None:
        stmt = text(
            """
UPDATE MultiPartner
SET ReqTimeAmount=:requested_time,
    ReqTimePercent=0
WHERE ProposalCode_Id =
      (SELECT ProposalCode_Id FROM ProposalCode WHERE Proposal_Code = :proposal_code)
  AND Semester_Id =
      (SELECT Semester_Id FROM Semester WHERE CONCAT(Year, '-', semester) = :semester);
              """
        )
        self.connection.execute(
            stmt,
            {
                "proposal_code": proposal_code,
                "semester": semester,
                "requested_time": requested_time,
            },
        )

    def _insert_or_update_requested_time(
        self,
        proposal_code: str,
        semester: str,
        partner_code: str,
        requested_time_percent: float,
        requested_time_amount: int,
    ) -> None:
        """
        Insert or update proposal progress requested time.
        """
        stmt = text(
            """
INSERT INTO MultiPartner(
    ProposalCode_Id,
    Partner_Id,
    Semester_Id,
    ReqTimePercent,
    ReqTimeAmount
)
VALUES (
    (SELECT ProposalCode_Id FROM ProposalCode WHERE Proposal_Code = :proposal_code),
    (SELECT Partner_Id FROM Partner WHERE Partner_Code = :partner_code),
    (SELECT Semester_Id FROM Semester WHERE CONCAT(`Year`, '-', Semester) = :semester),
    :requested_time_percent,
    :requested_time_amount
) ON DUPLICATE KEY UPDATE
    ReqTimePercent = :requested_time_percent,
    ReqTimeAmount = :requested_time_amount
        """
        )
        self.connection.execute(
            stmt,
            {
                "proposal_code": proposal_code,
                "semester": semester,
                "partner_code": partner_code,
                "requested_time_percent": requested_time_percent,
                "requested_time_amount": requested_time_amount,
            },
        )

    def _insert_or_update_observing_conditions(
        self,
        proposal_code: str,
        semester: str,
        maximum_seeing: float,
        transparency: str,
        observing_conditions_description: str,
    ) -> None:
        """
        Insert or update the observing conditions
        """
        stmt = text(
            """
INSERT INTO P1ObservingConditions (
    ProposalCode_Id,
    Semester_Id,
    MaxSeeing,
    Transparency_Id,
    ObservingConditionsDescription
)
VALUES
(
    (SELECT ProposalCode_Id FROM ProposalCode WHERE Proposal_Code = :proposal_code),
    (SELECT Semester_Id FROM Semester WHERE CONCAT(`Year`, '-', Semester) = :semester),
    :maximum_seeing,
    (SELECT Transparency_Id FROM Transparency WHERE Transparency = :transparency),
    :observing_conditions_description
) ON DUPLICATE KEY UPDATE
    MaxSeeing = :maximum_seeing,
    Transparency_Id = (SELECT Transparency_Id FROM Transparency WHERE Transparency = :transparency),
    ObservingConditionsDescription = :observing_conditions_description

        """
        )
        result = self.connection.execute(
            stmt,
            {
                "proposal_code": proposal_code,
                "semester": semester,
                "maximum_seeing": maximum_seeing,
                "transparency": transparency,
                "observing_conditions_description": observing_conditions_description,
            },
        )
        if not result.rowcount:
            raise NotFoundError()

    def get_latest_observing_conditions(
        self, proposal_code: str, semester: str
    ) -> Optional[Dict[str, Any]]:
        stmt = text(
            """
SELECT
    CONCAT(S.`Year`, '-', S.Semester)   AS semester,
    MaxSeeing						    AS seeing,
    Transparency					    AS transparency,
    ObservingConditionsDescription	    AS description
FROM P1ObservingConditions AS OC
    JOIN Transparency AS T ON (OC.Transparency_Id = T.Transparency_Id)
    JOIN ProposalCode AS PC ON (OC.ProposalCode_Id = PC.ProposalCode_Id)
    JOIN Semester AS S ON (OC.Semester_Id = S.Semester_Id)
WHERE PC.Proposal_Code = :proposal_code
    AND semester <= :semester
ORDER BY semester DESC;
    """
        )
        results = self.connection.execute(
            stmt, {"proposal_code": proposal_code, "semester": semester}
        )
        last = results.first()
        if last:
            return {
                "seeing": last.seeing,
                "transparency": last.transparency,
                "description": last.description,
            }
        else:
            return None

    def get_observed_time(self, proposal_code: str) -> List[Dict[str, Any]]:
        stmt = text(
            """
SELECT
    CONCAT(S.`Year`, '-', S.Semester) AS semester,
    SUM(Obstime)                AS observed_time
FROM Proposal		    AS P
    JOIN ProposalCode 	AS PC USING (ProposalCode_Id)
    JOIN `Block` 		AS B USING (Proposal_Id)
    JOIN BlockVisit 	AS BV USING (Block_Id)
    JOIN BlockVisitStatus AS BVS USING (BlockVisitStatus_Id)
    JOIN Semester 		AS S ON (P.Semester_Id = S.Semester_Id)
WHERE BlockVisitStatus = 'Accepted'
    AND Proposal_Code = :proposal_code
    GROUP BY S.Semester_Id
    """
        )
        result = self.connection.execute(stmt, {"proposal_code": proposal_code})
        try:
            return [
                {"semester": row.semester, "observed_time": row.observed_time}
                for row in result
            ]
        except NoResultFound:
            raise NotFoundError()

    def get_allocated_and_requested_time(
        self, proposal_code: str
    ) -> List[Dict[str, Any]]:
        # ReqTimeAmount is the total amount of time requested by a proposal per semester
        # for all partners combined; hence there is no need to sum its value.
        stmt = text(
            """
SELECT
    CONCAT(S.`Year`, '-', S.Semester) AS semester,
    ReqTimeAmount 	AS requested_time,
    SUM(IF(TimeAlloc IS NULL, 0, TimeAlloc)) 	AS allocated_time
FROM MultiPartner 	AS MP
    LEFT JOIN PriorityAlloc 	AS PA ON (MP.MultiPartner_Id = PA.MultiPartner_Id)
    JOIN ProposalCode 	AS PC ON (MP.ProposalCode_Id = PC.ProposalCode_Id)
    JOIN Semester 		AS S ON (MP.Semester_Id = S.Semester_Id)
WHERE Proposal_Code=:proposal_code
    GROUP BY S.Semester_Id
    """
        )
        result = self.connection.execute(stmt, {"proposal_code": proposal_code})
        try:
            return [
                {
                    "semester": row.semester,
                    "requested_time": row.requested_time,
                    "allocated_time": row.allocated_time or 0,
                }
                for row in result
            ]
        except NoResultFound:
            raise NotFoundError()

    def _get_time_statistics(self, proposal_code: str) -> List[Dict[str, Any]]:
        allocated_requested = self.get_allocated_and_requested_time(proposal_code)
        observed_time = self.get_observed_time(proposal_code)
        time_statistics = []
        for ar in allocated_requested:
            tmp = {
                "semester": ar["semester"],
                "requested_time": ar["requested_time"],
                "allocated_time": ar["allocated_time"],
                "observed_time": 0,
            }
            for ot in observed_time:
                if ot["semester"] == ar["semester"]:
                    tmp["observed_time"] = ot["observed_time"]
            time_statistics.append(tmp)
        return time_statistics

    def _get_partner_requested_percentages(
        self, proposal_code: str, semester: str
    ) -> List[Dict[str, Any]]:
        stmt = text(
            """
SELECT
    Partner_Code 						AS partner_code,
    Partner_Name 						AS partner_name,
    ReqTimePercent						AS requested_percentage,
    CONCAT(S.Year, '-', S.Semester)     AS semester
FROM MultiPartner MP
    JOIN ProposalCode PC ON MP.ProposalCode_Id = PC.ProposalCode_Id
    JOIN Semester S ON MP.Semester_Id = S.Semester_Id
    JOIN Partner AS P ON (MP.Partner_Id = P.Partner_Id)
WHERE PC.Proposal_Code = :proposal_code
    """
        )
        result = self.connection.execute(stmt, {"proposal_code": proposal_code})
        tmp = dict()
        # Some partners may have a time request (which may be 0) for other semesters,
        # but not for the one under consideration. We therefore collect the partners for
        # which there is a time request percentage in any semester, and if a partner has
        # a time request for the semester under consideration, we store that request.
        for row in result:
            if row.partner_code not in tmp:
                tmp[row.partner_code] = {
                    "partner_name": row.partner_name,
                    "partner_code": row.partner_code,
                }
            if semester == row.semester:
                tmp[row.partner_code]["requested_percentage"] = row.requested_percentage
        prp = []
        # Afterwards we set the percentage to 0 for all those partners who don't
        # have a request for the semester under consideration.
        for pc in tmp:
            tmp[pc].setdefault("requested_percentage", 0)
            prp.append(tmp[pc])
        return prp

    def get_phase1_summary(self, proposal_code: str) -> pathlib.Path:
        """
        Return the path of the latest Phase 1 summary file.

        The summary file for a Phase 1 submission is stored in a folder
        <proposal_code>/<submission_number> and has the name Summary.pdf.

        Parameters
        ----------
        proposal_code

        Returns
        -------
        `~pathlib.Path`
           The file path.

        """
        current_phase1_version = self.get_current_phase1_version(proposal_code)
        if current_phase1_version is None:
            raise NotFoundError(
                f"There exists no phase 1 proposal summary for proposal {proposal_code}"
            )

        path = (
            get_settings().proposals_dir
            / f"{proposal_code}"
            / str(current_phase1_version)
            / "Summary.pdf"
        )
        if not path.is_file():
            raise NotFoundError(
                f"No phase 1 proposal summary found for proposal {proposal_code}"
            )

        return path

    def get_proposal_file(self, proposal_code: str) -> pathlib.Path:
        """
        Return the path of the latest proposal zip file.

        The proposal zip file for a submission  is stored in a folder
        <proposal_code>/<submission_number> and has the name <proposal_code>/zip.

        Parameters
        ----------
        proposal_code

        Returns
        -------
        `~pathlib.Path`
            The file path.

        """
        proposals_dir = get_settings().proposals_dir
        version = self.get_current_version(proposal_code)
        path = proposals_dir / proposal_code / str(version) / f"{proposal_code}.zip"
        if not path.exists():
            raise NotFoundError(f"No proposal file found for proposal {proposal_code}")

        return path

    def get_progress_report_semesters(self, proposal_code: str) -> List[str]:
        """
        Return the list of semesters for which a progress report has been submitted.

        The list is sorted in ascending order.

        Parameters
        ----------
        proposal_code: str
            Proposal code.

        Returns
        -------
        list of str
            The sorted list of semesters.
        """
        stmt = text(
            """
SELECT CONCAT(S.Year, '-', S.Semester) AS semester
FROM ProposalProgress PP
         JOIN ProposalCode PC ON PP.ProposalCode_Id = PC.ProposalCode_Id
         JOIN Semester S ON PP.Semester_Id = S.Semester_Id
WHERE PC.Proposal_Code = :proposal_code;

        """
        )
        result = self.connection.execute(stmt, {"proposal_code": proposal_code})
        return sorted(row.semester for row in result)

    def get_progress_report(self, proposal_code: str, semester: str) -> Dict[str, Any]:
        stmt = text(
            """
SELECT
    MaxSeeing							AS maximum_seeing,
    Transparency						AS transparency,
    ObservingConditionsDescription		AS description_of_observing_constraints,
    TimeRequestChangeReasons			AS change_reason,
    StatusSummary						AS summary_of_proposal_status,
    StrategyChanges						AS strategy_changes,
    CONCAT(S.`Year`, '-', S.Semester)   AS semester,
    ReportPath                          AS proposal_progress_pdf,
    SupplementaryPath                   AS additional_pdf
FROM P1ObservingConditions OC
    JOIN Transparency T ON (OC.Transparency_Id = T.Transparency_Id)
    JOIN ProposalCode PC ON (OC.ProposalCode_Id = PC.ProposalCode_Id)
    JOIN Semester S ON (OC.Semester_Id = S.Semester_Id)
    LEFT JOIN ProposalProgress PP ON (
        OC.ProposalCode_Id = PP.ProposalCode_Id
        AND OC.Semester_Id = PP.Semester_Id
    )
WHERE PC.Proposal_Code = :proposal_code
    AND CONCAT(S.`Year`, '-', S.Semester) = :semester
    """
        )
        result = self.connection.execute(
            stmt, {"proposal_code": proposal_code, "semester": semester}
        )
        time_statistics = self._get_time_statistics(proposal_code)
        requested_time = None
        _next_semester = next_semester()
        for t in time_statistics:
            if _next_semester == t["semester"]:
                requested_time = t["requested_time"]
        if result.rowcount > 0:
            progress_report = {}
            for row in result:
                progress_report["requested_time"] = requested_time
                progress_report["semester"] = row.semester
                progress_report["maximum_seeing"] = row.maximum_seeing
                progress_report["transparency"] = row.transparency
                progress_report["additional_pdf"] = row.additional_pdf
                progress_report["proposal_progress_pdf"] = row.proposal_progress_pdf
                progress_report[
                    "description_of_observing_constraints"
                ] = row.description_of_observing_constraints
                progress_report["change_reason"] = row.change_reason
                progress_report[
                    "summary_of_proposal_status"
                ] = row.summary_of_proposal_status
                progress_report["strategy_changes"] = row.strategy_changes
                progress_report["previous_time_requests"] = time_statistics
                progress_report[
                    "last_observing_constraints"
                ] = self.get_latest_observing_conditions(proposal_code, semester)
                progress_report[
                    "partner_requested_percentages"
                ] = self._get_partner_requested_percentages(
                    proposal_code, _next_semester
                )
            return progress_report
        else:
            return {
                "requested_time": requested_time,
                "semester": None,
                "maximum_seeing": None,
                "transparency": None,
                "additional_pdf": None,
                "proposal_progress_pdf": None,
                "description_of_observing_constraints": None,
                "change_reason": None,
                "summary_of_proposal_status": None,
                "strategy_changes": None,
                "partner_requested_percentages": self._get_partner_requested_percentages(
                    proposal_code, _next_semester
                ),
                "previous_time_requests": time_statistics,
                "last_observing_constraints": self.get_latest_observing_conditions(
                    proposal_code, semester
                ),
            }

    def put_proposal_progress(
        self,
        proposal_progress: Dict[str, Any],
        proposal_code: str,
        semester: str,
        filenames: Dict[str, Optional[str]],
    ) -> None:
        """
        Insert the proposal progress into the database, or update the existing one.
        """
        _next_semester = next_semester()
        self._reset_partner_requested_time_and_percentages(
            proposal_code, _next_semester, proposal_progress["requested_time"]
        )
        for rp in proposal_progress["partner_requested_percentages"]:
            self._insert_or_update_requested_time(
                proposal_code=proposal_code,
                semester=_next_semester,
                partner_code=rp["partner_code"],
                requested_time_percent=rp["requested_percentage"],
                requested_time_amount=proposal_progress["requested_time"],
            )
        self._insert_or_update_observing_conditions(
            proposal_code=proposal_code,
            semester=_next_semester,
            maximum_seeing=proposal_progress["maximum_seeing"],
            transparency=proposal_progress["transparency"],
            observing_conditions_description=proposal_progress[
                "description_of_observing_constraints"
            ],
        )
        self.insert_or_update_proposal_progress(
            progress_report_data=proposal_progress,
            proposal_code=proposal_code,
            semester=semester,
            filenames=filenames,
        )

    def insert_proprietary_period_extension_request(
        self,
        proposal_code: str,
        proprietary_period: int,
        motivation: str,
        username: str,
    ) -> None:
        stmt = text(
            """
INSERT INTO ProprietaryPeriodExtensionRequest(
    ProposalCode_Id,
    Reason,
    RequestedBy,
    RequestedPeriod
)
VALUES (
    (SELECT ProposalCode_Id FROM ProposalCode WHERE Proposal_Code = :proposal_code),
    :reason,
    (SELECT PiptUser_Id FROM PiptUser WHERE Username = :username),
    :requested_period
)
    """
        )
        self.connection.execute(
            stmt,
            {
                "proposal_code": proposal_code,
                "username": username,
                "reason": motivation,
                "requested_period": proprietary_period,
            },
        )

    @staticmethod
    def proprietary_period_start_date(block_visits: List[Dict[str, Any]]) -> date:
        # find the latest observation

        observation_night: Optional[date] = None
        for observation in block_visits:
            if not observation_night:
                observation_night = observation["night"]
            if observation["night"] > observation_night:
                observation_night = observation["night"]
        if not observation_night:
            observation_night = datetime.today()

        return semester_end(
            semester_of_datetime(
                datetime(
                    observation_night.year,
                    observation_night.month,
                    observation_night.day,
                    12,
                    0,
                    0,
                    1,
                    tzinfo=pytz.utc,
                )
            )
        ).date()

    def _data_release_date(
        self, proprietary_period: int, block_visits: List[dict[str, Any]]
    ) -> Optional[date]:
        proprietary_period_start = self.proprietary_period_start_date(block_visits)

        if proprietary_period is None:
            return None
        # add the proprietary period to get the data release date
        return proprietary_period_start + relativedelta(months=proprietary_period)

    def is_partner_allocated(self, proposal_code: str, partner_code: str) -> bool:
        stmt = text(
            """
SELECT P.Partner_Code    AS partner_code,
       SUM(PA.TimeAlloc) AS time_allocation
FROM PriorityAlloc PA
         JOIN MultiPartner MP ON PA.MultiPartner_Id = MP.MultiPartner_Id
         JOIN ProposalCode PC ON MP.ProposalCode_Id = PC.ProposalCode_Id
         JOIN Semester S ON MP.Semester_Id = S.Semester_Id
         JOIN Partner P ON MP.Partner_Id = P.Partner_Id
WHERE PC.Proposal_Code = :proposal_code
GROUP BY PA.MultiPartner_Id, PA.Priority
        """
        )
        result = self.connection.execute(stmt, {"proposal_code": proposal_code})

        for row in result:
            if row.partner_code == partner_code and row.time_allocation > 0:
                return True
        return False

    def maximum_proprietary_period(self, proposal_code: str) -> int:
        proposal_type = self.get_proposal_type(proposal_code)
        if proposal_type == "Commissioning":
            return 36
        if proposal_type == "Director's Discretionary Time":
            return 6
        if proposal_type == "Engineering":
            return 0
        if proposal_type == "Gravitational Wave Event":
            return 1200
        if proposal_type == "Science Verification":
            return 12
        if proposal_type == "OPTICON-Radionet Pilot":
            return 24
        if proposal_type in [
            "Key Science Program",
            "Large Science Proposal",
            "Science",
            "Science - Long Term",
        ]:
            if self.is_partner_allocated(proposal_code, "RSA"):
                return 24
            return 1200
        raise ValueError("Unknown proposal type.")

    def update_proprietary_period(
        self, proposal_code: str, proprietary_period: int
    ) -> None:
        stmt = text(
            """
UPDATE ProposalGeneralInfo
SET ProprietaryPeriod = :proprietary_period, ReleaseDate = :release_date
WHERE ProposalCode_Id = (SELECT PC.ProposalCode_Id
                         FROM ProposalCode PC
                         WHERE PC.Proposal_Code = :proposal_code)
    """
        )
        block_visits = self._block_visits(proposal_code)
        self.connection.execute(
            stmt,
            {
                "proposal_code": proposal_code,
                "release_date": self._data_release_date(
                    proprietary_period, block_visits
                ),
                "proprietary_period": proprietary_period,
            },
        )

    def _get_phase_one_targets(self, proposal_code: str) -> List[Dict[str, Any]]:
        # The phase 1 targets.
        stmt = text(
            """
SELECT DISTINCT RequestedTime                                   AS observing_time,
                T.Target_Id                                     AS id,
                T.Target_Name                                   AS name,
                TC.RaH                                          AS ra_h,
                TC.RaM                                          AS ra_m,
                TC.RaS                                          AS ra_s,
                TC.DecSign                                      AS dec_sign,
                TC.DecD                                         AS dec_d,
                TC.DecM                                         AS dec_m,
                TC.DecS                                         AS dec_s,
                TC.Equinox                                      AS equinox,
                TM.MinMag                                       AS min_mag,
                TM.MaxMag                                       AS max_mag,
                BP.FilterName                                   AS bandpass,
                TST.TargetSubType                               AS target_sub_type,
                TT.TargetType                                   AS target_type,
                PPT.Optional									AS optional,
                PPT.NVisits										AS requested_observations,
                PPT.MaxLunarPhase								AS max_luner_phase,
                PR.Ranking										AS ranking,
                PPT.TrackCount									AS track_count,
                PPT.NightCount									AS nights_count,
                M.Moon											AS moon,
                PTP.CompetitionProbability						AS competition_probability,
                PTP.ObservabilityProbability					AS observability_probability,
                PTP.SeeingProbability							AS seeing_probability,
                PTP.TotalProbability							AS total_probability,
                MT.RaDot                                        AS ra_dot,
                MT.DecDot                                       AS dec_dot,
                MT.Epoch                                        AS epoch,
                PT.Period                                       AS period,
                PT.Pdot                                         AS period_change_rate,
                PT.T0                                           AS period_zero_point,
                TB.Time_Base                                    AS period_time_base,
                HT.Identifier                                   AS horizons_identifier,
                IF((MT1.Target_Id IS NOT NULL
                    OR MTF.Target_Id IS NOT NULL
                    OR HT.Identifier IS NOT NULL),
                    1,
                    0)                                          AS non_sidereal
FROM P1ProposalTarget PPT
    JOIN ProposalCode  PC ON PPT.ProposalCode_Id = PC.ProposalCode_Id
    JOIN Target T ON PPT.Target_Id = T.Target_Id
    JOIN TargetCoordinates TC ON T.TargetCoordinates_Id = TC.TargetCoordinates_Id
    JOIN P1ObservingConditions POC ON PC.ProposalCode_Id = POC.ProposalCode_Id
     LEFT JOIN TargetMagnitudes TM ON T.TargetMagnitudes_Id = TM.TargetMagnitudes_Id
     LEFT JOIN Bandpass BP ON TM.Bandpass_Id = BP.Bandpass_Id
         LEFT JOIN TargetSubType TST ON T.TargetSubType_Id = TST.TargetSubType_Id
         LEFT JOIN TargetType TT ON TST.TargetType_Id = TT.TargetType_Id
         LEFT JOIN MovingTarget MT ON T.MovingTarget_Id = MT.MovingTarget_Id
         LEFT JOIN PeriodicTarget PT ON T.PeriodicTarget_Id = PT.PeriodicTarget_Id
         LEFT JOIN TimeBase TB ON PT.TimeBase_Id = TB.TimeBase_Id
         LEFT JOIN HorizonsTarget HT ON T.HorizonsTarget_Id = HT.HorizonsTarget_Id
         LEFT JOIN MovingTable MT1 ON T.Target_Id = MT1.Target_Id
         LEFT JOIN MovingTableFile MTF ON T.Target_Id = MTF.Target_Id
         LEFT JOIN PiRanking PR ON PPT.PiRanking_Id = PR.PiRanking_Id
         LEFT JOIN Moon M ON POC.Moon_Id = M.Moon_Id
         LEFT JOIN P1TargetProbabilities PTP ON PC.ProposalCode_Id = PTP.ProposalCode_Id
WHERE Proposal_Code = :proposal_code
    """
        )
        return [
            {
                "id": row.id,
                "name": row.name,
                "observing_time": row.observing_time,
                "coordinates": target_coordinates(row),
                "proper_motion": target_proper_motion(row),
                "magnitude": target_magnitude(row),
                "target_type": target_type(row),
                "is_optional": row.optional,
                "requested_observations": row.requested_observations,
                "max_lunar_phase": row.max_luner_phase,
                "ranking": row.ranking,
                "track_count": row.track_count,
                "night_count": row.nights_count,
                "observing_probabilities": {
                    "moon": row.moon,
                    "competition": row.competition_probability,
                    "observability": row.observability_probability,
                    "seeing": row.seeing_probability,
                    "total": row.total_probability,
                },
                "period_ephemeris": target_period_ephemeris(row),
                "horizons_identifier": row.horizons_identifier,
                "non_sidereal": row.non_sidereal == 1,
            }
            for row in self.connection.execute(stmt, {"proposal_code": proposal_code})
        ]

    def _get_requested_times(self, proposal_code: str) -> List[Dict[str, Any]]:
        stmt = text(
            """
SELECT
    MP.ReqTimePercent					AS percentage,
    PMT.P1MinimumUsefulTime				AS minimum_useful_time,
    MP.ReqTimeAmount					AS total_requested_time,
    PMT.P1TimeComment					AS `comment`,
    P.Partner_Name						AS partner_name,
    CONCAT(S.`Year`, '-', S.Semester)   AS semester
FROM MultiPartner MP
    JOIN ProposalCode PC ON MP.ProposalCode_Id = PC.ProposalCode_Id
    JOIN Semester S ON MP.Semester_Id = S.Semester_Id
    JOIN Partner P ON MP.Partner_Id = P.Partner_Id
    JOIN P1MinTime PMT ON MP.ProposalCode_Id = PMT.ProposalCode_Id AND MP.Semester_Id = PMT.Semester_Id
WHERE Proposal_Code = :proposal_code
        """
        )

        req_time: DefaultDict[str, Dict[str, Any]] = defaultdict(lambda: dict())
        for row in self.connection.execute(stmt, {"proposal_code": proposal_code}):
            semester = row.semester
            if not req_time[semester]:
                req_time[semester] = {
                    "total_requested_time": row.total_requested_time,
                    "minimum_useful_time": row.minimum_useful_time,
                    "comment": row.comment,
                    "semester": semester,
                    "distribution": [],
                }
            req_time[semester]["distribution"].append(
                {"partner": row.partner_name, "percentage": row.percentage}
            )

        return list(req_time.values())

    def _get_nir_simulations(self, proposal_code: str) -> List[Dict[str, Any]]:
        stmt = text(
            """
SELECT
    P1NirSimulation_Id          AS id,
    P1NirSimulation_Name		AS `name`,
    PiComment					AS description
FROM P1NirSimulation P1NS
    JOIN ProposalCode PC ON	P1NS.ProposalCode_Id = PC.ProposalCode_Id
WHERE Proposal_Code = :proposal_code
        """
        )
        simulations = []
        for row in self.connection.execute(stmt, {"proposal_code": proposal_code}):
            simulations.append(
                {
                    "name": row.name,
                    "url": f"/instrument-simulations/nir/{row.id}.nsim",
                    "description": row.description,
                }
            )
        return simulations

    def _get_hrs_simulations(self, proposal_code: str) -> List[Dict[str, Any]]:
        stmt = text(
            """
SELECT
    P1HrsSimulation_Id          AS id,
    P1HrsSimulation_Name		AS `name`,
    PiComment					AS description
FROM P1HrsSimulation P1HS
    JOIN ProposalCode PC ON	P1HS.ProposalCode_Id = PC.ProposalCode_Id
WHERE Proposal_Code = :proposal_code
        """
        )
        simulations = []
        for row in self.connection.execute(stmt, {"proposal_code": proposal_code}):
            simulations.append(
                {
                    "name": row.name,
                    "url": f"/instrument-simulations/hrs/{row.id}.hsim",
                    "description": row.description,
                }
            )
        return simulations

    def _get_rss_simulations(self, proposal_code: str) -> List[Dict[str, Any]]:
        stmt = text(
            """
SELECT
    P1RssSimulation_Id          AS id,
    P1RssSimulation_Name		AS `name`,
    PiComment					AS description
FROM P1RssSimulation P1RS
    JOIN ProposalCode PC ON	P1RS.ProposalCode_Id = PC.ProposalCode_Id
WHERE Proposal_Code = :proposal_code
        """
        )
        simulations = []
        for row in self.connection.execute(stmt, {"proposal_code": proposal_code}):
            simulations.append(
                {
                    "name": row.name,
                    "url": f"/instrument-simulations/rss/{row.id}.rsim",
                    "description": row.description,
                }
            )
        return simulations

    def _get_salticam_simulations(self, proposal_code: str) -> List[Dict[str, Any]]:
        stmt = text(
            """
SELECT
    P1SalticamSimulation_Id         AS id,
    P1SalticamSimulation_Name		AS `name`,
    PiComment					    AS description
FROM P1SalticamSimulation P1SS
    JOIN ProposalCode PC ON	P1SS.ProposalCode_Id = PC.ProposalCode_Id
WHERE Proposal_Code = :proposal_code
        """
        )
        simulations = []
        for row in self.connection.execute(stmt, {"proposal_code": proposal_code}):
            simulations.append(
                {
                    "name": row.name,
                    "url": f"/instrument-simulations/salticam/{row.id}.ssim",
                    "description": row.description,
                }
            )
        return simulations

    def _get_science_configurations(self, proposal_code: str) -> List[Dict[str, Any]]:
        stmt = text(
            """
SELECT
    P1C.P1Bvit_Id				        AS bvit,
    P1C.P1Hrs_Id				        AS hrs,
    P1C.P1Nir_Id				        AS nir,
    P1C.P1Rss_Id				        AS rss,
    P1C.P1Salticam_Id			        AS scam,
    BF.BvitFilter_Name			        AS bvit_filter,
    HM.ExposureMode				        AS hrs_mode,
    NG.Grating					        AS nir_grating,
    RM.`Mode`					        AS rss_mode,
    SM.DetectorMode				        AS scam_detector_mode
FROM P1Config P1C
    JOIN ProposalCode PC ON P1C.ProposalCode_Id = PC.ProposalCode_Id
    LEFT JOIN P1Bvit PB ON P1C.P1Bvit_Id = PB.P1Bvit_Id
    LEFT JOIN BvitFilter BF ON PB.BvitFilter_Id = BF.BvitFilter_Id
    LEFT JOIN P1Hrs PH ON P1C.P1Hrs_Id = PH.P1Hrs_Id
    LEFT JOIN HrsMode HM ON PH.HrsMode_Id = HM.HrsMode_Id
    LEFT JOIN P1Nir PN ON P1C.P1Nir_Id = PN.P1Nir_Id
    LEFT JOIN NirGrating NG ON PN.NirGrating_Id = NG.NirGrating_Id
    LEFT JOIN P1Rss PR ON P1C.P1Rss_Id = PR.P1Rss_Id
    LEFT JOIN RssMode RM ON PR.RssMode_Id = RM.RssMode_Id
    LEFT JOIN P1Salticam PS ON P1C.P1Salticam_Id = PS.P1Salticam_Id
    LEFT JOIN SalticamDetectorMode SM ON PS.SalticamDetectorMode_Id = SM.SalticamDetectorMode_Id
WHERE PC.Proposal_Code = :proposal_code
        """
        )
        configurations = []

        for row in self.connection.execute(stmt, {"proposal_code": proposal_code}):
            if row.bvit:
                instrument = "BVIT"
                mode = row.bvit_filter
                simulations = []  # There are no BVIT simulations
            elif row.hrs:
                instrument = "HRS"
                mode = normalised_hrs_mode(row.hrs_mode)
                simulations = self._get_hrs_simulations(proposal_code)
            elif row.nir:
                instrument = "NIR"
                mode = row.nir_grating
                simulations = self._get_nir_simulations(proposal_code)
            elif row.rss:
                instrument = "RSS"
                mode = row.rss_mode
                simulations = self._get_rss_simulations(proposal_code)
            elif row.scam:
                instrument = "SALTICAM"
                mode = row.scam_detector_mode
                simulations = self._get_salticam_simulations(proposal_code)
            else:
                raise NotFoundError(
                    "Unknown instrument configuration found for proposal:"
                    f" {proposal_code}"
                )
            configurations.append(
                {"instrument": instrument, "mode": mode, "simulations": simulations}
            )
        if len(configurations) == 0:
            return []
        return configurations

    def _get_proposal_code_id(self, proposal_code: str):
        stmt = text(
            """
SELECT ProposalCode_Id FROM ProposalCode 
WHERE Proposal_Code = :proposal_code
        """
        )
        result = self.connection.execute(stmt, {"proposal_code": proposal_code})
        proposal_code_id = result.one_or_none()
        if not proposal_code_id:
            raise NotFoundError(f"Couldn't found  proposal code `{proposal_code}`")

        return cast(int, proposal_code_id[0])
    def update_is_self_activatable(self, proposal_code: str, is_self_activatable: bool) -> None:
        # The id could be evaluated in the INSERT query, but this would lead to more
        # cryptic errors for a non-existing proposal code.
        proposal_code_id = self._get_proposal_code_id(proposal_code)
        stmt = text(
            """
        INSERT INTO ProposalSelfActivation (ProposalCode_Id, PiPcMayActivate)
        VALUE(
            :proposal_code_id, 
            :is_self_activatable
        )
        ON DUPLICATE KEY UPDATE PiPcMayActivate = :is_self_activatable;
        """
        )
        self.connection.execute(
            stmt, {
                "proposal_code_id": proposal_code_id,
                "is_self_activatable": 1 if is_self_activatable else 0,
            }
        )

    def get_liaison_astronomer(self, proposal_code: str) -> Dict[str, any]:
        # The id could be evaluated in the INSERT query, but this would lead to more
        # cryptic errors for a non-existing proposal code.
        proposal_code_id = self._get_proposal_code_id(proposal_code)
        stmt = text(
            """
SELECT
    I.PiptUser_Id           AS id,
    I.FirstName             AS given_name,
    I.Surname               AS family_name
FROM ProposalContact PCon
    JOIN Investigator I ON I.Investigator_Id = PCon.Astronomer_Id
    JOIN ProposalCode PC ON PC.ProposalCode_Id = PCon.ProposalCode_Id
WHERE PCon.ProposalCode_Id = :proposal_code_id
        """
        )
        result = self.connection.execute(
            stmt, {
                "proposal_code_id": proposal_code_id,
            }
        )
        sa = result.one_or_none()
        if not sa:
            raise NotFoundError(f"No liaison astronomer for proposal code `{proposal_code}`")
        return {
            "id": sa.id,
            "family_name": sa.family_name,
            "given_name": sa.given_name,
        }

    def update_liaison_astronomer(self, proposal_code: str, liaison_astronomer_id: Optional[int]) -> None:
        # The ids could be retrieved within the SQL statement, but then a wrong proposal code or liaison id
        # would lead to more cryptic errors.
        investigator_id = self.get_investigator_id(user_id=liaison_astronomer_id) if liaison_astronomer_id else None
        proposal_code_id = self._get_proposal_code_id(proposal_code)

        stmt = text(
            """
UPDATE ProposalContact
SET Astronomer_Id = :liaison_astronomer_id
WHERE ProposalCode_Id = :proposal_code_id
        """
        )
        self.connection.execute(
            stmt, {
                "proposal_code_id": proposal_code_id,
                "liaison_astronomer_id": investigator_id,
            }
        )

    def get_investigator_id(self, user_id: int):
        stmt = text(
            """
SELECT PU.Investigator_Id FROM PiptUser PU
    JOIN SaltAstronomers SA ON PU.Investigator_Id = SA.Investigator_Id
WHERE PU.PiptUser_Id = :user_id

        """
        )
        result = self.connection.execute(
            stmt, {
                "user_id": user_id
            }
        )
        investigator_id = result.one_or_none()
        if not investigator_id:
            raise ValidationError(f"User id not found: {user_id}")

        return cast(int, investigator_id[0])
