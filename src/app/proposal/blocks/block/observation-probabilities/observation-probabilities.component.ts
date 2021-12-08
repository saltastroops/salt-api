import { Component, Input } from '@angular/core';
import { ObservationProbabilities } from '../../../../types/common';

@Component({
  selector: 'wm-observation-probabilities',
  templateUrl: './observation-probabilities.component.html',
  styleUrls: ['./observation-probabilities.component.scss'],
})
export class ObservationProbabilitiesComponent {
  @Input() probabilities!: ObservationProbabilities;
}
