import { Component, Input, OnInit } from '@angular/core';
import { HrsProcedure } from '../../../../types/hrs';

@Component({
  selector: 'wm-hrs-general-info',
  templateUrl: './hrs-general-info.component.html',
  styleUrls: ['./hrs-general-info.component.scss'],
})
export class HrsGeneralInfoComponent implements OnInit {
  @Input() hrsProcedure!: HrsProcedure;
  constructor() {}

  ngOnInit(): void {}
}
