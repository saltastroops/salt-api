import { Component, Input, OnInit, ViewChild } from "@angular/core";

import { AuthenticationService } from "../../../../../service/authentication.service";
import { Proposal, ProposalStatusValue } from "../../../../../types/proposal";
import { UserRole } from "../../../../../types/user";
import {
  AutoUnsubscribe,
  hasAnyRole,
  isUserPrincipalContact,
  isUserPrincipalInvestigator,
} from "../../../../../utils";
import { ProposalStatusModalComponent } from "./proposal-status-modal/proposal-status-modal.component";

@Component({
  selector: "wm-proposal-status",
  templateUrl: "./proposal-status.component.html",
  styleUrls: ["./proposal-status.component.scss"],
})
@AutoUnsubscribe()
export class ProposalStatusComponent implements OnInit {
  @Input() proposal!: Proposal;
  proposalStatusModal!: any;
  @ViewChild(ProposalStatusModalComponent)
  set ProposalStatusCommentModalComponent(child: ProposalStatusModalComponent) {
    this.proposalStatusModal = child;
  }
  isAdminOrSa = false;
  isPiOrPc = false;
  selectedStatus!: ProposalStatusValue;

  constructor(private authService: AuthenticationService) {}

  ngOnInit(): void {
    this.authService.user().subscribe(
      (user) => {
        if (user) {
          this.isAdminOrSa = hasAnyRole(user, [
            "SALT Astronomer",
            "Administrator",
          ] as UserRole[]);

          this.isPiOrPc =
            isUserPrincipalInvestigator(user, this.proposal.investigators) ||
            isUserPrincipalContact(user, this.proposal.investigators);
        }
      },
      () => {
        this.isAdminOrSa = false;
        this.isPiOrPc = false;
      },
    );
    this.selectedStatus = this.proposal.generalInfo.status.value;
  }

  setStatus(newStatus: string): void {
    // Revert the selected value to initial if the update modal is closed without updating
    this.selectedStatus = newStatus as ProposalStatusValue;
  }
}
