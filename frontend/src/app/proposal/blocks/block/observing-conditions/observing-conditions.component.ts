import { Component, Input, OnInit } from '@angular/core';
import { Block } from '../../../../types/block';

@Component({
  selector: 'wm-observing-conditions',
  templateUrl: './observing-conditions.component.html',
  styleUrls: ['./observing-conditions.component.scss'],
})
export class ObservingConditionsComponent implements OnInit {
  @Input() block!: Block;
  @Input() observationTime!: number;

  showObservingWindows = false;

  constructor() {}

  ngOnInit(): void {}
}
