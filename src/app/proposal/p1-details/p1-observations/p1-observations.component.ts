import { Component, Input } from "@angular/core";

import { Phase1Observation } from "../../../types/target";
import { degreesToDms, degreesToHms } from "../../../utils";

@Component({
  selector: "wm-p1-observations",
  templateUrl: "./p1-observations.component.html",
  styleUrls: ["./p1-observations.component.scss"],
})
export class P1ObservationsComponent {
  @Input() observations!: Phase1Observation[] | null;
  degreeToHMS = degreesToHms;
  degreesToDms = degreesToDms;
}
