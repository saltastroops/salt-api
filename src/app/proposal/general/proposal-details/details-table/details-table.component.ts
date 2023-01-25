import { Component, Input } from "@angular/core";

import { GeneralProposalInfo } from "../../../../types/proposal";

@Component({
  selector: "wm-details-table",
  templateUrl: "./details-table.component.html",
  styleUrls: ["./details-table.component.scss"],
})
export class DetailsTableComponent {
  @Input() generalProposalInfo!: GeneralProposalInfo;
}
