import { Component, Input } from "@angular/core";

import { Proposal } from "../../../types/proposal";

@Component({
  selector: "wm-proposal-details",
  templateUrl: "./proposal-details.component.html",
  styleUrls: ["./proposal-details.component.scss"],
})
export class ProposalDetailsComponent {
  @Input() proposal!: Proposal;
}
