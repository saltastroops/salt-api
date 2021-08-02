import {Component, Input, OnInit} from '@angular/core';
import {Hrs} from "../../../types";

@Component({
  selector: 'wm-observing-times-table',
  templateUrl: './hrs-observing-times-table.component.html',
  styleUrls: ['./hrs-observing-times-table.component.scss']
})
export class HrsObservingTimesTableComponent implements OnInit {
  @Input() hrs!: Hrs;

  constructor() { }

  ngOnInit(): void {
  }

}
