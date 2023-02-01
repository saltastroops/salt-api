import { Component, Input } from "@angular/core";

import { P1ScienceConfiguration } from "../../../types/proposal";

@Component({
  selector: "wm-p1-configurations",
  templateUrl: "./p1-configurations.component.html",
  styleUrls: ["./p1-configurations.component.scss"],
})
export class P1ConfigurationsComponent {
  @Input() scienceConfigurations!: P1ScienceConfiguration[];
}
