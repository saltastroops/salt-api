import {Component, Input, OnInit} from '@angular/core';
import {RSSConfiguration} from '../rss-types';

@Component({
  selector: 'wm-rss-view',
  templateUrl: './rss-view.component.html',
  styleUrls: ['./rss-view.component.scss']
})
export class RssViewComponent implements OnInit {
  // TODO Input instrumentConfiguration is from array within the block and runningNumber is its index.
  // TODO Input DitherPattern is from telescope config
  @Input() instrumentConfiguration: RSSConfiguration = {
    id: 99,
    instrument: 'RSS',
    configurationType: 'Science',
    guideMethod: null,
    usedIn: {
      block: {name: 'Block name', id: 12345},
      observation: {name: 'Observation name', id: 54321},
      pa: 300,
      iterations: 2,
    },
    configuration: {
      minSN: 0,
      cycles: 1,
      totalExposureTime: 100,
      overhead: 10,
      chargedTime: 10,
      guideMethod: null,
      spectroscopy: {
        filter: 'pc0000',
        grating: 'pg0000',
        gratingAngle: 18,
        cameraStation: 40,
        cameraAngle: 30
      },
      slitMask: {
        maskType: 'Longslit',
        description: 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Culpa error esse ex ipsum molestiae saepe.',
        barcode: 'PL0000N000'
      },
      detector: {
        iterations: 2,
        readoutSpeed: 'Slow',
        gain: 'Faint',
        mode: 'Normal',
        binning: '2 x 2',
        exposureType: 'Arc',
        exposureTime: 50,
        windowHeight: null
      },
      calibrations: [
        {lamp: 'Xe', filterSetup: null},
        {lamp: 'Ar', filterSetup: null}
      ],
      arcBibleEntries: [
        {lamp: 'Xe', baseExposureTime: 60, correctedExposureTime: 5.1},
        {lamp: 'Ag', baseExposureTime: 50, correctedExposureTime: 2.1},
        {lamp: 'Ne', baseExposureTime: 40, correctedExposureTime: 6.1},
      ]
    },
  };
  @Input() runningNumber = 0;
  @Input() ditherPattern = null;
  constructor() { }

  ngOnInit(): void {
  }

}
