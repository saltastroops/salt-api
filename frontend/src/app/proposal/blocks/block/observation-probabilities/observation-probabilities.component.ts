import { Component, Input, OnInit } from '@angular/core';
import { ObservationProbabilities } from '../../../../types/common';

@Component({
  selector: 'wm-observation-probabilities',
  templateUrl: './observation-probabilities.component.html',
  styleUrls: ['./observation-probabilities.component.scss'],
})
export class ObservationProbabilitiesComponent implements OnInit {
  @Input() probabilities!: ObservationProbabilities;

  constructor() {}

  ngOnInit(): void {}
}
