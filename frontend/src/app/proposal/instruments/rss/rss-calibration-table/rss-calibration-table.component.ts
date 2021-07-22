import {Component, Input, OnInit} from '@angular/core';
import {CalibrationSetup} from '../rss-types';

@Component({
  selector: 'wm-rss-calibration-table',
  templateUrl: './rss-calibration-table.component.html',
  styleUrls: ['./rss-calibration-table.component.scss']
})
export class RssCalibrationTableComponent implements OnInit {
  @Input() calibrationSetup!: CalibrationSetup[];
  constructor() { }

  ngOnInit(): void {}

}
