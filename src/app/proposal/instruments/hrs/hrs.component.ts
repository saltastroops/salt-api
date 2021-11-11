import { Component, Input, OnInit } from '@angular/core';
import { Hrs } from '../../../types/hrs';
import { PayloadConfiguration } from '../../../types/observation';

@Component({
  selector: 'wm-hrs',
  templateUrl: './hrs.component.html',
  styleUrls: ['./hrs.component.scss'],
})
export class HrsComponent {
  @Input() hrs!: Hrs;
  @Input() payloadConfiguration!: PayloadConfiguration;

  constructor() {}
}
