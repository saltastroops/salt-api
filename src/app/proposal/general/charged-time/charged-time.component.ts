import { Component, Input, OnInit } from '@angular/core';
import { ChargedTime, TimeAllocation } from '../../../types/proposal';

@Component({
  selector: 'wm-charged-time',
  templateUrl: './charged-time.component.html',
  styleUrls: ['./charged-time.component.scss'],
})
export class ChargedTimeComponent implements OnInit {
  @Input() chargedTime!: ChargedTime;
  @Input() timeAllocation!: TimeAllocation;
  allocatedP0ToP3Time: number = 0;
  chargedTimeP0ToP3: number = 0;
  constructor() {}

  ngOnInit(): void {
    this.allocatedP0ToP3Time =
      this.timeAllocation.priority0 +
      this.timeAllocation.priority1 +
      this.timeAllocation.priority2 +
      this.timeAllocation.priority3;
    this.chargedTimeP0ToP3 =
      this.chargedTime.priority0 +
      this.chargedTime.priority1 +
      this.chargedTime.priority2 +
      this.chargedTime.priority3;
  }
}
