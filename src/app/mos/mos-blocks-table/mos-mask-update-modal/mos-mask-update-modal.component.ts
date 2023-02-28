import { Component, HostListener, Input } from "@angular/core";

import { format } from "date-fns";

import { MosService } from "../../../service/mos.service";
import { MosBlock } from "../../../types/mos";
import { AutoUnsubscribe } from "../../../utils";

@Component({
  selector: "wm-mos-mask-update-modal",
  templateUrl: "./mos-mask-update-modal.component.html",
  styleUrls: ["./mos-mask-update-modal.component.scss"],
})
@AutoUnsubscribe()
export class MosMaskUpdateModalComponent {
  @Input() selectedMosBlock!: MosBlock;
  @Input() error: {
    cutByError: string | undefined;
    cutDateError: string | undefined;
    mosBlockError: string | undefined;
  } = {
    cutByError: undefined,
    cutDateError: undefined,
    mosBlockError: undefined,
  };
  isModalActive!: boolean;
  mosBlock!: MosBlock;

  constructor(private mosService: MosService) {}

  closeModal(): void {
    this.clearErrors();
    this.isModalActive = false;
  }

  openModal(mosBlock: MosBlock): void {
    this.isModalActive = true;
    this.mosBlock = { ...mosBlock };
  }

  updateMosMaskMetadata(
    changing: "cutBy" | "cutDate" | "maskComment",
    value: string,
  ): void {
    this.error.mosBlockError = undefined;
    if (this.mosBlock) {
      this.mosBlock[changing] = value;
    }
    if (changing === "cutDate") {
      this.error.cutDateError = undefined;
    }
    if (changing === "cutBy") {
      this.error.cutByError = undefined;
    }
  }

  setCutDateToToday(): void {
    this.mosBlock.cutDate = format(new Date(), "yyyy-MM-dd");
  }

  updateMosMask(): void {
    this.clearErrors();

    if (!this.mosBlock?.cutBy && this.mosBlock?.cutDate) {
      this.error.cutByError = "Cutter name is missing.";
      return;
    }
    if (!this.mosBlock?.cutDate && this.mosBlock?.cutBy) {
      this.error.cutDateError = "Cut date is missing.";
      return;
    }
    if (
      !this.mosBlock?.cutBy &&
      !this.mosBlock?.cutDate &&
      this.mosBlock?.maskComment
    ) {
      this.error.cutByError = "Cutter name is missing.";
      this.error.cutDateError = "Cut date is missing.";
      return;
    }

    const mask = {
      barcode: this.mosBlock.barcode,
      cutDate: this.mosBlock.cutDate,
      cutBy: this.mosBlock.cutBy,
      maskComment: this.mosBlock.maskComment,
    };

    this.mosService.updateMosMask(mask).subscribe(
      (data) => {
        if (this.selectedMosBlock) {
          this.selectedMosBlock.cutDate = data.cutDate;
          this.selectedMosBlock.cutBy = data.cutBy;
          this.selectedMosBlock.maskComment = data.maskComment;
        }
        this.closeModal();
      },
      () => {
        this.error.mosBlockError = "Failed to update mask details.";
      },
    );
  }
  clearErrors(): void {
    this.error = {
      cutByError: undefined,
      cutDateError: undefined,
      mosBlockError: undefined,
    };
  }

  @HostListener("document:keyup.escape", ["$event"])
  onEscKeyPress(): void {
    if (this.isModalActive) {
      this.clearErrors();
      this.closeModal();
    }
  }
}
