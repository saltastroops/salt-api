import { Component, OnInit, Input } from '@angular/core';
import {Salticam} from "../../../types";

@Component({
  selector: 'wm-observaton-times',
  templateUrl: './observation-times.component.html',
  styleUrls: ['./observation-times.component.scss']
})
export class ObservationTimesComponent implements OnInit {
  @Input() salticam!: Salticam

  constructor() { }

  ngOnInit(): void {
  }

}
