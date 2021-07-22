import {Component, Input, OnInit} from '@angular/core';
import {InstrumentConfiguration} from '../rss-types';

@Component({
  selector: 'wm-rss-general-table',
  templateUrl: './rss-general-table.component.html',
  styleUrls: ['./rss-general-table.component.scss']
})
export class RssGeneralTableComponent implements OnInit {
  @Input() configuration!: InstrumentConfiguration;
  constructor() { }

  ngOnInit(): void {
  }

}
