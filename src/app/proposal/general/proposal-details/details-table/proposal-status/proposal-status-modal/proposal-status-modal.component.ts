import {
  Component,
  EventEmitter,
  HostListener,
  Input,
  Output,
} from "@angular/core";
import { AbstractControl, FormBuilder } from "@angular/forms";

import { AuthenticationService } from "../../../../../../service/authentication.service";
import { ProposalService } from "../../../../../../service/proposal.service";
import {
  Proposal,
  ProposalStatusValue,
} from "../../../../../../types/proposal";
import { UserRole } from "../../../../../../types/user";
import {
  AutoUnsubscribe,
  hasAnyRole,
  isUserPrincipalContact,
  isUserPrincipalInvestigator,
} from "../../../../../../utils";

@Component({
  selector: "wm-proposal-status-modal",
  templateUrl: "./proposal-status-modal.component.html",
  styleUrls: ["./proposal-status-modal.component.scss"],
})
@AutoUnsubscribe()
export class ProposalStatusModalComponent {
  @Input() proposal!: Proposal;
  @Output() closeModal: EventEmitter<string> = new EventEmitter();
  isModalActive = false;
  statusComment = "";
  statusValue!: ProposalStatusValue;
  initialValue!: ProposalStatusValue;
  loading = false;
  updateMessage: string | null = null;
  isUpdated = false;
  isAdminOrSa = false;
  isPiOrPc = false;
  error = "";
  proposalStatus: ProposalStatusValue[] = [
    "Accepted",
    "Active",
    "Completed",
    "Deleted",
    "Expired",
    "In preparation",
    "Inactive",
    "Rejected",
    "Superseded",
    "Under scientific review",
    "Under technical review",
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

  openProposalStatusCommentModal(statusValue: ProposalStatusValue): void {
    this.isModalActive = true;
    this.statusValue = statusValue;
    this.initialValue = statusValue;
    this.changeProposalStatus(statusValue);
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
    if (!this.isAdminOrSa && this.isPiOrPc) {
      this.statusValue =
        statusValue === "Active" ? "Under technical review" : "Active";
    }
  }

  closeStatusModal(): void {
    if (!this.loading) {
      this.isModalActive = false;
      this.updateMessage = null;
      this.closeModal.emit(this.initialValue);
    }
  }

  submitProposalStatus(): void {
    this.loading = true;
    this.proposalService
      .submitProposalStatus(
        this.proposal.proposalCode,
        this.statusValue,
        this.proposalStatusComment.value,
      )
      .subscribe(
        (proposalStatus) => {
          this.loading = false;
          this.isUpdated = true;
          this.initialValue = proposalStatus.value;
          this.updateMessage = "Updated successfully!";
          this.proposal.generalInfo.status = proposalStatus;
          this.closeStatusModal();
        },
        () => {
          this.loading = false;
          this.isUpdated = false;
          this.updateMessage = "Failed to update!";
        },
      );
  }

  @HostListener("document:keyup.escape", ["$event"])
  onEscKeyPress(): void {
    if (this.isModalActive) {
      this.closeStatusModal();
    }
  }

  changeProposalStatus(statusValue: string): void {
    this.selectedStatus.setValue(statusValue, {
      onlySelf: true,
    });
    this.statusValue = statusValue as ProposalStatusValue;
  }
  // Access form controls getter
  get selectedStatus(): AbstractControl {
    return this.proposalStatusForm.controls.proposalStatus;
  }
  get proposalStatusComment(): AbstractControl {
    return this.proposalStatusForm.controls.proposalStatusComment;
  }
}
