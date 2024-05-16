import { Component, Input, OnInit } from "@angular/core";

import { Nir, NirExposureType, NirProcedureType } from "../../../types/nir";
import { PayloadConfigurationType } from "../../../types/observation";
import { secondsToHhMmSs } from "../../../util";
import { SoInstrumentConfiguration } from "../../so-page.component";

@Component({
  selector: "wm-nir-config-row",
  templateUrl: "./nir-config-row.component.html",
  styleUrls: ["./nir-config-row.component.scss"],
})
export class NirConfigRowComponent implements OnInit {
  @Input() telescopeConfiguration!: SoInstrumentConfiguration;
  nirConfig!: NirConfig;

  ngOnInit(): void {
    const nir: Nir = this.telescopeConfiguration.instrument as Nir;
    const instrumentConfig: any = {
      instrumentName: "NIR",
      configurationType: this.telescopeConfiguration.configurationType,
      grating: nir.configuration.grating,
      gratingAngle: nir.configuration.gratingAngle,
      cycles: nir.procedure.cycles,
      procedureType: nir.procedure.procedureType,
      filter: nir.configuration.filter,
      lamp: this.telescopeConfiguration.lamp,
      calibrationFilter: this.telescopeConfiguration.calibrationFilter,
      ditherSteps: [],
    };
    nir.procedure.ditherPattern.forEach((step) => {
      instrumentConfig.ditherSteps.push({
        detector: step.detector,
        exposureType: step.exposureType,
        exposureTime: step.detector.exposureTime,
        offset: step.offset,
        offsetType: step.offsetType,
        iterations: step.detector.iterations,
      });
    });
    this.nirConfig = instrumentConfig;
  }
  protected readonly secondsToHhMmSs = secondsToHhMmSs;
}

interface NirConfig {
  instrumentName: string;
  mode: string | null;
  configurationType: PayloadConfigurationType;
  exposureType: NirExposureType;
  cycles: number;
  grating: string | null;
  gratingAngle: number | null;
  filter: string | null;
  calibrationFilter: string | null;
  lamp: string | null;
  procedureType: NirProcedureType;
  ditherSteps: {
    exposureTime: number;
    exposureType: string;
    iterations: number;
    offset: { x: number; y: number };
    offsetType: string;
    stepCount: number;
  }[];
}
