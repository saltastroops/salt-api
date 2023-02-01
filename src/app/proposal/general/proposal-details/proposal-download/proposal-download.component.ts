import { Component, Input } from "@angular/core";

import { environment } from "../../../../../environments/environment";
import { Proposal } from "../../../../types/proposal";

@Component({
  selector: "wm-proposal-download",
  templateUrl: "./proposal-download.component.html",
  styleUrls: ["./proposal-download.component.scss"],
})
export class ProposalDownloadComponent {
  @Input() proposal!: Proposal;

  doesSummaryExist(): boolean {
    return this.proposal.phase1ProposalSummary !== null;
  }

  summaryDownloadLink(): string {
    return environment.apiUrl + this.proposal.phase1ProposalSummary;
  }

  zipDownloadLink(): string {
    return environment.apiUrl + "/" + this.proposal.proposalFile;
  }
}
