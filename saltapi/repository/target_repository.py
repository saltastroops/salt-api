from typing import Any, Dict, Optional

from sqlalchemy import text
from sqlalchemy.engine import Connection

from saltapi.service.target import Target
from saltapi.util import (
    target_coordinates,
    target_magnitude,
    target_period_ephemeris,
    target_proper_motion,
    target_type,
)


class TargetRepository:
    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def get(self, target_id: int) -> Target:
        stmt = text(
            """
SELECT DISTINCT T.Target_Id                                      AS id,
                T.Target_Name                                    AS name,
                TC.RaH                                           AS ra_h,
                TC.RaM                                           AS ra_m,
                TC.RaS                                           AS ra_s,
                TC.DecSign                                       AS dec_sign,
                TC.DecD                                          AS dec_d,
                TC.DecM                                          AS dec_m,
                TC.DecS                                          AS dec_s,
                TC.Equinox                                       AS equinox,
                TM.MinMag                                        AS min_mag,
                TM.MaxMag                                        AS max_mag,
                BP.FilterName                                    AS bandpass,
                TST.TargetSubType                                AS target_sub_type,
                TT.TargetType                                    AS target_type,
                MT.RaDot                                         AS ra_dot,
                MT.DecDot                                        AS dec_dot,
                MT.Epoch                                         AS epoch,
                PT.Period                                        AS period,
                PT.Pdot                                          AS period_change_rate,
                PT.T0                                            AS period_zero_point,
                TB.Time_Base                                     AS period_time_base,
                HT.Identifier                                    AS horizons_identifier,
                IF((MT1.Target_Id IS NOT NULL
                    OR MTF.Target_Id IS NOT NULL
                    OR HT.Identifier IS NOT NULL),
                    1,
                    0)                                           AS non_sidereal
FROM Target T
         LEFT JOIN TargetCoordinates TC
                   ON T.TargetCoordinates_Id = TC.TargetCoordinates_Id
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
WHERE T.Target_Id = :target_id;
        """
        )
        result = self.connection.execute(stmt, {"target_id": target_id})
        row = result.one()

        target = {
            "id": row.id,
            "name": row.name,
            "coordinates": target_coordinates(row),
            "proper_motion": target_proper_motion(row),
            "magnitude": target_magnitude(row),
            "target_type": target_type(row),
            "period_ephemeris": target_period_ephemeris(row),
            "horizons_identifier": row.horizons_identifier,
            "non_sidereal": row.non_sidereal == 1,
        }

        return target

    @staticmethod
    def _period_ephemeris(row: Any) -> Optional[Dict[str, Any]]:
        if row.period is None:
            return None

        return {
            "zero_point": float(row.period_zero_point),
            "period": float(row.period),
            "period_change_rate": float(row.period_change_rate),
            "time_base": row.period_time_base,
        }
