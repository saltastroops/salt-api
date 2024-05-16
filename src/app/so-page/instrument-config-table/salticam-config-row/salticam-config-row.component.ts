import { Component, Input, OnInit } from "@angular/core";

import { PayloadConfigurationType } from "../../../types/observation";
import { Salticam, SalticamExposureType } from "../../../types/salticam";
import { secondsToHhMmSs } from "../../../util";
import { SoInstrumentConfiguration } from "../../so-page.component";

@Component({
  selector: "wm-salticam-config-row",
  templateUrl: "./salticam-config-row.component.html",
  styleUrls: ["./salticam-config-row.component.scss"],
})
export class SalticamConfigRowComponent implements OnInit {
  @Input() instrumentConfig!: SoInstrumentConfiguration;
  salticamConfig!: SalticamConfig;

  ngOnInit(): void {
    const scam = this.instrumentConfig.instrument as Salticam;
    this.salticamConfig = {
      binning: {
        preBinnedColumns: scam.detector.preBinnedColumns,
        preBinnedRows: scam.detector.preBinnedRows,
      },
      exposures: scam.procedure.exposures.map((e) => ({
        time: e.exposureTime,
        filter: e.filter.name,
      })),
      gain: scam.detector.gain,
      cycles: scam.procedure.cycles,
      iterations: this.instrumentConfig.iterations,
      instrumentName: this.instrumentConfig.instrumentName,
      configurationType: this.instrumentConfig.configurationType,
      exposureType: scam.detector.exposureType,
      mode: scam.detector.mode,
      lamp: this.instrumentConfig.lamp,
      calibrationFilter: this.instrumentConfig.calibrationFilter
    };
  }
  protected readonly secondsToHhMmSs = secondsToHhMmSs;
}

interface SalticamConfig {
  instrumentName: string;
  mode: string | null;
  exposures: {
    time: number;
    filter: string;
  }[];
  gain: string;
  lamp: string | null;
  calibrationFilter: string | null;
  configurationType: PayloadConfigurationType;
  exposureType: SalticamExposureType;
  iterations: number;
  cycles: number;
  binning: { preBinnedColumns: number; preBinnedRows: number };
}
