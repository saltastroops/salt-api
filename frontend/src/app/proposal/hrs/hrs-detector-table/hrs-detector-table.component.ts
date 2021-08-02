import {Component, Input, OnInit} from '@angular/core';
import {Hrs, HrsDetector} from "../../../types";

@Component({
  selector: 'wm-detector-table',
  templateUrl: './hrs-detector-table.component.html',
  styleUrls: ['./hrs-detector-table.component.scss']
})
export class HrsDetectorTableComponent implements OnInit {
  @Input() hrs!: Hrs;
  @Input() detectorColor!: string;
  hrsDetector!: HrsDetector;
  exposure_times: number[] = [];

  constructor() { }

  ngOnInit(): void {
    this.hrsDetector = this.detectorColor === "Blue" ? this.hrs.hrsBlueDetector :
      this.hrs.hrsRedDetector;
    this.exposure_times = this.detectorColor === "Blue" ? this.hrs.hrsProcedure.blueExposurePattern :
      this.hrs.hrsProcedure.redExposurePattern;
  }

}
