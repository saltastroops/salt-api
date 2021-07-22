import {Component, Input, OnInit} from '@angular/core';
import {ArcBibleEntry} from '../rss-types';

@Component({
  selector: 'wm-arc-bible-table',
  templateUrl: './arc-bible-table.component.html',
  styleUrls: ['./arc-bible-table.component.scss']
})
export class ArcBibleTableComponent implements OnInit {
  @Input() arcBibleEntries!: ArcBibleEntry[];
  constructor() { }

  ngOnInit(): void {}

}
