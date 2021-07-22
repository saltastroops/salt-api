import { Component, OnInit, Input } from '@angular/core';
import {SalticamFilter} from "../../../types";

@Component({
  selector: 'wm-filters-table',
  templateUrl: './filters-table.component.html',
  styleUrls: ['./filters-table.component.scss']
})
export class FiltersTableComponent implements OnInit {
  @Input() salticamFilter!: SalticamFilter[];

  constructor() { }

  ngOnInit(): void {
  }

}
