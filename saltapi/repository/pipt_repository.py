from typing import Any, Dict, List, Tuple

from sqlalchemy import text
from sqlalchemy.engine import Connection


class PiptRepository:
    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def get_pipt_news_for_days(self, days: int) -> List[Dict[str, Any]]:
        """
        Returns a list of PIPT news entries issued within the last `days` days.
        """
        stmt = text(
            """
            SELECT Time AS time, Title AS title, Text AS text
            FROM PiptNews
            WHERE DATE_SUB(CURDATE(), INTERVAL :days DAY) <= Time
            ORDER BY Time DESC
            """
        )

        result = self.connection.execute(stmt, {"days": days})
        news_items = [
            {
                "date": row.time,
                "title": row.title,
                "text": row.text,
            }
            for row in result
        ]
        return news_items

    def get_proposal_constraints(
        self, proposal_code: str, year: int | None = None, semester: int | None = None
    ) -> List[Dict[str, Any]]:
        constraints: List[Dict[str, Any]] = []

        stmt = text(
            """
SELECT s.Year AS year,
       s.Semester AS semester,
       pa.Priority AS priority,
       m.Moon AS moon,
       SUM(pa.TimeAlloc) AS allocated_time
FROM ProposalCode AS pc
    JOIN ProposalGeneralInfo AS pgi ON pc.ProposalCode_Id = pgi.ProposalCode_Id
    JOIN MultiPartner AS mp ON pc.ProposalCode_Id = mp.ProposalCode_Id
    JOIN PriorityAlloc AS pa ON pa.MultiPartner_Id = mp.MultiPartner_Id
    JOIN Semester AS s ON mp.Semester_Id = s.Semester_Id
    JOIN Moon AS m ON pa.Moon_Id = m.Moon_Id
WHERE pc.Proposal_Code = :proposal_code
  {year_filter}
  {semester_filter}
GROUP BY s.Semester_Id, pa.Moon_Id, pa.Priority
HAVING SUM(pa.TimeAlloc) > 0
            """.format(
                year_filter="AND s.Year = :year" if year is not None else "",
                semester_filter="AND s.Semester = :semester"
                if semester is not None
                else "",
            )
        )

        params = {"proposal_code": proposal_code}
        if year is not None:
            params["year"] = year
        if semester is not None:
            params["semester"] = semester

        result = self.connection.execute(stmt, params)
        rows = result.fetchall()

        for row in rows:
            constraints.append(
                {
                    "year": row.year,
                    "semester": row.semester,
                    "priority": row.priority,
                    "moon": row.moon,
                    "allocated_time": row.allocated_time,
                }
            )
        return constraints

    def get_nir_flat_checksum(self) -> int:
        """
        Returns the checksum of the NirFlatBible table.
        """
        stmt = text("CHECKSUM TABLE NirFlatBible")
        result = self.connection.execute(stmt).first()
        return int(result.Checksum)

    def get_nir_flat_details(self) -> List[Dict[str, Any]]:
        """
        Returns flat-field calibration entries from NirFlatBible joined with NirGrating and Lamp.
        """
        stmt = text(
            """
            SELECT ng.Grating, nfb.GratingAngle, nfb.NirArtStation_Number, l.Lamp, nfb.Exptime, nfb.Ngroups, nfb.Nramps, nfb.NeutralDensity
            FROM NirFlatBible nfb
            JOIN NirGrating ng ON nfb.NirGrating_Id = ng.NirGrating_Id
            JOIN Lamp l ON nfb.Lamp_Id = l.Lamp_Id;
        """
        )
        result = self.connection.execute(stmt)
        return [
            {
                "grating": row.Grating,
                "grating_angle": row.GratingAngle,
                "art_station": row.NirArtStation_Number,
                "lamp": row.Lamp,
                "exptime": row.Exptime,
                "n_groups": row.Ngroups,
                "n_ramps": row.Nramps,
                "neutral_density": row.NeutralDensity,
            }
            for row in result
        ]

    def get_nir_arc_checksum(self) -> int:
        """
        Returns the combined checksum of NirArcBible, NirArcSetup, and NirArcExposure tables.
        """
        tables = ["NirArcBible", "NirArcSetup", "NirArcExposure"]
        total = 0
        for table in tables:
            stmt = text(f"CHECKSUM TABLE {table}")
            result = self.connection.execute(stmt).fetchone()
            if result is None:
                raise RuntimeError(
                    f"Unexpected: CHECKSUM TABLE {table} returned no rows"
                )
            total += int(result[1])
        return total

    def get_exposures(self) -> List[Dict[str, Any]]:
        """
        Returns exposures from arc calibration data.
        """
        stmt = text(
            """
            SELECT ng.Grating, nab.GratingAngle, nab.NirArtStation_Number, l.Lamp, nae.Exptime, nae.Ngroups, nae.NeutralDensity
            FROM NirArcBible nab
            JOIN NirArcSetup nas ON nab.NirArcBible_Id = nas.NirArcBible_Id
            JOIN NirArcExposure nae ON nas.NirArcSetup_Id = nae.NirArcSetup_Id
            JOIN NirGrating ng ON nab.NirGrating_Id = ng.NirGrating_Id
            JOIN Lamp l ON nae.Lamp_Id = l.Lamp_Id
        """
        )
        result = self.connection.execute(stmt)
        return [
            {
                "grating": row.Grating,
                "grating_angle": row.GratingAngle,
                "art_station": int(row.NirArtStation_Number),
                "lamp": row.Lamp,
                "exptime": float(row.Exptime),
                "n_groups": int(row.Ngroups),
                "neutral_density": int(row.NeutralDensity),
            }
            for row in result
        ]

    def _get_nir_arc_bible_lookup(
        self,
    ) -> Tuple[Dict[int, str], Dict[int, float], Dict[int, int]]:
        """
        Returns lookup dictionaries for arc bible grating, grating angle, and art station.
        """
        stmt = text(
            """
            SELECT ab.NirArcBible_Id, g.Grating, ab.GratingAngle, ab.NirArtStation_Number
            FROM NirArcBible AS ab 
            JOIN NirGrating AS g ON (ab.NirGrating_Id=g.NirGrating_Id)
            ORDER BY g.Grating, ab.NirArtStation_Number
        """
        )
        result = self.connection.execute(stmt)
        gratings = {}
        grating_angles = {}
        art_stations = {}
        for row in result:
            arc_bible_id = int(row.NirArcBible_Id)
            gratings[arc_bible_id] = row.Grating
            grating_angles[arc_bible_id] = row.GratingAngle
            art_stations[arc_bible_id] = int(row.NirArtStation_Number)
        return gratings, grating_angles, art_stations

    def _get_allowed_nir_lamp_setups_raw(self) -> List[Tuple[int, str, str]]:
        """
        Returns raw allowed lamp setups from grouped query.
        """
        stmt = text(
            """
            SELECT nas.NirArcBible_Id,
                GROUP_CONCAT(nae.`Order` SEPARATOR '-') AS Lamp_Order,
                GROUP_CONCAT(l.Lamp SEPARATOR '-') AS Lamps
            FROM NirArcSetup nas
            JOIN NirArcExposure nae ON nas.NirArcSetup_Id = nae.NirArcSetup_Id
            JOIN Lamp l ON nae.Lamp_Id = l.Lamp_Id
            GROUP BY nae.NirArcSetup_Id, nas.NirArcBible_Id
            """
        )
        return list(self.connection.execute(stmt))

    def _get_preferred_nir_lamp_setups_raw(self) -> List[Tuple[str, int, str, str]]:
        """
        Returns raw preferred lamp setups.
        """
        stmt = text(
            """
            SELECT ng.Grating, nab.NirArtStation_Number,
                   GROUP_CONCAT(nae.`Order` SEPARATOR '-') AS Lamp_Order,
                   GROUP_CONCAT(l.Lamp SEPARATOR '-') AS Lamps
            FROM NirArcBible nab
            JOIN NirArcSetup nas ON nab.PreferredArcSetup_Id = nas.NirArcSetup_Id
            JOIN NirArcExposure nae ON nas.NirArcSetup_Id = nae.NirArcSetup_Id
            JOIN NirGrating ng ON nab.NirGrating_Id = ng.NirGrating_Id
            JOIN Lamp l ON nae.Lamp_Id = l.Lamp_Id
            GROUP BY nas.NirArcSetup_Id, nab.NirArcBible_Id
        """
        )
        return list(self.connection.execute(stmt))

    def _nir_lamp_setup(self, orders: str, lamps: str) -> str:
        """
        Given order and lamp strings like "3-1-2" and "Ne-Ar-Kr", return a formatted setup string.
        """
        orders_array = [int(order_str) for order_str in orders.split("-")]
        lamps_array = lamps.split("-")

        ordered_lamps = {}
        for order, lamp in zip(orders_array, lamps_array):
            ordered_lamps.setdefault(order, []).append(lamp)

        setup_parts = []
        for i in sorted(ordered_lamps.keys()):
            lamps_in_order = sorted(ordered_lamps[i])
            setup_parts.append(" and ".join(lamps_in_order))

        return "; ".join(setup_parts)

    def get_allowed_nir_lamp_setups(self) -> List[Dict[str, Any]]:
        """
        Returns allowed lamp setups, grouped by grating and art station.
        """
        gratings, grating_angles, art_stations = self._get_nir_arc_bible_lookup()
        raw_data = self._get_allowed_nir_lamp_setups_raw()

        allowed_map: Dict[str, Dict[str, Any]] = {}
        keys: List[str] = []

        for arc_bible_id, orders, lamps in raw_data:
            arc_bible_id = int(arc_bible_id)
            key = f"{gratings[arc_bible_id]}-{art_stations[arc_bible_id]}"

            if key not in keys:
                keys.append(key)

            if key not in allowed_map:
                allowed_map[key] = {
                    "grating": gratings[arc_bible_id],
                    "grating_angle": grating_angles[arc_bible_id],
                    "art_station": art_stations[arc_bible_id],
                    "lamp_setups": [],
                }

            allowed_map[key]["lamp_setups"].append(self._nir_lamp_setup(orders, lamps))

        allowed = [allowed_map[key] for key in sorted(keys)]
        return allowed

    def get_preferred_nir_lamp_setups(self) -> List[Dict[str, Any]]:
        """
        Returns preferred lamp setups per grating/art_station combination.
        """
        raw_data = self._get_preferred_nir_lamp_setups_raw()
        preferred = []

        for grating, art_station, orders, lamps in raw_data:
            preferred.append(
                {
                    "grating": grating,
                    "art_station": int(art_station),
                    "lamp_setup": self._nir_lamp_setup(orders, lamps),
                }
            )

        return preferred
