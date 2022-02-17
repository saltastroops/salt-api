import { Component, EventEmitter, Input, OnInit, Output } from "@angular/core";

import { parseISO } from "date-fns";

import { BlockVisit } from "../../../types/common";

@Component({
  selector: "wm-summary-of-executed-observations",
  templateUrl: "./summary-of-executed-observations.component.html",
  styleUrls: ["./summary-of-executed-observations.component.scss"],
})
export class SummaryOfExecutedObservationsComponent implements OnInit {
  selectAll = false;
  @Input() blockVisits!: BlockVisit[];
  @Output() selectBlock = new EventEmitter<string>();
  observations!: Observation[];

  ngOnInit(): void {
    this.observations = this.blockVisits.map((o) => ({
      ...o,
      downloadObservation: this.selectAll,
    }));
  }

  selectDeselectAll(selectAll: boolean): void {
    this.selectAll = selectAll;
    this.observations.forEach((e) => {
      e.downloadObservation = this.selectAll;
    });
  }

  toggleRequestData(observation_id: number): void {
    this.selectAll = true;
    this.observations.forEach((o) => {
      if (o.blockId === observation_id) {
        o.downloadObservation = !o.downloadObservation;
      }
      if (!o.downloadObservation) {
        this.selectAll = false;
      }
    });
  }

  observationDate(dateString: string): Date {
    return parseISO(dateString);
  }

  onClick(blockName: string): void {
    this.selectBlock.emit(blockName);
  }
}

interface Observation extends BlockVisit {
  downloadObservation: boolean;
}
