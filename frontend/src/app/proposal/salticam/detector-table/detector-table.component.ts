import { Component, OnInit, Input } from '@angular/core';
import {Salticam} from '../../../types';

@Component({
  selector: 'wm-detector-table',
  templateUrl: './detector-table.component.html',
  styleUrls: ['./detector-table.component.scss']
})
export class DetectorTableComponent implements OnInit {
  @Input() salticam!: Salticam;
  constructor() { }

  ngOnInit(): void {
  }

}

