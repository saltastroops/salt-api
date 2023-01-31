import {
  Component,
  EventEmitter,
  Input,
  OnChanges,
  OnInit,
  Output,
} from "@angular/core";

import { Sort } from "../../../sort";
import { SortDirection } from "../../../sort.directive";
import { BlockSummary } from "../../../types/block";

@Component({
  selector: "wm-block-summaries",
  templateUrl: "./block-summaries.component.html",
  styleUrls: ["./block-summaries.component.scss"],
})
export class BlockSummariesComponent implements OnInit, OnChanges {
  @Input() blocks!: BlockSummary[];
  @Input() proposalCode!: string;
  @Output() selectBlock = new EventEmitter<number>();
  filteredByCompleted!: boolean;
  filteredByUnobservable!: boolean;
  filteredBlocks: BlockSummary[] = [];
  initialized = false;

  ngOnInit(): void {
    this.filteredByCompleted =
      localStorage.getItem("filterByCompleted") == "true";
    this.filteredByUnobservable =
      localStorage.getItem("filterByUnobservable") == "true";

    this.filterBlocks();
    this.initialized = true;
  }

  ngOnChanges(): void {
    if (this.initialized) {
      this.filterBlocks();
    }
  }

  onClick(blockId: number): void {
    this.selectBlock.emit(blockId);
  }

  filterByCompleted(): void {
    this.filteredByCompleted = !this.filteredByCompleted;
    localStorage.setItem(
      "filterByCompleted",
      JSON.stringify(this.filteredByCompleted),
    );
    this.filterBlocks();
  }

  filterByUnobservable(): void {
    this.filteredByUnobservable = !this.filteredByUnobservable;
    localStorage.setItem(
      "filterByUnobservable",
      JSON.stringify(this.filteredByUnobservable),
    );
    this.filterBlocks();
  }

  filterBlocks(): void {
    let blocks = [...this.blocks];
    if (this.filteredByCompleted) {
      blocks = blocks.filter((block) => block.status.value !== "Completed");
    }
    if (this.filteredByUnobservable) {
      blocks = blocks.filter(
        (block) =>
          block.acceptedObservations === block.requestedObservations ||
          block.remainingNights !== 0,
      );
    }
    this.filteredBlocks = blocks;
  }

  isCompleted(block: BlockSummary): boolean {
    return (
      block.status.value === "Completed" &&
      block.acceptedObservations === block.requestedObservations
    );
  }

  isUnobservable(block: BlockSummary): boolean {
    return (
      block.remainingNights === 0 &&
      block.acceptedObservations !== block.requestedObservations
    );
  }

  blockClass(block: BlockSummary): string {
    if (this.isCompleted(block)) {
      return "completed-block";
    } else if (this.isUnobservable(block)) {
      return "is-red-background";
    }
    return "";
  }

  blockDataTestAttribute(block: BlockSummary): string {
    if (this.isCompleted(block)) {
      return "completed-block";
    } else if (this.isUnobservable(block)) {
      return "unobservable-block";
    }
    return "";
  }

  sort = (key: string, direction: SortDirection): void => {
    const sort = new Sort();
    const isString = ["name"].includes(key);
    let sortFunc;
    if (key == "maximumSeeing") {
      sortFunc = sort.startSort(
        (b: BlockSummary) => b.observingConditions.maximumSeeing,
        direction,
        isString,
      );
    } else if (key == "maximumLunarPhase") {
      sortFunc = sort.startSort(
        (b: BlockSummary) => b.observingConditions.maximumLunarPhase,
        direction,
        isString,
      );
    } else {
      sortFunc = sort.startSort(key, direction, isString);
    }
    this.filteredBlocks.sort(sortFunc);
  };
}
