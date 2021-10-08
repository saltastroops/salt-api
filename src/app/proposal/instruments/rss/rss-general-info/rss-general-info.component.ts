import { Component, Input, OnInit } from '@angular/core';
import { Rss } from '../../../../types/rss';

@Component({
  selector: 'wm-rss-general-info',
  templateUrl: './rss-general-info.component.html',
  styleUrls: ['./rss-general-info.component.scss'],
})
export class RssGeneralInfoComponent implements OnInit {
  @Input() rss!: Rss;
  constructor() {}

  ngOnInit(): void {}
}
