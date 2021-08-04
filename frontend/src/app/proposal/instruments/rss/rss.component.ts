import { Component, Input, OnInit } from '@angular/core';
import { Rss } from '../../../types/rss';
import {
  PayloadConfiguration,
  PayloadConfigurationType,
} from '../../../types/observation';

@Component({
  selector: 'wm-rss',
  templateUrl: './rss.component.html',
  styleUrls: ['./rss.component.scss'],
})
export class RssComponent implements OnInit {
  @Input() rss!: Rss;
  @Input() payloadConfiguration!: PayloadConfiguration;
  @Input() runningNumber!: number;
  headerLine: string | null = null;

  constructor() {}

  ngOnInit(): void {
    switch (this.payloadConfiguration.payloadConfigurationType) {
      case 'Science':
        this.headerLine = 'rss-science-config-color';
        break;
      case 'Calibration':
        this.headerLine = 'rss-calibration-config-color';
        break;
      case 'Acquisition':
        this.headerLine = 'rss-header-config-color';
        break;
    }
  }
}
