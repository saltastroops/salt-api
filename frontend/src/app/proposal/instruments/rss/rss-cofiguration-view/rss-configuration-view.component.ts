import {Component, Input, OnInit} from '@angular/core';
import {RSSConfiguration} from '../rss-types';

@Component({
  selector: 'wm-rss-configuration-view',
  templateUrl: './rss-configuration-view.component.html',
  styleUrls: ['./rss-configuration-view.component.scss']
})
export class RssConfigurationViewComponent implements OnInit {
  @Input() instrumentConfiguration!: RSSConfiguration;
  @Input() runningNumber!: number;
  headerLine: string | null = null;
  constructor() { }

  ngOnInit(): void {
    const configurationType = this.instrumentConfiguration.configurationType;
    const instrument = this.instrumentConfiguration.instrument.toLocaleLowerCase();
    this.headerLine = configurationType === 'Science' ? `${instrument}-science-config-color` :
      configurationType === 'Calibration' ? `${instrument}-calibration-config-color` :
        configurationType === 'Acquisition' ? `s${instrument}-header-config-color` : null;
  }
}
