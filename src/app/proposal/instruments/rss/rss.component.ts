import { Component, Input } from '@angular/core';
import { Rss } from '../../../types/rss';
import { PayloadConfiguration } from '../../../types/observation';

@Component({
  selector: 'wm-rss',
  templateUrl: './rss.component.html',
  styleUrls: ['./rss.component.scss'],
})
export class RssComponent {
  @Input() rss!: Rss;
  @Input() payloadConfiguration!: PayloadConfiguration;
  headerLine: string | null = null;
}
