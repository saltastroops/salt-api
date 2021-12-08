import { Component, Input } from '@angular/core';
import { CalibrationFilter } from '../../../../types/observation';
import { Lamp } from '../../../../types/common';

@Component({
  selector: 'wm-rss-calibration',
  templateUrl: './rss-calibration.component.html',
  styleUrls: ['./rss-calibration.component.scss'],
})
export class RssCalibrationComponent {
  @Input() filter!: CalibrationFilter | null;
  @Input() lamp!: Lamp;
}
