import { Component, Input } from "@angular/core";

import { GeneralProposalInfo } from "../../../../types/proposal";

@Component({
  selector: "wm-phase-one-proposal-details-table",
  templateUrl: "./phase-one-proposal-details-table.component.html",
  styleUrls: ["./phase-one-proposal-details-table.component.scss"],
})
export class PhaseOneProposalDetailsTableComponent {
  @Input() generalProposalInfo!: GeneralProposalInfo;
}
