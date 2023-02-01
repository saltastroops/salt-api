import { Component, EventEmitter, HostListener, Output } from "@angular/core";
import { UntypedFormBuilder } from "@angular/forms";

import { ProposalService } from "../../../../service/proposal.service";
import {
  NewProprietaryPeriod,
  ProprietaryPeriod,
} from "../../../../types/proposal";
import { AutoUnsubcribe } from "../../../../utils";

@Component({
  selector: "wm-edit-proprietary-period-modal",
  templateUrl: "./edit-proprietary-period-modal.component.html",
  styleUrls: ["./edit-proprietary-period-modal.component.scss"],
})
@AutoUnsubcribe()
export class EditProprietaryPeriodModalComponent {
  @Output() updatePeriod = new EventEmitter<number>();
  isModalActive = false;
  proprietaryPeriod!: ProprietaryPeriod;
  proposalCode!: string;
  error: string | undefined = undefined;
  motivationNeeded = false;
  constructor(
    private formBuilder: UntypedFormBuilder,
    private proposalService: ProposalService,
  ) {}

  closeModal(): void {
    this.isModalActive = false;
  }
  openModal(proprietaryPeriod: ProprietaryPeriod, proposalCode: string): void {
    this.isModalActive = true;
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
    this.checkForMotivation();
    if (!this.motivationNeeded || this.proprietaryPeriod.motivation) {
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
              window.alert("Your request has been submitted.");
            }
            this.updatePeriod.emit(data.period);
            this.closeModal();
          },
          () => {
            this.error = "Opps, Something went wrong.";
          },
        );
    } else {
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
