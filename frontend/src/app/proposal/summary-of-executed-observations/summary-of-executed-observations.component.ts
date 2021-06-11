import { Component, Input, OnInit } from '@angular/core';
import { BlockIdentifier, ExecutedObservation } from '../../types';

@Component({
  selector: 'wm-summary-of-executed-observations',
  templateUrl: './summary-of-executed-observations.component.html',
  styleUrls: ['./summary-of-executed-observations.component.scss'],
})
export class SummaryOfExecutedObservationsComponent implements OnInit {
  selectAll = false;
  @Input() executed_observations!: ExecutedObservation[];
  observations!: Observation[];
  constructor() {}

  ngOnInit(): void {
    this.observations = this.executed_observations.map((o) => ({
      ...o,
      download_observation: this.selectAll,
    }));
  }

  selectDeselectAll(selectAll: boolean): void {
    this.selectAll = selectAll;
    this.observations.forEach((e) => {
      e.download_observation = this.selectAll;
    });
  }

  toggleRequestData(observation_id: number): void {
    this.selectAll = true;
    this.observations.forEach((o) => {
      if (o.observation_id === observation_id) {
        o.download_observation = !o.download_observation;
      }
      if (!o.download_observation) {
        this.selectAll = false;
      }
    });
  }
}

interface Observation extends ExecutedObservation {
  download_observation: boolean;
}
