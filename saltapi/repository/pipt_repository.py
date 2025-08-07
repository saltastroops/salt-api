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

    def format_lamp_setup(self, orders: str, lamps: str) -> str:
        """
        Given order and lamp strings like "3-1-2" and "Ne-Ar-Kr", returns a formatted setup string.

        Example:
        orders = "3-1-2"
        lamps = "Ne-Ar-Kr"
        Output: "Ar; Kr; Ne"
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

            allowed_map[key]["lamp_setups"].append(
                self.format_lamp_setup(orders, lamps)
            )

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
                    "lamp_setup": self.format_lamp_setup(orders, lamps),
                }
            )

        return preferred

    @staticmethod
    def w_obs(w_line: float) -> float:
        return w_line + 12

    def get_rss_calibration_regions(self, version: str) -> list[dict]:
        """
        Returns Fabry-Perot calibration regions.
        The returned structure depends on the version:
        - version '1': includes mode, w_min, w_max, filter, lamp, w_line, w_obs, exptime, valid
        - version '2': includes mode, w_min, w_max, filter, line_id, valid
        """

        stmt = text(
            """
            SELECT cal.RssFabryPerotCalibrationLine_Id AS line_id,
            cal.MinWavelength AS min_wavelength,
            cal.MaxWavelength AS max_wavelength,
            cal.Valid AS valid,
            mode.FabryPerot_Mode AS fp_mode,
            filter.Barcode AS filter,
            line.RssFabryPerotCalibrationLine_Id AS line_id,
            line.Wavelength AS line_wavelength,
            line.Exptime AS exp_time,
            lamp.Lamp AS lamp
            FROM RssFabryPerotCalibration AS cal
            JOIN RssFabryPerotCalibrationLine AS line ON (cal.RssFabryPerotCalibrationLine_Id=line.RssFabryPerotCalibrationLine_Id)
            JOIN RssFabryPerotMode AS mode ON (cal.RssFabryPerotMode_Id=mode.RssFabryPerotMode_Id) 
            JOIN RssFilter AS filter ON (cal.RssFilter_Id=filter.RssFilter_Id)
            JOIN Lamp AS lamp ON (line.Lamp_Id=lamp.Lamp_Id)
            ORDER BY mode.FabryPerot_Mode, cal.MinWavelength
            """
        )
        rows = self.connection.execute(stmt).fetchall()

        regions = []
        for row in rows:
            if version == "1":
                regions.append(
                    {
                        "mode": row.fp_mode,
                        "w_min": row.min_wavelength,
                        "w_max": row.max_wavelength,
                        "filter": row.filter,
                        "lamp": row.lamp,
                        "w_line": row.line_wavelength,
                        "w_obs": self.w_obs(row.line_wavelength),
                        "exptime": row.exp_time,
                        "valid": bool(row.valid),
                    }
                )
            elif version == "2":
                regions.append(
                    {
                        "mode": row.fp_mode,
                        "w_min": row.min_wavelength,
                        "w_max": row.max_wavelength,
                        "filter": row.filter,
                        "line_id": row.line_id,
                        "valid": bool(row.valid),
                    }
                )
            else:
                raise ValueError(f"Unsupported version: {version}")

        return regions

    def get_rss_calibration_lines(self) -> list[dict]:
        """
        Returns Fabry-Perot calibration lines.
        Includes line ID, lamp, line and observed wavelengths, relative intensity, and exposure time.
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
                "w_obs": self.w_obs(row.line_wavelength),
                "rel_intensity": row.rel_intensity,
                "exptime": row.exp_time,
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
                "exptime": float(row.Exptime),
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
        Returns flat-field calibration entries, including smi_barcode, grating, lamp, etc.
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
                "exptime": row.Exptime,
                "neutral_density": row.NeutralDensity,
            }
            for row in result
        ]

    def get_smi_arc_details(self) -> List[Dict[str, Any]]:
        """
        Returns arc exposure entries with full context.
        Lamp_Order
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
                "exptime": float(row.Exptime),
            }
            for row in result
        ]

    def _get_smi_arc_bible_metadata(self) -> Dict[int, Dict[str, Any]]:
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
        meta_map = self._get_smi_arc_bible_metadata()
        raw_data = self._get_smi_allowed_lamp_setups_raw()

        grouped: Dict[str, Dict[str, Any]] = {}
        keys: List[str] = []

        for arc_id, orders, lamps in raw_data:
            arc_id = int(arc_id)
            meta = meta_map.get(arc_id)
            if not meta:
                continue
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
