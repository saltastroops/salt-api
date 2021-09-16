import { Component, Input, OnInit } from '@angular/core';
import { RssMode } from '../../../../types/rss';

@Component({
  selector: 'wm-fabry-perot',
  templateUrl: './fabry-perot.component.html',
  styleUrls: ['./fabry-perot.component.scss'],
})
export class FabryPerotComponent implements OnInit {
  @Input() filter!: string;
  @Input() mode!: RssMode;

  constructor() {}

  ngOnInit(): void {}
}
