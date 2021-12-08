import { Component, Input } from '@angular/core';
import { RssDetector } from '../../../../types/rss';

@Component({
  selector: 'wm-rss-detector',
  templateUrl: './rss-detector.component.html',
  styleUrls: ['./rss-detector.component.scss'],
})
export class RssDetectorComponent {
  @Input() detector!: RssDetector;
}
