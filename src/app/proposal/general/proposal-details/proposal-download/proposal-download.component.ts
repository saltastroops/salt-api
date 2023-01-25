import { Component, Input } from "@angular/core";

import { GeneralProposalInfo } from "../../../../types/proposal";

@Component({
  selector: "wm-proposal-download",
  templateUrl: "./proposal-download.component.html",
  styleUrls: ["./proposal-download.component.scss"],
})
export class ProposalDownloadComponent {
  @Input() generalProposalInfo!: GeneralProposalInfo;
}
