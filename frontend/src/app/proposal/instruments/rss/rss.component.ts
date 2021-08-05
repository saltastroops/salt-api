import { Component, Input, OnInit } from '@angular/core';
import { Rss } from '../../../types/rss';
import { PayloadConfiguration } from '../../../types/observation';

@Component({
  selector: 'wm-rss',
  templateUrl: './rss.component.html',
  styleUrls: ['./rss.component.scss'],
})
export class RssComponent implements OnInit {
  @Input() rss!: Rss;
  @Input() payloadConfiguration!: PayloadConfiguration;
  headerLine: string | null = null;

  constructor() {}

  ngOnInit(): void {}
}
