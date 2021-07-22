import {Component, Input, OnInit} from '@angular/core';
import {Detector} from '../rss/rss-types';

@Component({
  selector: 'wm-detector-table',
  templateUrl: './detector-table.component.html',
  styleUrls: ['./detector-table.component.scss']
})
export class DetectorTableComponent implements OnInit {
  @Input() detector!: Detector;
  constructor() { }

  ngOnInit(): void {
  }

}
