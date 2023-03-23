import { Component, Input } from "@angular/core";

import { ProposalService } from "../../../../../service/proposal.service";

@Component({
  selector: "wm-self-activate",
  templateUrl: "./self-activate.component.html",
  styleUrls: ["./self-activate.component.scss"],
})
export class SelfActivateComponent {
  @Input() isSelfActivatable!: boolean;
  @Input() proposalCode!: string;
  loading = false;
  updateMessage: string | null = null;
  isUpdated = false;
  constructor(private proposalService: ProposalService) {}

  changeSelfActivatable(): void {
    this.updateMessage = null;
    this.loading = true;
    this.proposalService
      .updateSelfActivatable(this.proposalCode, !this.isSelfActivatable)
      .subscribe(
        () => {
          this.loading = false;
          this.isUpdated = true;
          this.updateMessage = "Updated successfully!";
          this.isSelfActivatable = !this.isSelfActivatable;
        },
        () => {
          this.loading = false;
          this.isUpdated = false;
          this.updateMessage = "Failed to update!";
        },
      );

    setTimeout(() => {
      if (this.isUpdated) {
        this.updateMessage = null;
      }
    }, 3000);
  }
}
