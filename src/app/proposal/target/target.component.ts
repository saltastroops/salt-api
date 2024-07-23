import { Component, Input } from "@angular/core";

import { Target } from "../../types/target";
import { degreesToDms, degreesToHms } from "../../utils";

@Component({
  selector: "wm-target",
  templateUrl: "./target.component.html",
  styleUrls: ["./target.component.scss"],
})
export class TargetComponent {
  @Input() target!: Target;

  rightAscension = (): string => {
    return !this.target.nonSidereal
      ? degreesToHms(this.target.coordinates?.rightAscension as number, 2)
      : "N/A";
  };

  declination = (): string => {
    if (!this.target.nonSidereal) {
      return degreesToDms(this.target.coordinates?.declination as number, 2);
    } else if (this.target.horizonsIdentifier) {
      return "N/A (" + this.target.horizonsIdentifier + ")";
    } else {
      return "N/A (Non-sidereal)";
    }
  };
}
