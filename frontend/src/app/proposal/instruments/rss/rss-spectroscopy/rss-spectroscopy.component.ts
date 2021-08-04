import { Component, Input, OnInit } from '@angular/core';
import { RssSpectroscopy } from '../../../../types/rss';

@Component({
  selector: 'wm-rss-spectroscopy',
  templateUrl: './rss-spectroscopy.component.html',
  styleUrls: ['./rss-spectroscopy.component.scss'],
})
export class RssSpectroscopyComponent implements OnInit {
  @Input() spectroscopy!: RssSpectroscopy;
  @Input() filter!: string;

  constructor() {}

  ngOnInit(): void {}
}
