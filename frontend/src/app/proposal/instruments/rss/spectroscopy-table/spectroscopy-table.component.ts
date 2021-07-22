import {Component, Input, OnInit} from '@angular/core';
import {Spectroscopy} from '../rss-types';

@Component({
  selector: 'wm-spectroscopy-table',
  templateUrl: './spectroscopy-table.component.html',
  styleUrls: ['./spectroscopy-table.component.scss']
})
export class SpectroscopyTableComponent implements OnInit {
  @Input() spectroscopy!: Spectroscopy;
  constructor() { }

  ngOnInit(): void {
  }

}
