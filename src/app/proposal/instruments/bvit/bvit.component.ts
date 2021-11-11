import { Component, Input, OnInit } from '@angular/core';
import { Bvit } from '../../../types/bvit';
import { PayloadConfiguration } from '../../../types/observation';

@Component({
  selector: 'wm-bvit',
  templateUrl: './bvit.component.html',
  styleUrls: ['./bvit.component.scss'],
})
export class BvitComponent {
  @Input() bvit!: Bvit;
  @Input() payloadConfiguration!: PayloadConfiguration;

  constructor() {}
}
