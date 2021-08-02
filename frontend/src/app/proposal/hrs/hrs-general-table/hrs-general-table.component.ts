import {Component, Input, OnInit} from '@angular/core';
import {HrsProcedure} from "../../../types";

@Component({
  selector: 'wm-general-table',
  templateUrl: './hrs-general-table.component.html',
  styleUrls: ['./hrs-general-table.component.scss']
})
export class HrsGeneralTableComponent implements OnInit {
  @Input() hrsProcedure!: HrsProcedure;
  constructor() { }

  ngOnInit(): void {
  }

}
