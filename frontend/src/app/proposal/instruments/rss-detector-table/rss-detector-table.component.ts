import {Component, Input, OnInit} from '@angular/core';
import {Detector} from '../rss/rss-types';

@Component({
  selector: 'wm-rss-detector-table',
  templateUrl: './rss-detector-table.component.html',
  styleUrls: ['./rss-detector-table.component.scss']
})
export class RssDetectorTableComponent implements OnInit {
  @Input() detector!: Detector;
  constructor() { }

  ngOnInit(): void {
  }

}
