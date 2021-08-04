import { Component, Input, OnInit } from '@angular/core';
import {
  PayloadConfiguration,
  TelescopeConfiguration,
} from '../../../../types/observation';

@Component({
  selector: 'wm-payload',
  templateUrl: './payload-configuration.component.html',
  styleUrls: ['./payload-configuration.component.scss'],
})
export class PayloadConfigurationComponent implements OnInit {
  @Input() telescopeConfiguration!: TelescopeConfiguration;
  @Input() payloadConfigurationIndex!: number;

  payloadConfiguration!: PayloadConfiguration;
  instrument!: string;
  headerLine: string | null = null;
  ditherPatternDescription!: string;

  constructor() {}

  ngOnInit(): void {
    this.payloadConfiguration = this.telescopeConfiguration.payloadConfigurations[
      this.payloadConfigurationIndex
    ];
    const instruments = this.payloadConfiguration.instruments;
    if (instruments.salticam) {
      this.instrument = 'Salticam';
      this.headerLine = 'salticam-header-config-color';
    } else if (instruments.rss) {
      this.instrument = 'RSS';
      this.headerLine = 'rss-header-config-color';
    } else if (instruments.hrs) {
      this.instrument = 'HRS';
      this.headerLine = 'hrs-header-config-color';
    } else if (instruments.bvit) {
      this.instrument = 'BVIT';
      this.headerLine = 'bvit-header-config-color';
    }
    const dp = this.telescopeConfiguration.ditherPattern;
    this.ditherPatternDescription = dp
      ? `${dp.horizontalTiles} h.t. x ${
          dp.verticalTiles
        } v.t., ${dp.offsetSize.toFixed(1)} arcsec, ${dp.steps} dithers`
      : '';
  }
}
