import {Component, Input, OnInit} from '@angular/core';
import {ChargedTime, TimeAllocation} from "../../types";

@Component({
  selector: 'wm-charged-time-table',
  templateUrl: './charged-time-table.component.html',
  styleUrls: ['./charged-time-table.component.scss']
})
export class ChargedTimeTableComponent implements OnInit {
  @Input() charged_time!: ChargedTime
  @Input() time_allocation!: TimeAllocation
  allocated_p0_to_p3_time: number = 0
  charged_time_p0_to_p3: number = 0
  constructor() { }

  ngOnInit(): void {
    this.allocated_p0_to_p3_time = this.time_allocation.priority_0 + this.time_allocation.priority_1 +
      this.time_allocation.priority_2 + this.time_allocation.priority_3
    this.charged_time_p0_to_p3 = this.charged_time.priority_0 + this.charged_time.priority_1 +
      this.charged_time.priority_2 + this.charged_time.priority_3
  }

}
