import {Component, Input, OnInit} from '@angular/core';
import {RSSConfiguration} from '../rss/rss-types';

@Component({
  selector: 'wm-used-in-table',
  templateUrl: './used-in-table.component.html',
  styleUrls: ['./used-in-table.component.scss']
})
export class UsedInTableComponent implements OnInit {
  @Input() instrumentConfiguration!: RSSConfiguration;
  @Input() runningNumber!: number;
  @Input() ditherPattern!: string | null;
  headerLine: string | null = null;
  constructor() { }

  ngOnInit(): void {
    const instrument = this.instrumentConfiguration.instrument;
    this.headerLine = instrument === 'RSS' ? 'rss-header-config-color' :
      instrument === 'HRS' ? 'hrs-header-config-color' :
        instrument === 'Salticam' ? 'salticam-header-config-color' : null;
  }

}
