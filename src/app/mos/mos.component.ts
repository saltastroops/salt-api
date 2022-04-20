import { Component, ElementRef, OnInit, ViewChild } from "@angular/core";

import { Subscription } from "rxjs";

import { MosService } from "../service/mos.service";
import { MosBlock } from "../types/mos";
import {
  AutoUnsubcribe,
  availableSemesters,
  convertRightAscensionHMSToDegrees,
  currentSemester,
  nextSemesterOf,
  previousSemesterOf,
} from "../utils";

@Component({
  selector: "wm-mos",
  templateUrl: "./mos.component.html",
  styleUrls: ["./mos.component.scss"],
})
@AutoUnsubcribe()
export class MosComponent implements OnInit {
  @ViewChild("raMinimum") raMinimumEl!: ElementRef;
  @ViewChild("raMaximum") raMaximumEl!: ElementRef;
  @ViewChild("proposalCode") proposalCodeEl!: ElementRef;
  @ViewChild("barcode") barcodeEl!: ElementRef;
  @ViewChild("piSurname") piSurnameEl!: ElementRef;
  mosBlocks!: MosBlock[];
  displayedMosBlocks!: MosBlock[];
  selectedSemester: string =
    sessionStorage.getItem("mosSelectedSemester") || currentSemester();
  availableSemesters: string[] = availableSemesters();
  requiredMosMasks: string[] = [];
  loading = true;
  error: string | undefined;
  cuttingPower = "19.1";
  searchedOnProposalCode: string | null = null;
  searchedOnPiSurname: string | null = null;
  searchedOnBarcode: string | null = null;
  isIncludeNextSemester = false;
  isIncludePreviousSemester = false;
  raMinError: string | undefined;
  raMaxError: string | undefined;
  loadError: string | undefined;
  private mosBlocksSubscription!: Subscription;

  constructor(private mosService: MosService) {}

  ngOnInit(): void {
    this.isIncludeNextSemester =
      sessionStorage.getItem("mosIncludeNextSemester") === "true";
    this.isIncludePreviousSemester =
      sessionStorage.getItem("mosIncludePreviousSemester") === "true";
    this.queryMosBlocks();
  }

  filterBlocksForDisplay(): void {
    const minRa = this.raMinimumEl.nativeElement.value || "0:0:0";
    const maxRa = this.raMaximumEl.nativeElement.value || "23:59:59.999";
    const proposalCode =
      this.proposalCodeEl.nativeElement.value.toLocaleLowerCase() || "";
    const barcode =
      this.barcodeEl.nativeElement.value.toLocaleLowerCase() || "";
    const piSurname =
      this.piSurnameEl.nativeElement.value.toLocaleLowerCase() || "";
    let filteredBlocks = this.mosBlocks;

    // filter by proposal code.
    filteredBlocks = filteredBlocks.filter((mb) =>
      mb.proposalCode.toLocaleLowerCase().includes(proposalCode),
    );

    // filter by barcode.
    filteredBlocks = filteredBlocks.filter((mb) =>
      mb.barcode.toLocaleLowerCase().includes(barcode),
    );

    // Filter by PI surname
    filteredBlocks = filteredBlocks.filter((mb) =>
      mb.piSurname.toLocaleLowerCase().includes(piSurname),
    );

    // Filter by RA center
    filteredBlocks = filteredBlocks.filter((mb) => {
      return (
        mb["raCenter"] >= this.validateRa(minRa, "min") &&
        this.validateRa(maxRa, "max") >= mb["raCenter"]
      );
    });

    this.displayedMosBlocks = filteredBlocks;
  }

  queryMosBlocks(): void {
    this.displayedMosBlocks = [];
    this.error = undefined;
    this.loading = true;
    let fromSemester = this.selectedSemester;
    let toSemester = this.selectedSemester;

    if (sessionStorage.getItem("mosIncludeNextSemester") === "true") {
      toSemester = nextSemesterOf(this.selectedSemester);
    }
    if (sessionStorage.getItem("mosIncludePreviousSemester") === "true") {
      fromSemester = previousSemesterOf(this.selectedSemester);
    }

    this.mosBlocksSubscription = this.mosService
      .getMosBlocks(fromSemester, toSemester)
      .subscribe(
        (data) => {
          data.forEach((m: MosBlock) => {
            if (
              (m.blockStatus.toLocaleLowerCase() === "active" ||
              m.blockStatus.toLocaleLowerCase() === "on hold") &&
              m.remainingNights > 0
            ) {
              this.requiredMosMasks.push(m.barcode);
            }
          });
          this.mosBlocks = data;
          this.filterBlocksForDisplay();
          this.loading = false;
        },
        () => {
          this.loading = false;
          this.mosBlocks = [];
          this.error = "Failed to fetch MOS blocks.";
        },
      );
  }

  semesterChange(event: any): void {
    this.selectedSemester = event.target.value;
    this.queryMosBlocks();
    sessionStorage.setItem("mosSelectedSemester", event.target.value);
  }

  includeSemester(name: string, checked: boolean): void {
    localStorage.setItem(name, checked.toString());
    this.queryMosBlocks();
  }

  validateRa(ra: string, whichRa: "max" | "min"): number {
    try {
      if (whichRa === "max") {
        this.raMaxError = undefined;
      }
      if (whichRa === "min") {
        this.raMinError = undefined;
      }
      return convertRightAscensionHMSToDegrees(ra);
    } catch (e: any) {
      if (whichRa === "min") {
        this.raMinError = e.message;
      } else {
        this.raMaxError = e.message;
      }
    }
    return whichRa === "min" ? 0 : 360;
  }
}
