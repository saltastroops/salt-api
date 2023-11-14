import { Component, Input, OnInit } from "@angular/core";

import { AuthenticationService } from "../../../../service/authentication.service";
import { Proposal, ProposalStatusValue } from "../../../../types/proposal";
import { UserRole } from "../../../../types/user";
import { hasAnyRole } from "../../../../utils";

@Component({
  selector: "wm-p1-details-table",
  templateUrl: "./p1-details-table.component.html",
  styleUrls: ["./p1-details-table.component.scss"],
})
export class P1DetailsTableComponent implements OnInit {
  @Input() proposal!: Proposal;

  isAdminOrSa = false;

  constructor(private authService: AuthenticationService) {}
  ngOnInit(): void {
    this.authService.user().subscribe(
      (user) => {
        if (user) {
          this.isAdminOrSa = hasAnyRole(user, [
            "SALT Astronomer",
            "Administrator",
          ] as UserRole[]);
        }
      },
      () => {
        this.isAdminOrSa = false;
      },
    );
  }

  updateProposalStatus(proposalStatusUpdate: ProposalStatusUpdate): void {
    this.proposal.generalInfo.status.value =
      proposalStatusUpdate.proposalStatus;
    this.proposal.generalInfo.status.comment =
      proposalStatusUpdate.proposalStatusComment;
  }
}

interface ProposalStatusUpdate {
  proposalStatus: ProposalStatusValue;
  proposalStatusComment: string | null;
}
