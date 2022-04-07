import { Component, Input, OnInit } from "@angular/core";

import { Subscription } from "rxjs";

import { MosService } from "../../service/mos.service";
import { MosBlock } from "../../types/mos";
import { AutoUnsubcribe, degreesToHms } from "../../utils";

@Component({
  selector: "wm-mos-blocks-table",
  templateUrl: "./mos-blocks-table.component.html",
  styleUrls: ["./mos-blocks-table.component.scss"],
})
@AutoUnsubcribe()
export class MosBlocksTableComponent implements OnInit {
  @Input() loading!: boolean;
  @Input() mosBlocks: MosBlock[] = [];
  @Input() requiredMosMasks!: string[];
  mosMasksInMagazine!: string[];
  degreesToHms = degreesToHms;
  selectedMosBlock!: MosBlock;
  mosBlockError: string | null = null;
  private mosMasksSubscription!: Subscription;

  constructor(private mosService: MosService) {}

  ngOnInit(): void {
    this.mosMasksSubscription = this.mosService
      .getMosMasksInMagazine()
      .subscribe(
        (data) => {
          this.mosMasksInMagazine = data;
        },
        () => {
          this.mosBlockError = "Failed to get masks in the magazine.";
        },
      );
  }

  rowColor(block: MosBlock): string {
    if (!block.cutDate && block.blockStatus === "Active") {
      return "is-cut-mask-background";
    }
    if (
      block.blockStatus === "Active" &&
      block.cutDate &&
      !this.mosMasksInMagazine.includes(block.barcode)
    ) {
      return "is-put-mask-background";
    }
    if (
      block.blockStatus === "Active" &&
      this.mosMasksInMagazine.includes(block.barcode)
    ) {
      return "is-ready-mask-background";
    }
    if (
      block.blockStatus === "Completed" &&
      this.mosMasksInMagazine.includes(block.barcode) &&
      !this.requiredMosMasks.includes(block.barcode)
    ) {
      return "is-take-mask-out-background";
    }
    return "is-no-action-mask-background";
  }

  selectMosBlock(mosBlock: MosBlock): void {
    this.selectedMosBlock = mosBlock;
  }
}
