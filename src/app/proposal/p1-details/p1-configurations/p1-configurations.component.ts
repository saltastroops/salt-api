import { Component, Input } from "@angular/core";

import { InstrumentConfiguration } from "../../../types/proposal";

@Component({
  selector: "wm-p1-configurations",
  templateUrl: "./p1-configurations.component.html",
  styleUrls: ["./p1-configurations.component.scss"],
})
export class P1ConfigurationsComponent {
  @Input() configurations!: InstrumentConfiguration[];
}
