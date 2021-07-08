import {Component, Input, OnInit} from '@angular/core';
import {Block, ObservingWindow} from '../../../types';

@Component({
  selector: 'wm-observing-conditions',
  templateUrl: './observing-conditions.component.html',
  styleUrls: ['./observing-conditions.component.scss']
})
export class ObservingConditionsComponent implements OnInit {
  @Input() block!: Block;
  showObservingWindow = false;
  constructor() { }

  ngOnInit(): void {
  }
}
