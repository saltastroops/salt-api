import { Component, Input, OnInit } from '@angular/core';
import { Salticam } from '../../../../types/salticam';

@Component({
  selector: 'wm-salticam-general-info',
  templateUrl: './salticam-general-info.component.html',
  styleUrls: ['./salticam-general-info.component.scss'],
})
export class SalticamGeneralInfoComponent implements OnInit {
  @Input() salticam!: Salticam;

  constructor() {}

  ngOnInit(): void {}
}
