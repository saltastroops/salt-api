import { Component, OnInit, Input } from '@angular/core';
import { SalticamExposure, SalticamFilter } from '../../../../types/salticam';

@Component({
  selector: 'wm-salticam-filters',
  templateUrl: './salticam-filters.component.html',
  styleUrls: ['./salticam-filters.component.scss'],
})
export class SalticamFiltersComponent {
  @Input() salticamExposures!: SalticamExposure[];

  constructor() {}
}
