import { Component, OnInit, Input } from '@angular/core';
import { SalticamExposure, SalticamFilter } from '../../../../types/salticam';

@Component({
  selector: 'salticam-wm-filters',
  templateUrl: './salticam-filters.component.html',
  styleUrls: ['./salticam-filters.component.scss'],
})
export class SalticamFiltersComponent implements OnInit {
  @Input() salticamExposures!: SalticamExposure[];

  constructor() {}

  ngOnInit(): void {}
}
