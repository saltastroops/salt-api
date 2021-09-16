import { Component, Input, OnInit } from '@angular/core';
import { ArcBibleEntry } from '../../../../types/rss';

@Component({
  selector: 'wm-arc-bible',
  templateUrl: './arc-bible.component.html',
  styleUrls: ['./arc-bible.component.scss'],
})
export class ArcBibleComponent implements OnInit {
  @Input() arcBibleEntries!: ArcBibleEntry[];

  constructor() {}

  ngOnInit(): void {}
}
