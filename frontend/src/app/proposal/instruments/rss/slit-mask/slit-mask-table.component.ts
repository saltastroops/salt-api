import {Component, Input, OnInit} from '@angular/core';
import {SlitMask} from '../rss-types';

@Component({
  selector: 'wm-rss-slit-mask',
  templateUrl: './slit-mask-table.component.html',
  styleUrls: ['./slit-mask-table.component.scss']
})
export class SlitMaskTableComponent implements OnInit {
  @Input() slitMask!: SlitMask;
  constructor() { }

  ngOnInit(): void {
  }

}
