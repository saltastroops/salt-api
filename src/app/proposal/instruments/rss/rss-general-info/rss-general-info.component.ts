import { Component, Input } from '@angular/core';
import { Rss } from '../../../../types/rss';

@Component({
  selector: 'wm-rss-general-info',
  templateUrl: './rss-general-info.component.html',
  styleUrls: ['./rss-general-info.component.scss'],
})
export class RssGeneralInfoComponent {
  @Input() rss!: Rss;
}
