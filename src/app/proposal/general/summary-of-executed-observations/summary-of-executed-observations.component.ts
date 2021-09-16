import { Component, Input, OnInit } from '@angular/core';
import { parseISO } from 'date-fns';
import { ExecutedObservation } from '../../../types/common';

@Component({
  selector: 'wm-summary-of-executed-observations',
  templateUrl: './summary-of-executed-observations.component.html',
  styleUrls: ['./summary-of-executed-observations.component.scss'],
})
export class SummaryOfExecutedObservationsComponent implements OnInit {
  selectAll = false;
  @Input() executedObservations!: ExecutedObservation[];
  observations!: Observation[];
  constructor() {}

  ngOnInit(): void {
    this.observations = this.executedObservations.map((o) => ({
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
}

interface Observation extends ExecutedObservation {
  downloadObservation: boolean;
}
