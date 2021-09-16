import { Component, Input, OnInit } from '@angular/core';
import { Observation } from '../../../../types/observation';
import { parseISO } from 'date-fns';

@Component({
  selector: 'wm-observation',
  templateUrl: './observation.component.html',
  styleUrls: ['./observation.component.scss'],
})
export class ObservationComponent implements OnInit {
  @Input() observation!: Observation;

  positionAngles!: Array<any>;
  firstValidFrom: Date | undefined;
  lastValidUntil: Date | undefined;

  constructor() {}

  ngOnInit(): void {
    // TODO: Must be fixed
    this.positionAngles = this.observation.telescopeConfigurations.map(
      (tc) => tc.positionAngle
    );
    this.firstValidFrom = parseISO('1970-01-01T00:00:00Z');
    this.lastValidUntil = parseISO('2100-01-01T00:00:00Z');
  }
}
