import { Component, Input } from "@angular/core";

import { secondsToHhMmSs } from "src/app/util";

import { SoInstrumentConfiguration } from "../so-page.component";

@Component({
  selector: "wm-instrument-config-table",
  templateUrl: "./instrument-config-table.component.html",
  styleUrls: ["./instrument-config-table.component.scss"],
})
export class InstrumentConfigTableComponent {
  @Input() telescopeConfigurations!: SoInstrumentConfiguration[];

  secondsToHhMmSs = secondsToHhMmSs;
}
