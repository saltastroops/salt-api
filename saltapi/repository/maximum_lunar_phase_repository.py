from typing import Any, Dict

from sqlalchemy import text
from sqlalchemy.engine import Connection


class LunarPhaseRepository:
    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def get_by_proposal_code(self, proposal_code: str) -> Dict[str, Any]:
        stmt = text(
            """
            SELECT t.Target_Name, p1pt.MaxLunarPhase
            FROM P1ProposalTarget AS p1pt
            JOIN Target AS t ON (p1pt.Target_Id=t.Target_Id)
            JOIN ProposalCode AS pc ON (p1pt.ProposalCode_Id=pc.ProposalCode_Id)
            JOIN ProposalGeneralInfo AS pgi ON pc.ProposalCode_Id = pgi.ProposalCode_Id
            JOIN ProposalStatus AS ps ON (pgi.ProposalStatus_Id=ps.ProposalStatus_Id)
            WHERE pc.Proposal_Code = :proposal_code
                AND ps.Status = 'Accepted'
            """
        )

        result = self.connection.execute(
            stmt, {"proposal_code": proposal_code}
        ).fetchall()

        phases = [
            {"target": row.Target_Name, "phase": float(row.MaxLunarPhase)}
            for row in result
        ]

        return {"phases": phases}
