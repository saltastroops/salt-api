import { Component, Input, OnInit } from '@angular/core';
import { Hrs } from '../../../../types/hrs';

@Component({
  selector: 'wm-hrs-observing-times',
  templateUrl: './hrs-observing-times.component.html',
  styleUrls: ['./hrs-observing-times.component.scss'],
})
export class HrsObservingTimesComponent implements OnInit {
  @Input() hrs!: Hrs;

  constructor() {}

  ngOnInit(): void {}
}
