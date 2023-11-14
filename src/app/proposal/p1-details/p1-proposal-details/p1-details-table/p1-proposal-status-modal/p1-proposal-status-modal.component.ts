import { Component, EventEmitter, Input, Output } from "@angular/core";
import { AbstractControl, FormBuilder } from "@angular/forms";

import { AuthenticationService } from "../../../../../service/authentication.service";
import { ProposalService } from "../../../../../service/proposal.service";
import { Proposal, ProposalStatusValue } from "../../../../../types/proposal";
import { UserRole } from "../../../../../types/user";
import { hasAnyRole, isUserPrincipalInvestigator } from "../../../../../utils";

@Component({
  selector: "wm-p1-proposal-status-modal",
  templateUrl: "./p1-proposal-status-modal.component.html",
  styleUrls: ["./p1-proposal-status-modal.component.scss"],
})
export class P1ProposalStatusModalComponent {
  @Input() proposal!: Proposal;
  @Output() proposalStatusUpdate = new EventEmitter<{
    proposalStatus: ProposalStatusValue;
    proposalStatusComment: string | null;
  }>();
  readonly modalTitle = "Change proposal status";
  isModalActive = false;
  error: string | undefined = undefined;
  loading = false;
  isAdminOrSa = false;
  isPi = false;
  allowedProposalStatus: ProposalStatusValue[] = [
    "Accepted",
    "Deleted",
    "Expired",
    "In preparation",
    "Rejected",
    "Superseded",
    "Under scientific review",
  ];

  proposalStatusForm = this.fb.group({
    proposalStatus: [""],
    proposalStatusComment: [""],
  });

  constructor(
    private proposalService: ProposalService,
    private authService: AuthenticationService,
    private fb: FormBuilder,
  ) {}

  get f(): { [key: string]: AbstractControl } {
    return this.proposalStatusForm.controls;
  }

  openProposalStatusCommentModal(
    statusValue: ProposalStatusValue,
    statusComment: string | null,
  ): void {
    this.authService.user().subscribe(
      (user) => {
        if (user) {
          this.isAdminOrSa = hasAnyRole(user, [
            "SALT Astronomer",
            "Administrator",
          ] as UserRole[]);

          this.isPi = isUserPrincipalInvestigator(
            user,
            this.proposal.investigators,
          );
        }
      },
      () => {
        this.isAdminOrSa = false;
        this.isPi = false;
      },
    );
    this.isModalActive = true;
    this.proposalStatusForm.patchValue({
      proposalStatus: statusValue,
      proposalStatusComment: statusComment,
    });
  }

  closeModal(): void {
    this.isModalActive = false;
    this.loading = false;
  }

  submitProposalStatus(): void {
    this.loading = true;
    this.proposalService
      .submitProposalStatus(
        this.proposal.proposalCode,
        this.f.proposalStatus.value,
        this.f.proposalStatusComment.value,
      )
      .subscribe(
        (proposalStatus) => {
          this.proposalStatusUpdate.emit({
            proposalStatus: proposalStatus.value,
            proposalStatusComment: proposalStatus.comment,
          });
          this.error = undefined;
          this.proposalStatusForm.reset();
          this.closeModal();
        },
        () => {
          this.loading = false;
          this.error = "Failed to update!";
        },
      );
  }
}
