import { Component, Input } from "@angular/core";

import { GeneralProposalInfo } from "../../../types/proposal";

@Component({
  selector: "wm-phase-one-proposal-details",
  templateUrl: "./phase-one-proposal-details.component.html",
  styleUrls: ["./phase-one-proposal-details.component.scss"],
})
export class PhaseOneProposalDetailsComponent {
  @Input() generalProposalInfo!: GeneralProposalInfo;
}