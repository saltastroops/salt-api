import { Component, EventEmitter, HostListener, Output } from "@angular/core";
import { UntypedFormBuilder } from "@angular/forms";

import { ProposalService } from "../../../../service/proposal.service";
import {
  NewProprietaryPeriod,
  ProprietaryPeriod,
} from "../../../../types/proposal";
import { AutoUnsubscribe } from "../../../../utils";

@Component({
  selector: "wm-edit-proprietary-period-modal",
  templateUrl: "./edit-proprietary-period-modal.component.html",
  styleUrls: ["./edit-proprietary-period-modal.component.scss"],
})
@AutoUnsubscribe()
export class EditProprietaryPeriodModalComponent {
  readonly modalTitle = "Edit proprietary period";
  @Output() updatePeriod = new EventEmitter<number>();
  isModalActive = false;
  loading = false;
  proprietaryPeriod: ProprietaryPeriod = {
    period: 0,
    maximumPeriod: 0,
    startDate: "",
    motivation: null,
  };
  proposalCode!: string;
  error: string | undefined = undefined;
  motivationNeeded = false;
  userMessage: string | undefined = undefined;

  constructor(
    private formBuilder: UntypedFormBuilder,
    private proposalService: ProposalService,
  ) {}

  closeModal(): void {
    this.loading = false;
    this.isModalActive = false;
  }
  openModal(proprietaryPeriod: ProprietaryPeriod, proposalCode: string): void {
    this.isModalActive = true;
    this.loading = false;
    this.error = undefined;
    this.userMessage = undefined;
    this.proprietaryPeriod = proprietaryPeriod;
    this.proposalCode = proposalCode;
    this.checkForMotivation();
  }
  updateProprietaryPeriod(proprietaryPeriodValue: string): void {
    if (Number(proprietaryPeriodValue)) {
      this.proprietaryPeriod["period"] = Number(proprietaryPeriodValue);
      this.error = undefined;
    } else {
      this.error = "The proprietary period must be a number of months.";
    }
  }
  updateMotivation(motivation: string): void {
    this.proprietaryPeriod["motivation"] = motivation;
  }
  submitProprietaryPeriod(): void {
    this.userMessage = undefined;
    this.error = undefined;
    this.checkForMotivation();
    if (!this.motivationNeeded || this.proprietaryPeriod.motivation) {
      this.loading = true;
      this.proposalService
        .submitProprietaryPeriod(
          this.proposalCode,
          this.proprietaryPeriod.period,
          this.proprietaryPeriod.motivation,
        )
        .subscribe(
          (data: NewProprietaryPeriod) => {
            this.proprietaryPeriod = {
              ...data,
            };
            if (data.status == "Pending") {
              this.userMessage = "Your request has been submitted."
            }
            this.updatePeriod.emit(data.period);

            if (!this.userMessage){
              this.closeModal();
            }
            this.loading = false;
          },
          () => {
            this.loading = false;
            this.error = "Opps, Something went wrong. " +
              "Contact SALT Help for assistance.";
          },
        );
    } else {
      this.loading = false;
      this.error = "The motivation is needed.";
    }
  }

  checkForMotivation(): void {
    this.motivationNeeded =
      this.proprietaryPeriod.period > this.proprietaryPeriod.maximumPeriod;
  }

  @HostListener("document:keyup.escape", ["$event"])
  onEscKeyPress(): void {
    if (this.isModalActive) {
      this.closeModal();
    }
  }
}
