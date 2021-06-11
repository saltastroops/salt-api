import {Component, Input, OnInit} from '@angular/core';
import {TimeAllocation} from '../../types';

@Component({
  selector: 'wm-time-allocation-table',
  templateUrl: './time-allocation-table.component.html',
  styleUrls: ['./time-allocation-table.component.scss']
})
export class TimeAllocationTableComponent implements OnInit {
  @Input() time_allocations!: TimeAllocation[];
  constructor() { }

  ngOnInit(): void {
  }

}
