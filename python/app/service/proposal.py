import asyncio
from typing import Any, Awaitable, Dict, Iterable, List, Optional, Union, cast

from aiomysql import DictCursor, connect
from astropy.coordinates import Angle

from app.models.general import Semester
from app.models.proposal import (
    BlockVisit,
    Institute,
    Investigator,
    ObservedTime,
    Partner,
    PartnerPercentage,
    PersonalDetails,
    Phase1Proposal,
    Phase1Target,
    Phase2Proposal,
    RequestedTime,
    TextContent,
    TimeAllocation,
)


async def get_text_content(proposal_code: str, db: connect) -> List[TextContent]:
    """
    Get the text content for a proposal.
    """
    sql = """
SELECT Title, Abstract, ReadMe, NightLogSummary, Year, Semester FROM ProposalText as pt
JOIN ProposalCode AS pc ON pt.ProposalCode_Id = pc.ProposalCode_Id
JOIN Semester AS s ON s.Semester_Id = pt.Semester_Id
WHERE Proposal_Code = %(proposal_code)s
    """
    async with db.acquire() as conn:
        async with conn.cursor(DictCursor) as cur:
            await cur.execute(
                sql,
                {
                    "proposal_code": proposal_code,
                },
            )
            rs = await cur.fetchall()
            return [
                TextContent(
                    semester=Semester(year=r["Year"], semester=r["Semester"]),
                    title=r["Title"],
                    abstract=r["Abstract"],
                    read_me=r["ReadMe"],
                    nightlog_summary=r["NightLogSummary"],
                )
                for r in rs
            ]


async def get_investigators(proposal_code: str, db: connect) -> List[Investigator]:
    """
    Get the investigators on a proposal.
    """
    sql = """
SELECT pi.Investigator_Id AS Investigator_Id, FirstName, Surname, Partner_Name,
       InstituteName_Name, Department, Url, Leader_Id, Contact_Id, Partner_Code, Email
FROM ProposalInvestigator AS pi
    JOIN ProposalCode AS pc ON pi.ProposalCode_Id = pc.ProposalCode_Id
    JOIN Investigator AS inv ON inv.Investigator_Id = pi.Investigator_Id
    JOIN Institute AS ins ON ins.Institute_Id = inv.Institute_Id
    JOIN ProposalContact AS pcon ON pcon.ProposalCode_Id = pc.ProposalCode_Id
    JOIN InstituteName AS insn ON insn.InstituteName_Id = ins.InstituteName_Id
    JOIN Partner AS p ON ins.Partner_Id = p.Partner_Id
WHERE Proposal_Code = %(proposal_code)s
    """
    async with db.acquire() as conn:
        async with conn.cursor(DictCursor) as cur:
            await cur.execute(sql, {"proposal_code": proposal_code})
            rs = await cur.fetchall()
            if rs:
                return [
                    Investigator(
                        is_pc=r["Investigator_Id"] == r["Contact_Id"],
                        is_pi=r["Investigator_Id"] == r["Leader_Id"],
                        personal_details=PersonalDetails(
                            given_name=r["FirstName"],
                            family_name=r["Surname"],
                            email=r["Email"],
                        ),
                        affiliation=Institute(
                            partner=Partner(
                                code=r["Partner_Code"], name=r["Partner_Name"]
                            ),
                            name=r["InstituteName_Name"],
                            department=r["Department"],
                            home_page=r["Url"],
                        ),
                    )
                    for r in rs
                ]
    raise ValueError(f"Investigator for {proposal_code} couldn't be found.")


async def get_time_allocations(proposal_code: str, db: connect) -> List[TimeAllocation]:
    """
    Get the time allocations for a proposal.
    """
    sql = """
SELECT Partner_Code, Partner_Name, Priority ,TimeAlloc, TacComment, Year, Semester
FROM MultiPartner AS mp
    JOIN ProposalCode AS pc ON mp.ProposalCode_Id = pc.ProposalCode_Id
    JOIN Semester AS s ON s.Semester_Id = mp.Semester_Id
    JOIN Partner AS p ON p.Partner_Id = mp.Partner_Id
    JOIN PriorityAlloc AS pa ON pa.MultiPartner_Id = mp.MultiPartner_Id
    JOIN TacProposalComment AS tc ON tc.MultiPartner_Id = mp.MultiPartner_Id
WHERE Proposal_Code = %(proposal_code)s
    """
    async with db.acquire() as conn:
        async with conn.cursor(DictCursor) as cur:
            await cur.execute(
                sql,
                {
                    "proposal_code": proposal_code,
                },
            )
            rs = await cur.fetchall()
            alloc: Dict[str, Dict[str, TimeAllocation]] = {}
            for r in rs:
                semester = f"{r['Year']}-{r['Semester']}"
                partner_code = r["Partner_Code"]
                if semester not in alloc:
                    alloc[semester] = {}
                sem_alloc = alloc[semester]
                if partner_code not in sem_alloc:
                    sem_alloc[partner_code] = TimeAllocation(
                        semester=Semester(year=r["Year"], semester=r["Semester"]),
                        partner=Partner(name=r["Partner_Name"], code=partner_code),
                        tac_comment=r["TacComment"],
                        priority_0=0,
                        priority_1=0,
                        priority_2=0,
                        priority_3=0,
                        priority_4=0,
                    )
                    priority = f"priority_{r['Priority']}"
                    setattr(sem_alloc[partner_code], priority, r["TimeAlloc"])
            return [t for v in alloc.values() for t in v.values()]


async def get_phase_1_targets(proposal_code: str, db: connect) -> List[Phase1Target]:
    """
    Get the targets defined in phase 1 of a proposal.
    """
    sql = """
SELECT Target_Name, RaH, RaM, RaS, DecSign, DecD, DecM, DecS, Equinox, MinMag, MaxMag,
    TargetType, TargetSubType, Optional, NVisits, MaxLunarPhase, Ranking, NightCount,
    MoonProbability, CompetitionProbability, ObservabilityProbability,
    SeeingProbability, Identifier
FROM P1ProposalTarget AS pt
    JOIN ProposalCode AS pc ON pt.ProposalCode_Id = pc.ProposalCode_Id
    JOIN Target AS ta ON ta.Target_Id = pt.Target_Id
    JOIN TargetCoordinates AS tc ON ta.TargetCoordinates_Id = tc.TargetCoordinates_Id
    JOIN TargetMagnitudes AS tm ON ta.TargetMagnitudes_Id = tm.TargetMagnitudes_Id
    JOIN TargetSubType AS tst ON ta.TargetSubType_Id = tst.TargetSubType_Id
    JOIN TargetType AS tt ON tst.TargetType_Id = tt.TargetType_Id
    LEFT JOIN PiRanking AS pr ON pr.PiRanking_Id = pt.PiRanking_Id
    LEFT JOIN P1TargetProbabilities AS tp ON tp.Target_Id = ta.Target_Id
    LEFT JOIN HorizonsTarget AS ht ON ht.HorizonsTarget_Id = ta.HorizonsTarget_Id
    LEFT JOIN MovingTarget AS mt ON mt.MovingTarget_Id = ta.MovingTarget_Id
WHERE Proposal_Code = %(proposal_code)s
    """
    async with db.acquire() as conn:
        async with conn.cursor(DictCursor) as cur:
            await cur.execute(sql, {"proposal_code": proposal_code})
            rs = await cur.fetchall()
            return [
                Phase1Target(
                    name=r["Target_Name"],
                    right_ascension=Angle(
                        f"{r['RaH']}:{r['RaM']}:{r['RaS']} hours"
                    ).degree,
                    declination=Angle(
                        f"{r['DecSign']}{r['DecD']}:{r['DecM']}:{r['DecS']} degrees"
                    ).degree,
                    equinox=r["Equinox"],
                    minimum_magnitude=r["MinMag"],
                    maximum_magnitude=r["MaxMag"],
                    target_type=r["TargetType"],
                    target_subtype=r["TargetSubType"],
                    is_optional=r["Optional"] == 1,
                    n_visits=r["NVisits"],
                    max_lunar_phase=r["MaxLunarPhase"],
                    ranking=r["Ranking"],
                    night_count=r["NightCount"],
                    moon_probability=r["MoonProbability"],
                    competition_probability=r["CompetitionProbability"],
                    observability_probability=r["ObservabilityProbability"],
                    seeing_probability=r["SeeingProbability"],
                    horizons_identifier=r["Identifier"],
                )
                for r in rs
            ]


async def get_block_visits(proposal_code: str, db: connect) -> List[BlockVisit]:
    """
    Get the accepted and rejected block visits of a proposal.
    """
    sql = """
SELECT BlockVisit_Id, b.Block_Id AS Block_Id, Block_Name, p.ObsTime, Priority,
       MaxLunarPhase, Target_Name, `Date`, BlockVisitStatus, RejectedReason
    FROM BlockVisit AS bv
    JOIN `Block` AS b ON b.Block_Id = bv.Block_Id
    JOIN Proposal pr ON b.Proposal_Id = pr.Proposal_Id
    JOIN Semester s ON pr.Semester_Id = s.Semester_Id
    JOIN ProposalCode AS pc ON pc.ProposalCode_Id = b.ProposalCode_Id
    JOIN NightInfo AS ni ON ni.NightInfo_Id = bv.NightInfo_Id
    JOIN Pointing AS p ON p.Block_Id = bv.Block_Id
    JOIN Observation AS o ON o.Pointing_Id = p.Pointing_Id
    JOIN Target AS t ON t.Target_Id = o.Target_Id
    LEFT JOIN BlockVisitStatus AS bvs
        ON bvs.BlockVisitStatus_Id = bv.BlockVisitStatus_Id
    LEFT JOIN BlockRejectedReason AS brr
        ON brr.BlockRejectedReason_Id = bv.BlockRejectedReason_Id
WHERE Proposal_Code = %(proposal_code)s AND BlockVisitStatus IN ('Accepted', 'Rejected')
    """
    async with db.acquire() as conn:
        async with conn.cursor(DictCursor) as cur:
            await cur.execute(sql, {"proposal_code": proposal_code})
            rs = await cur.fetchall()
            bv: Dict[int, BlockVisit] = {}
            for r in rs:
                # If a block had multiple observations (which is technically possible
                # and happens for a few rather old proposals), there will be more one
                # result for a corresponding block visit. The only difference between
                # these is the target name. To keep things simple, we only use the
                # first result. The target name thus can be any of the target names for
                # the block visit.
                block_visit_id_ = r["BlockVisit_Id"]
                bv[block_visit_id_] = BlockVisit(
                    block_visit_id=block_visit_id_,
                    block_id=r["Block_Id"],
                    block_name=r["Block_Name"],
                    observed_time=r["ObsTime"],
                    priority=r["Priority"],
                    max_lunar_phase=r["MaxLunarPhase"],
                    target_name=r["Target_Name"],
                    observation_night=r["Date"],
                    semester=Semester(year=2042, semester=2),
                    status=r["BlockVisitStatus"],
                    rejection_reason=r["RejectedReason"],
                )
            return list(bv.values())


async def _time_distribution(
    proposal_code: str, db: connect
) -> Iterable[Dict[str, Any]]:
    sql = """
SELECT Partner_Code, Partner_Name, ReqTimePercent, ReqTimeAmount, Year, Semester
FROM MultiPartner AS mp
    JOIN ProposalCode AS pc ON mp.ProposalCode_Id = pc.ProposalCode_Id
    JOIN Semester AS s ON s.Semester_Id = mp.Semester_Id
    JOIN Partner AS p ON p.Partner_Id = mp.Partner_Id
WHERE Proposal_Code = %(proposal_code)s
    """
    async with db.acquire() as conn:
        async with conn.cursor(DictCursor) as cur:
            await cur.execute(sql, {"proposal_code": proposal_code})
            results = await cur.fetchall()
            return cast(Iterable[Dict[str, Any]], results)


async def _minimum_useful_time(
    proposal_code: str, db: connect
) -> Iterable[Dict[str, Any]]:
    sql = """
SELECT P1MinimumUsefulTime, P1TimeComment, Year, Semester
FROM P1MinTime AS pmt
    JOIN ProposalCode AS pc ON pmt.ProposalCode_Id = pc.ProposalCode_Id
    JOIN Semester AS s ON s.Semester_Id = pmt.Semester_Id
WHERE Proposal_Code = %(proposal_code)s
    """
    async with db.acquire() as conn:
        async with conn.cursor(DictCursor) as cur:
            await cur.execute(sql, {"proposal_code": proposal_code})
            results = await cur.fetchall()
            return cast(Iterable[Dict[str, Any]], results)


async def get_requested_time(proposal_code: str, db: connect) -> List[RequestedTime]:
    """
    Get the time requested for a proposal.
    """
    distribution_rs, min_useful_rs = await asyncio.gather(
        asyncio.create_task(_time_distribution(proposal_code, db)),
        asyncio.create_task(_minimum_useful_time(proposal_code, db)),
    )

    requested_time: Dict[str, RequestedTime] = {}

    # The order matters: For every entry in the MultiPartner table, there should be an
    # entry in the P1MinTime table, but there may be MultiPartner table entries without
    # a corresponding P1MinTime table entry. Hence we should create the requested_time
    # dictionary from the results of the MultiPartner table query.

    for r in distribution_rs:
        _sem = f"{r['Year']}-{r['Semester']}"
        if _sem not in requested_time:
            requested_time[_sem] = RequestedTime(
                total_requested_time=r["ReqTimeAmount"],
                minimum_useful_time=None,
                comment=None,
                semester=Semester(year=r["Year"], semester=r["Semester"]),
                distribution=[],
            )
        if r["Partner_Code"] == "OTH" and r["ReqTimePercent"] > 0:
            raise ValueError("The partner 'Other' should not have a time share.")
        if r["Partner_Code"] != "OTH":
            requested_time[_sem].distribution.append(
                PartnerPercentage(
                    partner=Partner(code=r["Partner_Code"], name=r["Partner_Name"]),
                    percentage=r["ReqTimePercent"],
                )
            )

    for r in min_useful_rs:
        _sem = f"{r['Year']}-{r['Semester']}"
        requested_time[_sem].minimum_useful_time = r["P1MinimumUsefulTime"]
        requested_time[_sem].comment = r["P1TimeComment"]

    return [requested_time[r] for r in requested_time]


async def get_observed_time(proposal_code: str, db: connect) -> List[ObservedTime]:
    sql = """
SELECT SUM(ObsTime) AS ObsTime, Priority, Year, Semester
FROM BlockVisit AS bv
    JOIN `Block` AS b ON bv.Block_Id = b.Block_Id
    JOIN ProposalCode AS pc ON pc.ProposalCode_Id = b.ProposalCode_Id
    JOIN Proposal AS p ON p.Proposal_Id = b.Proposal_Id
    JOIN Semester AS s ON s.Semester_Id = p.Semester_Id
    JOIN BlockVisitStatus AS bvs ON bvs.BlockVisitStatus_Id = bv.BlockVisitStatus_Id
WHERE Proposal_Code = %(proposal_code)s
    AND BlockVisitStatus = 'Accepted'
GROUP BY Priority, s.Semester_Id
    """
    async with db.acquire() as conn:
        async with conn.cursor(DictCursor) as cur:
            await cur.execute(
                sql,
                {
                    "proposal_code": proposal_code,
                },
            )
            rs = await cur.fetchall()
            ot: Dict[str, ObservedTime] = {}
            for r in rs:
                semester = f"{r['Year']-r['Semester']}"
                if semester not in ot:
                    ot[semester] = ObservedTime(
                        semester=Semester(year=r["Year"], semester=r["Semester"]),
                        priority_0=0,
                        priority_1=0,
                        priority_2=0,
                        priority_3=0,
                        priority_4=0,
                    )
                priority = f"priority_{r['Priority']}"
                setattr(ot[semester], priority, r["ObsTime"])
            return list(ot.values())


async def get_phase(proposal_code: str, db: connect) -> int:
    """
    Get the proposal phase of a proposal's latest submission.
    """
    sql = """
SELECT Phase
FROM Proposal p
JOIN ProposalCode pc ON p.ProposalCode_Id = pc.ProposalCode_Id
WHERE Proposal_Code=%(proposal_code)s AND Current=1
ORDER BY Proposal_Id DESC
LIMIT 1
    """
    async with db.acquire() as conn:
        async with conn.cursor(DictCursor) as cur:
            await cur.execute(sql, {"proposal_code": proposal_code})
            r = await cur.fetchone()
            return cast(int, r["Phase"])


async def _phase_1_proposal(proposal_code: str, db: connect) -> Phase1Proposal:
    queries = [
        get_text_content(proposal_code, db),
        get_investigators(proposal_code, db),
        get_phase_1_targets(proposal_code, db),
        get_requested_time(proposal_code, db),
    ]
    content = await asyncio.gather(
        *[asyncio.create_task(cast(Awaitable[Any], q)) for q in queries]
    )
    return Phase1Proposal(
        phase=1,
        text_content=content[0],
        investigators=content[1],
        targets=content[2],
        requested_time=content[3],
    )


async def _phase_2_proposal(proposal_code: str, db: connect) -> Phase2Proposal:
    queries = [
        get_text_content(proposal_code, db),
        get_investigators(proposal_code, db),
        get_block_visits(proposal_code, db),
        get_observed_time(proposal_code, db),
        get_time_allocations(proposal_code, db),
    ]
    content = await asyncio.gather(
        *[asyncio.create_task(cast(Awaitable[Any], q)) for q in queries]
    )
    return Phase2Proposal(
        phase=2,
        text_content=content[0],
        investigators=content[1],
        block_visits=content[2],
        observed_time=content[3],
        time_allocations=content[4],
    )


async def get_proposal(
    proposal_code: str, db: connect, phase: Optional[int] = None
) -> Union[Phase1Proposal, Phase2Proposal]:
    """
    Return the proposal content for a phase 1 or 2 proposal.

    If a phase is given, the content for that phase is returned. Otherwise the content
    is returned for the phase of the proposal's latest submission.
    """
    if phase is None:
        phase = await get_phase(proposal_code, db)
    if phase == 1:
        return await _phase_1_proposal(proposal_code, db)
    elif phase == 2:
        return await _phase_2_proposal(proposal_code, db)
    else:
        raise ValueError(f"Unsupported proposal phase: {phase}")
