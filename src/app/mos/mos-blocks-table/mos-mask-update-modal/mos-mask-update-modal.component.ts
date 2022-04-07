import { Component, HostListener, Input } from "@angular/core";

import { format } from "date-fns";
import { Subscription } from "rxjs";

import { MosService } from "../../../service/mos.service";
import { MosBlock } from "../../../types/mos";
import { AutoUnsubcribe } from "../../../utils";

@Component({
  selector: "wm-mos-mask-update-modal",
  templateUrl: "./mos-mask-update-modal.component.html",
  styleUrls: ["./mos-mask-update-modal.component.scss"],
})
@AutoUnsubcribe()
export class MosMaskUpdateModalComponent {
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
  _mosBlock!: MosBlock;
  private updateMosMaskSubscription!: Subscription;

  constructor(private mosService: MosService) {}

  closeModal(): void {
    this.clearErrors();
    this.isModalActive = false;
  }

  openModal(mosBlock: MosBlock): void {
    this.isModalActive = true;
    this._mosBlock = mosBlock;
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
    this.mosBlock!.cutDate = format(new Date(), "yyyy-MM-dd");
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
      barcode: this.mosBlock!.barcode,
      cutDate: this.mosBlock!.cutDate,
      cutBy: this.mosBlock!.cutBy,
      maskComment: this.mosBlock!.maskComment,
    };

    this.updateMosMaskSubscription = this.mosService
      .updateMosMask(mask)
      .subscribe(
        (data) => {
          if (this._mosBlock) {
            this._mosBlock.cutDate = data.cutDate;
            this._mosBlock.cutBy = data.cutBy;
            this._mosBlock.maskComment = data.maskComment;
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
