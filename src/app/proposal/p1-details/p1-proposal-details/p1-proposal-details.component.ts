import { Component, Input } from "@angular/core";

import { Proposal } from "../../../types/proposal";

@Component({
  selector: "wm-p1-proposal-details",
  templateUrl: "./p1-proposal-details.component.html",
  styleUrls: ["./p1-proposal-details.component.scss"],
})
export class P1ProposalDetailsComponent {
  @Input() proposal!: Proposal;
}
