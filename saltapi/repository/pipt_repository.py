from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union

import pytz
from sqlalchemy import text
from sqlalchemy.engine import Connection

from saltapi.exceptions import NotFoundError
from saltapi.repository.proposal_repository import ProposalRepository
from saltapi.service.user import User
from saltapi.util import semester_of_datetime


class PiptRepository:
    def __init__(self, connection: Connection) -> None:
        self.connection = connection
        self.proposal_repository = ProposalRepository(connection)

    def get_pipt_news_for_days(self, days: int) -> List[Dict[str, Any]]:
        """
        Return a list of PIPT news entries issued within the last `days` days.
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

    def get_nir_flat_details(self) -> List[Dict[str, Any]]:
        """
        Return flat field calibration entries from NirFlatBible joined with NirGrating and Lamp.
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
                "exposure_time": row.Exptime,
                "n_groups": row.Ngroups,
                "n_ramps": row.Nramps,
                "neutral_density": row.NeutralDensity,
            }
            for row in result
        ]

    def get_exposures(self) -> List[Dict[str, Any]]:
        """
        Return exposures from arc calibration data.
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
                "exposure_time": float(row.Exptime),
                "n_groups": int(row.Ngroups),
                "neutral_density": int(row.NeutralDensity),
            }
            for row in result
        ]

    def _get_nir_arc_bible_lookup(
        self,
    ) -> Tuple[Dict[int, str], Dict[int, float], Dict[int, int]]:
        """
        Return lookup dictionaries for arc bible grating, grating angle, and art station.
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
        Return raw allowed lamp setups from grouped query.
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
        Return raw preferred lamp setups.
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

    def format_lamp_setup(self, orders: str, lamps: str) -> str:
        """
        Given order and lamp strings like "3-2-1-2" and "Ne-Ar-Xe-Kr", returns a formatted setup string.

        Example:
        orders = "3-2-1-2"
        lamps = "Ne-Ar-Xe-Kr"
        Output: "Xe; Ar and Kr; Ne"
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
        Return allowed lamp setups, grouped by grating and art station.
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

            allowed_map[key]["lamp_setups"].append(
                self.format_lamp_setup(orders, lamps)
            )

        allowed = [allowed_map[key] for key in sorted(keys)]
        return allowed

    def get_preferred_nir_lamp_setups(self) -> List[Dict[str, Any]]:
        """
        Return preferred lamp setups per grating/art_station combination.
        """
        raw_data = self._get_preferred_nir_lamp_setups_raw()
        preferred = []

        for grating, art_station, orders, lamps in raw_data:
            preferred.append(
                {
                    "grating": grating,
                    "art_station": int(art_station),
                    "lamp_setup": self.format_lamp_setup(orders, lamps),
                }
            )

        return preferred

    @staticmethod
    def _w_obs(w_line: float) -> float:
        return w_line + 12

    def get_rss_calibration_regions(self) -> list[dict]:
        """
        Return Fabry-Perot calibration regions.
        """

        stmt = text(
            """
            SELECT cal.RssFabryPerotCalibrationLine_Id AS line_id,
            cal.MinWavelength AS min_wavelength,
            cal.MaxWavelength AS max_wavelength,
            cal.Valid AS valid,
            mode.FabryPerot_Mode AS fp_mode,
            filter.Barcode AS filter,
            line.RssFabryPerotCalibrationLine_Id AS line_id
            FROM RssFabryPerotCalibration AS cal
            JOIN RssFabryPerotCalibrationLine AS line ON (cal.RssFabryPerotCalibrationLine_Id=line.RssFabryPerotCalibrationLine_Id)
            JOIN RssFabryPerotMode AS mode ON (cal.RssFabryPerotMode_Id=mode.RssFabryPerotMode_Id) 
            JOIN RssFilter AS filter ON (cal.RssFilter_Id=filter.RssFilter_Id)
            ORDER BY mode.FabryPerot_Mode, cal.MinWavelength
            """
        )
        rows = self.connection.execute(stmt).fetchall()
        return [
            {
                "mode": row.fp_mode,
                "w_min": row.min_wavelength,
                "w_max": row.max_wavelength,
                "filter": row.filter,
                "line_id": row.line_id,
                "valid": bool(row.valid),
            }
            for row in rows
        ]

    def get_rss_calibration_lines(self) -> list[dict]:
        """
        Return Fabry-Perot calibration lines.
        """

        stmt = text(
            """
            SELECT line.RssFabryPerotCalibrationLine_Id AS line_id,
            lamp.Lamp AS lamp,
            line.Wavelength AS line_wavelength,
            line.RelIntensity AS rel_intensity,
            line.Exptime AS exp_time
            FROM RssFabryPerotCalibrationLine AS line
            JOIN Lamp AS lamp USING (Lamp_Id)
            ORDER BY RssFabryPerotCalibrationLine_Id
            """
        )
        rows = self.connection.execute(stmt).fetchall()

        return [
            {
                "line_id": row.line_id,
                "lamp": row.lamp,
                "w_line": row.line_wavelength,
                "w_obs": self._w_obs(row.line_wavelength),
                "rel_intensity": row.rel_intensity,
                "exposure_time": row.exp_time,
            }
            for row in rows
        ]

    def get_rss_exposure_times(self) -> list[dict]:
        stmt = text(
            """
            SELECT g.Grating, ab.RssArtStation_Number, l.Lamp, ae.Exptime
            FROM ArcBible AS ab JOIN ArcExposure AS ae ON ab.ArcBible_Id=ae.ArcBible_Id
            JOIN RssGrating AS g ON ab.RssGrating_Id=g.RssGrating_Id
            JOIN Lamp AS l ON ae.Lamp_Id=l.Lamp_Id
            ORDER BY ab.ArcBible_Id 
            """
        )
        result = self.connection.execute(stmt).fetchall()
        return [
            {
                "grating": row.Grating,
                "art_station": int(row.RssArtStation_Number),
                "lamp": row.Lamp,
                "exposure_time": float(row.Exptime),
            }
            for row in result
        ]

    def get_rss_allowed_lamps(self) -> list[dict]:
        stmt = text(
            """
            SELECT ab.ArcBible_Id, g.Grating, ab.RssArtStation_Number
            FROM ArcBible AS ab JOIN RssGrating AS g ON (ab.RssGrating_Id=g.RssGrating_Id)
            ORDER BY g.Grating, ab.RssArtStation_Number
            """
        )
        bible_rows = self.connection.execute(stmt).fetchall()
        arc_bible_ids = []
        gratings = {}
        art_stations = {}
        for row in bible_rows:
            arc_bible_id = int(row.ArcBible_Id)
            arc_bible_ids.append(arc_bible_id)
            gratings[arc_bible_id] = row.Grating
            art_stations[arc_bible_id] = int(row.RssArtStation_Number)

        allowed_lamps_map = {}
        keys = []

        for arc_bible_id in arc_bible_ids:
            lamp_rows = self.connection.execute(
                text(
                    """
                    SELECT l.Lamp
                    FROM ArcExposure ae
                    JOIN Lamp l ON ae.Lamp_Id = l.Lamp_Id
                    WHERE ae.ArcBible_Id = :arc_bible_id
                    """
                ),
                {"arc_bible_id": arc_bible_id},
            ).fetchall()

            key = f"{gratings[arc_bible_id]}-{art_stations[arc_bible_id]}"
            if key not in keys:
                keys.append(key)

            if key not in allowed_lamps_map:
                allowed_lamps_map[key] = {
                    "grating": gratings[arc_bible_id],
                    "art_station": art_stations[arc_bible_id],
                    "lamps": [],
                }

            allowed_lamps_map[key]["lamps"].extend(
                [lamp_row[0] for lamp_row in lamp_rows]
            )

        keys.sort()

        allowed_lamps = [allowed_lamps_map[key] for key in keys]

        return allowed_lamps

    def get_rss_preferred_lamps(self) -> list[dict]:
        query = """
            SELECT g.Grating, ab.RssArtStation_Number, l.Lamp
            FROM ArcBible ab
            JOIN RssGrating g ON ab.RssGrating_Id = g.RssGrating_Id
            JOIN Lamp l ON ab.PreferredLamp_Id = l.Lamp_Id
            ORDER BY g.Grating, ab.RssArtStation_Number, l.Lamp
        """
        result = self.connection.execute(text(query)).fetchall()
        return [
            {"grating": row[0], "art_station": int(row[1]), "lamp": row[2]}
            for row in result
        ]

    def get_smi_flat_details(self) -> List[Dict[str, Any]]:
        """
        Return flat field calibration setup.
        """
        stmt = text(
            """
            SELECT rm.Barcode,
                rg.Grating,
                sfb.GratingAngle,
                sfb.RssArtStation_Number,
                sfb.PreBinRows,
                sfb.PreBinCols,
                l.Lamp,
                sfb.Exptime,
                sfb.NeutralDensity
            FROM SmiFlatBible sfb
            JOIN RssMask rm ON sfb.RssMask_id = rm.RssMask_Id
            JOIN RssGrating rg ON sfb.RssGrating_Id = rg.RssGrating_Id
            JOIN Lamp l ON sfb.Lamp_Id = l.Lamp_Id
            """
        )
        result = self.connection.execute(stmt)
        return [
            {
                "smi_barcode": row.Barcode,
                "grating": row.Grating,
                "grating_angle": row.GratingAngle,
                "art_station": row.RssArtStation_Number,
                "pre_bin_rows": row.PreBinRows,
                "pre_bin_cols": row.PreBinCols,
                "lamp": row.Lamp,
                "exposure_time": row.Exptime,
                "neutral_density": row.NeutralDensity,
            }
            for row in result
        ]

    def get_smi_arc_details(self) -> List[Dict[str, Any]]:
        """
        Return the arc details for Slit Mask IFU setups.
        """
        stmt = text(
            """
            SELECT rm.Barcode,
                rg.Grating,
                sab.GratingAngle,
                sab.RssArtStation_Number,
                sab.PreBinRows,
                sab.PreBinCols,
                l.Lamp,
                sae.Exptime
            FROM SmiArcBible sab
            JOIN SmiArcSetup sas ON sab.SmiArcBible_Id=sas.SmiArcBible_Id
            JOIN SmiArcExposure sae ON sas.SmiArcSetup_Id = sae.SmiArcSetup_Id
            JOIN RssMask rm ON sab.RssMask_id = rm.RssMask_Id
            JOIN RssGrating rg ON sab.RssGrating_Id = rg.RssGrating_Id
            JOIN Lamp l ON sae.Lamp_Id = l.Lamp_Id
            """
        )
        result = self.connection.execute(stmt)
        return [
            {
                "smi_barcode": row.Barcode,
                "grating": row.Grating,
                "grating_angle": row.GratingAngle,
                "art_station": row.RssArtStation_Number,
                "pre_bin_rows": row.PreBinRows,
                "pre_bin_cols": row.PreBinCols,
                "lamp": row.Lamp,
                "exposure_time": float(row.Exptime),
            }
            for row in result
        ]

    def _get_smi_arc_bible_setup(self) -> Dict[int, Dict[str, Any]]:
        """
        Lookup metadata for each arc bible ID (used for joining in other queries).
        """
        stmt = text(
            """
            SELECT ab.SmiArcBible_Id, 
                rm.Barcode, 
                g.Grating, 
                ab.GratingAngle, 
                ab.RssArtStation_Number, 
                ab.PreBinRows, 
                ab.PreBinCols 
            FROM SmiArcBible AS ab JOIN RssGrating AS g ON (ab.RssGrating_Id=g.RssGrating_Id)
            JOIN RssMask AS rm ON (ab.RssMask_Id=rm.RssMask_Id)
            ORDER BY g.Grating, ab.RssArtStation_Number
            """
        )
        result = self.connection.execute(stmt)
        return {
            int(row.SmiArcBible_Id): {
                "smi_barcode": row.Barcode,
                "grating": row.Grating,
                "grating_angle": row.GratingAngle,
                "art_station": int(row.RssArtStation_Number),
                "pre_bin_rows": int(row.PreBinRows),
                "pre_bin_cols": int(row.PreBinCols),
            }
            for row in result
        }

    def _get_smi_allowed_lamp_setups_raw(self) -> List[Tuple[int, str, str]]:
        stmt = text(
            """
            SELECT sas.SmiArcBible_Id,
                GROUP_CONCAT(sae.`Order` SEPARATOR '-') AS Lamp_Order,
                GROUP_CONCAT(l.Lamp SEPARATOR '-') AS Lamps
            FROM SmiArcSetup sas
            JOIN SmiArcExposure sae ON sas.SmiArcSetup_Id = sae.SmiArcSetup_Id
            JOIN Lamp l ON sae.Lamp_Id = l.Lamp_Id
            GROUP BY sae.SmiArcSetup_Id, sas.SmiArcBible_Id
            """
        )
        return list(self.connection.execute(stmt))

    def _get_smi_preferred_lamp_setups_raw(
        self,
    ) -> List[Tuple[str, str, float, int, int, int, str, str]]:
        stmt = text(
            """
            SELECT rm.Barcode,
                rg.Grating,
                sab.GratingAngle,
                sab.RssArtStation_Number,
                sab.PreBinRows,
                sab.PreBinCols, 
                GROUP_CONCAT(sae.`Order` SEPARATOR '-') AS Lamp_Order,
                GROUP_CONCAT(l.Lamp SEPARATOR '-')
            FROM SmiArcBible sab
            JOIN SmiArcSetup sas ON sab.PreferredArcSetup_Id = sas.SmiArcSetup_Id
            JOIN SmiArcExposure sae ON sas.SmiArcSetup_Id = sae.SmiArcSetup_Id
            JOIN RssMask rm ON sab.RssMask_id = rm.RssMask_Id
            JOIN RssGrating rg ON sab.RssGrating_Id = rg.RssGrating_Id
            JOIN Lamp l ON sae.Lamp_Id = l.Lamp_Id
            GROUP BY sas.SmiArcSetup_Id, sab.SmiArcBible_Id
            """
        )
        return list(self.connection.execute(stmt))

    def get_smi_allowed_lamp_setups(self) -> List[Dict[str, Any]]:
        """Return allowed arc lamp setups grouped by grating, art station number, pre-bin rows, and pre-bin columns."""
        meta_map = self._get_smi_arc_bible_setup()
        raw_data = self._get_smi_allowed_lamp_setups_raw()

        grouped: Dict[str, Dict[str, Any]] = {}
        keys: List[str] = []

        for arc_id, orders, lamps in raw_data:
            arc_id = int(arc_id)
            meta = meta_map.get(arc_id)
            if not meta:
                raise NotFoundError(f"Arc ID {arc_id} not found in metadata map.")
            key = f"{meta['grating']}-{meta['art_station']}-{meta['pre_bin_rows']}-{meta['pre_bin_cols']}"

            if key not in grouped:
                grouped[key] = {
                    **meta,
                    "lamp_setups": [],
                }
                keys.append(key)

            grouped[key]["lamp_setups"].append(self.format_lamp_setup(orders, lamps))

        return [grouped[k] for k in sorted(keys)]

    def get_smi_preferred_lamp_setups(self) -> List[Dict[str, Any]]:
        """Return the preferred arc setups for the RSS Slit Mask IFU."""
        raw_data = self._get_smi_preferred_lamp_setups_raw()
        result = []

        for row in raw_data:
            (
                smi_barcode,
                grating,
                grating_angle,
                art_station,
                pre_bin_rows,
                pre_bin_cols,
                orders,
                lamps,
            ) = row
            result.append(
                {
                    "smi_barcode": smi_barcode,
                    "grating": grating,
                    "grating_angle": grating_angle,
                    "art_station": int(art_station),
                    "pre_bin_rows": int(pre_bin_rows),
                    "pre_bin_cols": int(pre_bin_cols),
                    "lamp_setup": self.format_lamp_setup(orders, lamps),
                }
            )

        return result

    def _current_semester(self) -> Dict[str, Any]:
        semester_str = semester_of_datetime(datetime.now(pytz.utc))
        year, sem = map(int, semester_str.split("-"))
        return self._get_semester_by_year_and_semester(year, sem)

    def _get_semester_by_year_and_semester(
        self, year: int, semester: int
    ) -> Dict[str, Any]:
        """Fetch semester details by year and semester."""
        query = text(
            """
            SELECT Semester_Id, Year, Semester, UNIX_TIMESTAMP(StartSemester) AS start_unix,
                   UNIX_TIMESTAMP(EndSemester) AS end_unix
            FROM Semester
            WHERE Year = :year AND Semester = :semester
            LIMIT 1
        """
        )
        result = self.connection.execute(query, {"year": year, "semester": semester})
        row = result.fetchone()
        if not row:
            raise NotFoundError(f"No semester found for {year} and {semester}.")
        return {
            "semester_id": row.Semester_Id,
            "year": row.Year,
            "semester": row.Semester,
            "start_unix": row.start_unix,
            "end_unix": row.end_unix,
        }

    def get_previous_proposals_info(
        self,
        user_id: int,
        from_semester: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        current = self._current_semester()

        # Default is 3 semesters ago
        if from_semester is None:
            if current["semester"] == 1:
                from_semester = f"{current['year']-2}-2"
            else:
                from_semester = f"{current['year']-1}-1"

        # Handles whether the starting semester is 1 or 2
        from_year, from_sem = map(int, from_semester.split("-"))
        if from_sem == 1:
            semester_condition = f"s.Year >= {from_year}"
        else:
            semester_condition = (
                f"((s.Year={from_year} AND s.Semester=2) OR s.Year >= {from_year + 1})"
            )

        # Allocated time & title
        stmt = text(
            f"""
            SELECT Proposal_Code AS proposal_code, Title AS title, SUM(TimeAlloc) AS allocated_time
            FROM ProposalCode 
            JOIN ProposalText AS pt ON ProposalCode.ProposalCode_Id = pt.ProposalCode_Id
            JOIN MultiPartner ON ProposalCode.ProposalCode_Id=MultiPartner.ProposalCode_Id
            JOIN PriorityAlloc USING (MultiPartner_Id)
            WHERE MultiPartner.Semester_Id = pt.Semester_Id
            AND Priority < 4
            AND Proposal_Code IN (
                SELECT DISTINCT pco.Proposal_Code FROM ProposalCode AS pco JOIN Proposal AS p USING (ProposalCode_Id)
                JOIN ProposalContact AS pc ON pco.ProposalCode_Id = pc.ProposalCode_Id
                JOIN Investigator AS i ON (pc.Leader_Id = i.Investigator_Id) JOIN PiptUser AS pu USING (PiptUser_Id)
                JOIN Semester AS s ON p.Semester_id = s.Semester_Id
                WHERE pu.PiptUser_Id = :user_id AND p.Current = 1 AND p.Phase = 2
                AND {semester_condition}
            )
        GROUP BY Proposal_Code
        """
        )
        result = self.connection.execute(stmt, {"user_id": user_id})
        allocated_times = {}
        titles = {}
        for row in result:
            allocated_times[row.proposal_code] = row.allocated_time
            titles[row.proposal_code] = row.title

        # Observed time
        sql_observed = text(
            f"""
            SELECT Proposal_Code AS proposal_code, SUM(Obstime) AS observed_time
            FROM Proposal
            JOIN ProposalCode USING (ProposalCode_Id)
            JOIN Block USING (Proposal_Id)
            JOIN BlockVisit USING (Block_Id)
            JOIN BlockVisitStatus USING (BlockVisitStatus_Id)
            WHERE BlockVisitStatus = 'Accepted'
              AND Priority < 4
              AND Proposal_Code IN (
                    SELECT DISTINCT pco.Proposal_Code FROM ProposalCode AS pco JOIN Proposal AS p ON pco.ProposalCode_Id = p.ProposalCode_Id
                    JOIN ProposalContact AS pc ON p.ProposalCode_Id = pc.ProposalCode_Id
                    JOIN Investigator AS i ON (pc.Leader_Id = i.Investigator_Id) JOIN PiptUser AS pu USING (PiptUser_Id)
                    JOIN Semester AS s ON p.Semester_id = s.Semester_Id
                    WHERE pu.PiptUser_Id = :user_id AND p.Current = 1 AND p.Phase = 2
                    AND {semester_condition}
              )
            GROUP BY Proposal_Code
        """
        )
        result = self.connection.execute(sql_observed, {"user_id": user_id})
        observed_times = {row.proposal_code: row.observed_time for row in result}

        # Publications
        sql_publications = text(
            f"""
            SELECT DISTINCT Proposal_Code AS proposal_code, Bibcode AS bibcode
            FROM Publication AS pp
            JOIN ProposalCode ON pp.ProposalCode_Id = ProposalCode.ProposalCode_Id
            JOIN Proposal ON ProposalCode.ProposalCode_Id = Proposal.ProposalCode_Id
            WHERE Proposal_Code IN (
                SELECT DISTINCT pco.Proposal_Code
                FROM ProposalCode AS pco
                JOIN Proposal AS p ON pco.ProposalCode_Id = p.ProposalCode_Id
                JOIN ProposalContact AS pc ON p.ProposalCode_Id = pc.ProposalCode_Id
                JOIN Investigator AS i ON pc.Leader_Id = i.Investigator_Id
                JOIN PiptUser AS pu USING (PiptUser_Id)
                JOIN Semester AS s ON p.Semester_id = s.Semester_Id
                WHERE pu.PiptUser_Id = :user_id AND p.Current = 1 AND p.Phase = 2 AND pp.Valid = 1
                  AND {semester_condition}
            )
        """
        )
        result = self.connection.execute(sql_publications, {"user_id": user_id})
        bibcodes = {}
        for row in result:
            if row.proposal_code not in bibcodes:
                bibcodes[row.proposal_code] = []
            bibcodes[row.proposal_code].append(row.bibcode)

        previous_proposals = []
        for proposal_code in allocated_times.keys():
            previous_proposals.append(
                {
                    "proposal_code": proposal_code,
                    "title": titles.get(proposal_code, ""),
                    "allocated_time": allocated_times[proposal_code],
                    "observed_time": observed_times.get(proposal_code, 0),
                    "publications": bibcodes.get(proposal_code, []),
                }
            )

        return previous_proposals

    def get_block_visits(self, proposal_code: str) -> List[Dict[str, Any]]:
        """Get block visit records for a given proposal code."""

        query = """
            SELECT DISTINCT bv.BlockVisit_Id,
                bc.BlockCode AS BlockCode,
                b.Block_Name AS BlockName,
                bvs.BlockVisitStatus AS BlockVisitStatus,
                b.Priority AS Priority,
                m.Moon AS Moon,
                b.ObsTime AS ObservedTime,
                b.OverheadTime AS OverheadTime,
                pool.PoolCode AS PoolCode,
                s.Year AS Year,
                s.Semester AS Semester
            FROM BlockVisit AS bv
            JOIN BlockVisitStatus AS bvs ON (bv.BlockVisitStatus_Id=bvs.BlockVisitStatus_Id)
            JOIN Block AS b ON (bv.Block_Id=b.Block_Id)
            JOIN Moon AS m ON (b.Moon_Id=m.Moon_Id)
            JOIN Proposal AS p ON (b.Proposal_Id=p.Proposal_Id)
            JOIN ProposalCode AS pc ON (p.ProposalCode_Id=pc.ProposalCode_Id)
            JOIN Semester AS s ON (p.Semester_Id=s.Semester_Id)
            LEFT JOIN BlockCode AS bc ON (b.BlockCode_Id=bc.BlockCode_Id)
            LEFT JOIN BlockPool AS bp ON (b.Block_Id=bp.Block_Id)
            LEFT JOIN Pool AS pool ON (bp.Pool_Id=pool.Pool_Id)
            WHERE pc.Proposal_Code = :proposal_code
        """

        result = self.connection.execute(text(query), {"proposal_code": proposal_code})
        block_visits = []

        for row in result:
            moon = row.Moon
            if moon in ["Dark-Gray", "Bright-Gray"]:
                moon = "Gray"
            block_visits.append(
                {
                    "block_code": row.BlockCode,
                    "block_name": row.BlockName,
                    "block_visit_status": row.BlockVisitStatus,
                    "priority": row.Priority,
                    "moon": moon,
                    "total_time": row.ObservedTime,
                    "overhead_time": row.OverheadTime,
                    "pool_code": row.PoolCode,
                    "semester": f"{row.Year}-{row.Semester}",
                }
            )

        return block_visits

    def _get_proposal_query(self) -> str:
        return """
            SELECT Proposal.Proposal_Id,
                Proposal.ProposalCode_Id,
                ProposalCode.Proposal_Code,
                Proposal.Current,
                Proposal.Semester_Id,
                Proposal.TotalReqTime,
                Proposal.Phase,
                Proposal.Submission,
                UNIX_TIMESTAMP(Proposal.SubmissionDate) AS submission_timestamp,
                Proposal.OverheadTime,
                PULead.Username AS leader_username,
                PUCont.Username AS contact_username
            FROM Proposal
            JOIN ProposalContact ON Proposal.ProposalCode_Id = ProposalContact.ProposalCode_Id
            JOIN ProposalCode ON Proposal.ProposalCode_Id = ProposalCode.ProposalCode_Id
            JOIN ProposalGeneralInfo ON Proposal.ProposalCode_Id = ProposalGeneralInfo.ProposalCode_Id
            JOIN ProposalStatus ON ProposalGeneralInfo.ProposalStatus_Id = ProposalStatus.ProposalStatus_Id
            JOIN Semester ON Proposal.Semester_Id = Semester.Semester_Id
            JOIN Investigator ILead ON ILead.Investigator_Id = ProposalContact.Leader_Id
            JOIN Investigator ICont ON ICont.Investigator_Id = ProposalContact.Contact_Id
            JOIN PiptUser PULead ON PULead.PiptUser_Id = ILead.PiptUser_Id
            JOIN PiptUser PUCont ON PUCont.PiptUser_Id = ICont.PiptUser_Id
        """

    def get_proposals(
        self,
        user: User,
        phase: Optional[int] = None,
        limit: int = 250,
        descending: bool = False,
    ) -> List[Dict[str, Any]]:
        """
        Fetch proposals with optional filters for phase and proposal_code.
        """

        where_clauses = []
        params: Dict[str, Any] = {}

        username = user.username
        can_edit_all = "Administrator" in user.roles
        can_see_all = can_edit_all or "Astronomer" in user.roles

        if phase == 1:
            where_clauses.append(
                "ProposalStatus.Status != :deleted AND Proposal.Phase = 1"
            )
            params["deleted"] = "Deleted"
        elif phase == 2:
            where_clauses.append(
                "(ProposalStatus.Status = :accepted AND Proposal.Phase= 1) OR"
                " (Proposal.Current = 1 AND Proposal.Phase = 2)"
            )
            params["accepted"] = "Accepted"

        sql = self._get_proposal_query()

        if not can_see_all:
            sql += """
            JOIN ProposalInvestigator ON Proposal.ProposalCode_Id = ProposalInvestigator.ProposalCode_Id
            JOIN Investigator I ON ProposalInvestigator.Investigator_Id = I.Investigator_Id
            JOIN PiptUser PU ON I.Investigator_Id = PU.Investigator_Id
            """
            where_clauses.append("PU.Username = :username")
            params["username"] = username

        where_clause = (
            " AND ".join(f"({wc})" for wc in where_clauses) if where_clauses else ""
        )
        if where_clause:
            sql += f" WHERE {where_clause}"

        order_by = f"Proposal.Proposal_Id {'DESC' if descending else 'ASC'}"
        sql += f" ORDER BY {order_by} LIMIT {limit}"

        result = self.connection.execute(text(sql), params)
        proposals = [dict(row) for row in result.mappings()]

        pi_sql = """
            SELECT DISTINCT p.Proposal_Id AS proposal_id, i.Surname AS surname
            FROM Investigator AS i
            JOIN ProposalContact AS pc ON i.Investigator_Id = pc.Leader_Id
            JOIN Proposal AS p ON pc.ProposalCode_Id = p.ProposalCode_Id
        """
        pi_result = self.connection.execute(text(pi_sql))
        principal_investigator = {
            row.proposal_id: row.surname for row in pi_result.mappings()
        }

        # Build final proposal list, remove duplicates by Proposal_Code
        proposals_list = []
        seen_codes = set()

        for proposal in proposals:
            code = proposal["Proposal_Code"]
            if code in seen_codes:
                continue
            seen_codes.add(code)

            full_proposal = self.proposal_repository.get(code)
            editable = can_edit_all or username in [
                proposal["leader_username"],
                proposal["contact_username"],
            ]
            proposals_list.append(
                {
                    "proposal_id": proposal["Proposal_Id"],
                    "proposal_code": code,
                    "title": full_proposal["general_info"]["title"],
                    "principal_investigator": principal_investigator.get(
                        proposal["Proposal_Id"]
                    ),
                    "semester": full_proposal["semester"],
                    "editable": editable,
                    "proposal_file": full_proposal["proposal_file"],
                }
            )
        return proposals_list

    def get_partners(self):
        """
        Return the partner details.

        For every partner the name and the list of institutes are included. The list is
        sorted by partner name, and for each partner the institutes are sorted by
        institute name and department.

        Returns
        -------
        The partner details.
        """
        sql = """
SELECT P.Partner_Code           AS partner_code,
       P.Partner_Name           AS partner_name,
       IName.InstituteName_Name AS institute_name,
       I.Department             AS department
FROM Partner P
         JOIN Institute I ON P.Partner_Id = I.Partner_Id
         JOIN InstituteName IName ON I.InstituteName_Id = IName.InstituteName_Id
ORDER BY P.Partner_Code, IName.InstituteName_Name, I.Department
        """
        result = self.connection.execute(text(sql))

        # Collect the results by partner in a dictionary
        partners_dict = {}
        for row in result:
            partner_code = row.partner_code
            if partner_code not in partners_dict:
                partners_dict[partner_code] = {
                    "name": row.partner_name,
                    "institutes": [],
                }
            department = row.department
            if department is not None:
                department = department.strip()
            if department == "":
                department = None
            partners_dict[partner_code]["institutes"].append(
                {"name": row.institute_name, "department": department}
            )

        # Turn the dictionary into a list and sort the result. The institutes are
        # sorted already as they were returned sorted by the SQL query.
        partners = sorted(partners_dict.values(), key=lambda v: v["name"])
        return partners
