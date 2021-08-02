import {Component, Input, OnInit} from '@angular/core';
import {HrsConfiguration} from "../../../types";

@Component({
  selector: 'wm-configuration-table',
  templateUrl: './hrs-configuration-table.component.html',
  styleUrls: ['./hrs-configuration-table.component.scss']
})
export class HrsConfigurationTableComponent implements OnInit {
  @Input() hrsConfig!: HrsConfiguration;

  constructor() { }

  ngOnInit(): void {
  }

}
