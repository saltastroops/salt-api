import { Component, EventEmitter, HostListener, Output } from "@angular/core";
import {
  AbstractControl,
  FormBuilder,
  FormGroup,
  ValidationErrors,
  ValidatorFn,
  Validators,
} from "@angular/forms";

import { BlockService } from "../../../service/block.service";
import { BlockRejectionReason } from "../../../types/block";
import { BlockVisitStatus } from "../../../types/common";
import { AutoUnsubscribe } from "../../../utils";

@Component({
  selector: "wm-edit-block-visit-status-modal",
  templateUrl: "./edit-block-visit-status-modal.component.html",
  styleUrls: ["./edit-block-visit-status-modal.component.scss"],
})
@AutoUnsubscribe()
export class EditBlockVisitStatusModalComponent {
  @Output() blockVisitStatusUpdate = new EventEmitter<{
    blockVisitId: number;
    blockVisitStatus: BlockVisitStatus;
    rejectionReason: BlockRejectionReason | null;
  }>();
  blockVisitId!: number;
  isModalActive = false;
  error: string | undefined = undefined;
  loading = false;
  editBlockVisitStatusForm!: FormGroup;

  constructor(
    private blockService: BlockService,
    private formBuilder: FormBuilder,
  ) {
    this.editBlockVisitStatusForm = formBuilder.group(
      {
        blockVisitStatus: [null, Validators.required],
        rejectionReason: [null],
      },
      {
        validators: [this.rejectionReasonValidator],
      },
    );
  }

  // cross-validation to check whether a rejection reason is required
  rejectionReasonValidator: ValidatorFn = (
    control: AbstractControl,
  ): ValidationErrors | null => {
    const blockVisitStatus = control.get("blockVisitStatus");
    const rejectionReason = control.get("rejectionReason");
    return blockVisitStatus?.value === "Rejected" &&
      rejectionReason?.value === null
      ? { required: true }
      : null;
  };

  // convenience getter for easy access to form fields
  get f(): { [key: string]: AbstractControl } {
    return this.editBlockVisitStatusForm.controls;
  }

  closeModal(): void {
    this.isModalActive = false;
  }

  openModal(
    blockVisitId: number,
    blockVisitStatus: BlockVisitStatus,
    rejectionReason: BlockRejectionReason | null,
  ): void {
    this.isModalActive = true;
    this.blockVisitId = blockVisitId;
    this.error = undefined;
    this.editBlockVisitStatusForm.patchValue({
      blockVisitStatus: blockVisitStatus,
      rejectionReason: rejectionReason,
    });
    this.editBlockVisitStatusForm.markAsUntouched({ onlySelf: true });
  }

  onBlockVisitStatusSelect(blockVisitStatus: string): void {
    const status = blockVisitStatus as BlockVisitStatus;
    if (status === "Accepted") {
      this.editBlockVisitStatusForm.patchValue({
        rejectionReason: null,
      });
    }
  }

  submitBlockVisitStatus(): void {
    this.editBlockVisitStatusForm.markAllAsTouched();

    // stop here if form is invalid
    if (this.editBlockVisitStatusForm.invalid) {
      return;
    }

    this.loading = true;

    const blockVisitStatus = this.f.blockVisitStatus.value;
    const rejectionReason = this.f.rejectionReason.value;

    this.blockService
      .updateBlockVisitStatus(
        this.blockVisitId,
        blockVisitStatus,
        rejectionReason,
      )
      .subscribe(
        () => {
          this.blockVisitStatusUpdate.emit({
            blockVisitId: this.blockVisitId,
            blockVisitStatus: blockVisitStatus,
            rejectionReason: rejectionReason,
          });
          this.loading = false;
          this.editBlockVisitStatusForm.reset();
          this.closeModal();
        },
        (error) => {
          this.error = error.toString();
          this.loading = false;
        },
      );
  }

  clearError(): void {
    this.error = undefined;
  }

  @HostListener("document:keyup.escape", ["$event"])
  onEscKeyPress(): void {
    if (this.isModalActive) {
      this.closeModal();
    }
  }
}
