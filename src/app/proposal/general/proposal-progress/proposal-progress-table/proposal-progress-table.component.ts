import { Component, Input } from "@angular/core";

import { Proposal, ProposalProgress } from "../../../../types/proposal";

@Component({
  selector: "wm-proposal-progress-table",
  templateUrl: "./proposal-progress-table.component.html",
  styleUrls: ["./proposal-progress-table.component.scss"],
})
export class ProposalProgressTableComponent {
  @Input() proposal!: Proposal;
  @Input() progressReport!: ProposalProgress;
}
