import { Component, Input, OnInit } from '@angular/core';
import { HrsConfiguration } from '../../../../types/hrs';

@Component({
  selector: 'wm-hrs-configuration',
  templateUrl: './hrs-configuration.component.html',
  styleUrls: ['./hrs-configuration.component.scss'],
})
export class HrsConfigurationComponent implements OnInit {
  @Input() hrsConfig!: HrsConfiguration;

  constructor() {}

  ngOnInit(): void {}
}
