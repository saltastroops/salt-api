import { Component, Input } from "@angular/core";

import { environment } from "../../../../environments/environment";
import { ProposalService } from "../../../service/proposal.service";
import { Proposal, ProposalProgress } from "../../../types/proposal";
import {
  AutoUnsubcribe,
  GENERIC_ERROR_MESSAGE,
  currentSemester,
} from "../../../utils";

@AutoUnsubcribe()
@Component({
  selector: "wm-proposal-progress",
  templateUrl: "./proposal-progress.component.html",
  styleUrls: ["./proposal-progress.component.scss"],
})
export class ProposalProgressComponent {
  @Input() proposal!: Proposal;
  proposalProgress!: ProposalProgress;
  showForm = false;
  error: string | undefined;
  loading = false;
  apiUrl = environment.apiUrl;
  currentSemester = currentSemester();

  constructor(private proposalService: ProposalService) {}

  showProgressReportForm(): void {
    this.loading = true;
    this.proposalService
      .getProgressReport(this.proposal.proposalCode, currentSemester())
      .subscribe(
        (data) => {
          this.proposalProgress = { ...data };
          this.showForm = true;
          this.loading = false;
        },
        () => {
          this.error = GENERIC_ERROR_MESSAGE;
          this.loading = false;
        },
      );
  }

  closeForm(): void {
    this.showForm = false;
  }
}
