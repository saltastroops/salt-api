from typing import Any, Dict, List

from sqlalchemy import text
from sqlalchemy.engine import Connection

from saltapi.service.instrument import NIR


class NirRepository:
    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def get(self, nir_id: int) -> NIR:
        stmt = text(
            """
SELECT N.Nir_Id                                          AS nir_id,
       N.Cycles                                          AS cycles,
       N.TotalExposureTime / 1000                        AS observation_time,
       N.OverheadTime / 1000                             AS overhead_time,
       NG.Grating                                        AS grating,
       NC.GratingAngle / 1000                            AS grating_angle,
       NAS.Location                                      AS articulation_station,
       NF.NirFilter                                      AS filter,
       NCFW.NirCameraFilterWheel                         AS camera_filter_wheel,
       NPT.NirProcedureType                              AS procedure_type
FROM Nir N
         JOIN NirConfig NC ON N.NirConfig_Id = NC.NirConfig_Id
         LEFT JOIN NirGrating NG ON NC.NirGrating_Id = NG.NirGrating_Id
         LEFT JOIN NirArtStation NAS
                   ON NC.NirArtStation_Number = NAS.NirArtStation_Number
         JOIN NirFilter NF ON NC.NirFilter_Id = NF.NirFilter_Id
         JOIN NirProcedure NP ON N.NirProcedure_Id = NP.NirProcedure_Id
         JOIN NirProcedureType NPT ON NP.NirProcedureType_Id = NPT.NirProcedureType_Id
         JOIN NirCameraFilterWheel NCFW
                   ON NC.NirCameraFilterWheel_Id = NCFW.NirCameraFilterWheel_Id
WHERE N.Nir_Id = :nir_id
ORDER BY Nir_Id DESC;
        """
        )
        results = self.connection.execute(stmt, {"nir_id": nir_id})
        row = results.fetchone()
        nir = {
            "id": row.nir_id,
            "configuration": self._configuration(row),
            "procedure": self._procedure(row),
            "observation_time": float(row.observation_time),
            "overhead_time": float(row.overhead_time),
        }
        return nir

    def _configuration(self, row: Any) -> Dict[str, Any]:
        """Return an NIR configuration."""

        camera_station, camera_angle = row.articulation_station.split("_")
        config = {
            "grating": row.grating,
            "grating_angle": float(row.grating_angle),
            "camera_station": int(camera_station),
            "camera_angle": float(camera_angle),
            "filter": row.filter,
            "camera_filter_wheel": row.camera_filter_wheel,
        }
        return config

    def _detector(self, row: Any) -> Dict[str, Any]:
        """Return an NIR detector setup."""

        detector = {
            "mode": row.detector_sampling_mode.title(),
            "ramps": row.ramps,
            "groups": row.up_the_ramp_groups,
            "reads_per_sample": row.reads_per_sample,
            "exposure_time": float(row.exposure_time),
            "iterations": row.detector_iterations,
            "exposure_type": row.exposure_type,
            "gain": row.gain,
        }

        return detector

    def _dither_steps(self, row: Any) -> List[Dict[str, Any]]:
        """Return the dither pattern steps."""

        stmt = text(
            """
SELECT NDPS.OffsetX                 AS offset_x,
       NDPS.OffsetY                 AS offset_y,
       NDOT.NirDitherOffsetType     AS offset_type,
       NS.NirSampling                                    AS detector_sampling_mode,
       ND.Ramps                                          AS ramps,
       ND.URG_Groups                                     AS up_the_ramp_groups,
       ND.ReadsPerSample                                 AS reads_per_sample,
       ND.ExposureTime                                   AS exposure_time,
       ND.Iterations                                     AS detector_iterations,
       NET.NirExposureType                               AS exposure_type,
       NG1.NirGain                                       AS gain
FROM Nir N
         JOIN NirProcedure NP
                    ON N.NirProcedure_Id = NP.NirProcedure_Id
         JOIN NirProcedureType NPT
                    ON NP.NirProcedureType_Id = NPT.NirProcedureType_Id
         JOIN NirDitherPatternStep NDPS
                    ON NP.NirDitherPattern_Id = NDPS.NirDitherPattern_Id
         LEFT JOIN NirDitherOffsetType NDOT
                    ON NDPS.NirDitherOffsetType_Id = NDOT.NirDitherOffsetType_Id
         JOIN NirDetector ND ON NDPS.NirDetector_Id = ND.NirDetector_Id
         JOIN NirExposureType NET ON NDPS.NirExposureType_Id = NET.NirExposureType_Id
         JOIN NirGain NG1 ON ND.NirGain_Id = NG1.NirGain_Id
         JOIN NirSampling NS ON ND.NirSampling_Id = NS.NirSampling_Id
WHERE N.Nir_Id = :nir_id
ORDER BY NDPS.NirDitherPattern_Order ASC
        """
        )
        results = self.connection.execute(
            stmt,
            {
                "nir_id": row.nir_id,
            },
        )

        dither_steps = [
            {
                "offset": {"x": result.offset_x / 1000, "y": result.offset_y / 1000},
                "offset_type": result.offset_type,
                "detector": self._detector(result),
                "exposure_type": result.exposure_type,
            }
            for result in results
        ]

        return dither_steps

    def _procedure_type(self, row: Any) -> str:
        """Return the procedure type."""

        procedure_types = {
            "NORMAL": "Normal",
            "FOCUS": "Focus",
        }
        return procedure_types[row.procedure_type]

    def _procedure(self, row: Any) -> Dict[str, Any]:
        """Return an NIR procedure."""

        return {
            "procedure_type": row.procedure_type,
            "cycles": row.cycles,
            "dither_pattern": self._dither_steps(row),
        }
