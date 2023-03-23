import { Component, EventEmitter, Output } from "@angular/core";
import {
  AbstractControl,
  FormBuilder,
  FormGroup,
  Validators,
} from "@angular/forms";

import { BlockService } from "../../../../service/block.service";
import { BlockStatusValue } from "../../../../types/block";
import { AutoUnsubscribe } from "../../../../utils";

@Component({
  selector: "wm-edit-block-status-modal",
  templateUrl: "./edit-block-status-modal.component.html",
  styleUrls: ["./edit-block-status-modal.component.scss"],
})
@AutoUnsubscribe()
export class EditBlockStatusModalComponent {
  @Output() blockStatusUpdate = new EventEmitter<{
    blockId: number;
    value: BlockStatusValue;
    reason: string | null;
  }>();
  blockId!: number;
  isModalActive = false;
  submissionError: string | undefined = undefined;
  loading = false;
  editBlockStatusForm!: FormGroup;

  constructor(
    private blockService: BlockService,
    private formBuilder: FormBuilder,
  ) {
    this.editBlockStatusForm = formBuilder.group({
      blockStatus: [null, Validators.required],
      statusReason: [null],
    });
  }

  // convenience getter for easy access to form fields
  get f(): { [key: string]: AbstractControl } {
    return this.editBlockStatusForm.controls;
  }

  closeModal(): void {
    this.isModalActive = false;
  }

  openModal(
    blockId: number,
    blockStatus: BlockStatusValue,
    statusReason: string | null,
  ): void {
    this.isModalActive = true;
    this.blockId = blockId;
    const statusInOptions = blockStatus == "Active" || blockStatus == "On hold";
    this.editBlockStatusForm.patchValue({
      blockStatus: statusInOptions ? blockStatus : null,
      statusReason: statusReason,
    });
    this.editBlockStatusForm.markAsUntouched({ onlySelf: true });
  }

  clearError(): void {
    this.submissionError = undefined;
  }

  submitBlockStatus(): void {
    this.editBlockStatusForm.markAllAsTouched();

    // stop here if form is invalid
    if (this.editBlockStatusForm.invalid) {
      return;
    }

    this.loading = true;

    const blockStatus = this.f.blockStatus.value;
    const statusReason = this.f.statusReason.value;

    this.blockService
      .updateBlockStatus(this.blockId, blockStatus, statusReason)
      .subscribe(
        () => {
          this.blockStatusUpdate.emit({
            blockId: this.blockId,
            value: blockStatus,
            reason: statusReason,
          });
          this.loading = false;
          this.editBlockStatusForm.reset();
          this.closeModal();
        },
        (error) => {
          this.submissionError = error.toString();
          this.loading = false;
        },
      );
  }
}
