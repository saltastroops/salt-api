import { Component, Input, OnInit } from '@angular/core';
import { Hrs, HrsDetector } from '../../../../types/hrs';

@Component({
  selector: 'wm-hrs-detector',
  templateUrl: './hrs-detector.component.html',
  styleUrls: ['./hrs-detector.component.scss'],
})
export class HrsDetectorComponent implements OnInit {
  @Input() hrs!: Hrs;
  @Input() detectorColor!: string;
  hrsDetector!: HrsDetector;
  exposureTimes: Array<number | null> = [];

  ngOnInit(): void {
    this.hrsDetector =
      this.detectorColor === 'Blue'
        ? this.hrs.blueDetector
        : this.hrs.redDetector;
    this.exposureTimes =
      this.detectorColor === 'Blue'
        ? this.hrs.procedure.blueExposureTimes
        : this.hrs.procedure.redExposureTimes;
  }
}
