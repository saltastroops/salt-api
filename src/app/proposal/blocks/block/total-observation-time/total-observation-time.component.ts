import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'wm-total-observation-time',
  templateUrl: './total-observation-time.component.html',
  styleUrls: ['./total-observation-time.component.scss'],
})
export class TotalObservationTimeComponent implements OnInit {
  @Input() totalObservationTime!: number;
  @Input() overhead!: number;
  constructor() {}

  ngOnInit(): void {}
}
