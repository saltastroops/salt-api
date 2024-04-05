import { Component, Input, OnInit } from "@angular/core";

import { AuthenticationService } from "../../service/authentication.service";
import { RealProposalService } from "../../service/real/real-proposal.service";
import { Investigator, Proposal } from "../../types/proposal";
import { User } from "../../types/user";
import { AutoUnsubscribe, hasAnyRole } from "../../utils";

@Component({
  selector: "wm-investigators",
  templateUrl: "./investigators.component.html",
  styleUrls: ["./investigators.component.scss"],
})
@AutoUnsubscribe()
export class InvestigatorsComponent implements OnInit {
  @Input() proposal!: Proposal;
  investigators!: Investigator[];
  user!: User;
  showApprovalStatusButton = false;

  constructor(
    private authService: AuthenticationService,
    private proposalService: RealProposalService,
  ) {}

  ngOnInit(): void {
    this.investigators = this.proposal.investigators;
    this.authService.getUser().subscribe((user) => {
      this.user = user;
      this.showApprovalStatusButton =
        this.investigators.some((i) => i.id === this.user.id) ||
        this.isAdministrator();
    });
  }

  isAdministrator(): boolean {
    return hasAnyRole(this.user, ["Administrator"]);
  }

  hideAcceptButton(userId: number, hasApproved: boolean | null): boolean {
    if (this.isAdministrator()) {
      return hasApproved === true;
    } else if (this.user.id === userId) {
      return hasApproved !== null;
    } else {
      return true;
    }
  }

  hideRejectButton(userId: number, hasApproved: boolean | null): boolean {
    if (this.isAdministrator()) {
      return hasApproved === false;
    } else if (this.user.id === userId) {
      return hasApproved !== null;
    } else {
      return true;
    }
  }

  submitApprovalStatus(
    event: Event,
    investigatorId: number,
    proposalCode: string,
    approve: boolean,
  ): void {
    const button = event.target as HTMLButtonElement;
    button.classList.add("is-loading");
    this.proposalService
      .updateInvestigatorProposalApprovalStatus(
        investigatorId,
        proposalCode,
        approve,
      )
      .subscribe(
        () => {
          const investigatorDetails = this.investigators.find(
            (i) => i.id === investigatorId,
          );
          if (investigatorDetails !== undefined) {
            investigatorDetails.hasApprovedProposal = approve;
          }
          button.classList.remove("is-loading");
        },
        (error) => {
          button.classList.remove("is-loading");
          window.alert(error.toString());
        },
      );
  }

}
