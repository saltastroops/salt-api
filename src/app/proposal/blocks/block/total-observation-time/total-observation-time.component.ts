import { Component, Input } from '@angular/core';

@Component({
  selector: 'wm-total-observation-time',
  templateUrl: './total-observation-time.component.html',
  styleUrls: ['./total-observation-time.component.scss'],
})
export class TotalObservationTimeComponent {
  @Input() totalObservationTime!: number;
  @Input() overhead!: number;
}
