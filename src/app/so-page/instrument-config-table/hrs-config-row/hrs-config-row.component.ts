import { Component, Input, OnInit } from "@angular/core";

import { Hrs, HrsExposureType } from "../../../types/hrs";
import { PayloadConfigurationType } from "../../../types/observation";
import { secondsToHhMmSs } from "../../../util";
import { SoInstrumentConfiguration } from "../../so-page.component";

@Component({
  selector: "wm-hrs-config-row",
  templateUrl: "./hrs-config-row.component.html",
  styleUrls: ["./hrs-config-row.component.scss"],
})
export class HrsConfigRowComponent implements OnInit {
  @Input() telescopeConfiguration!: SoInstrumentConfiguration;
  hrsConfig!: HrsConfig;
  numExposureTimes = 0;

  ngOnInit(): void {
    const hrs = this.telescopeConfiguration.instrument as Hrs;
    this.hrsConfig = {
      instrumentName: "HRS",
      configurationType: this.telescopeConfiguration.configurationType,
      calibrationFilter: this.telescopeConfiguration.calibrationFilter,
      exposureType: hrs.configuration.exposureType,
      mode: hrs.configuration.mode,
      cycles: hrs.procedure.cycles,
      blueDetector: {
        exposureTimes: hrs.procedure.blueExposureTimes,
        binning: {
          preBinnedColumns: hrs.blueDetector.preBinnedColumns,
          preBinnedRows: hrs.blueDetector.preBinnedRows,
        },
        iterations: hrs.blueDetector.iterations,
      },
      redDetector: {
        exposureTimes: hrs.procedure.redExposureTimes,
        binning: {
          preBinnedColumns: hrs.redDetector.preBinnedColumns,
          preBinnedRows: hrs.redDetector.preBinnedRows,
        },
        iterations: hrs.redDetector.iterations,
      },
    };

    this.numExposureTimes = Math.max(
      hrs.procedure.blueExposureTimes.length,
      hrs.procedure.redExposureTimes.length,
    );
  }

  protected readonly secondsToHhMmSs = secondsToHhMmSs;
}

interface HrsConfig {
  instrumentName: string;
  configurationType: PayloadConfigurationType;
  exposureType: HrsExposureType;
  cycles: number;
  mode: string;
  calibrationFilter: string | null;
  blueDetector: {
    binning: {
      preBinnedColumns: number;
      preBinnedRows: number;
    };
    iterations: number;
    exposureTimes: (number | null)[];
  };
  redDetector: {
    binning: {
      preBinnedColumns: number;
      preBinnedRows: number;
    };
    iterations: number;
    exposureTimes: (number | null)[];
  };
}
