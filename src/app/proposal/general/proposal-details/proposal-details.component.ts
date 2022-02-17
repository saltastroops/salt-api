import { Component, Input } from "@angular/core";

import { GeneralProposalInfo } from "../../../types/proposal";

@Component({
  selector: "wm-proposal-details",
  templateUrl: "./proposal-details.component.html",
  styleUrls: ["./proposal-details.component.scss"],
})
export class ProposalDetailsComponent {
  @Input() generalProposalInfo!: GeneralProposalInfo;
}
