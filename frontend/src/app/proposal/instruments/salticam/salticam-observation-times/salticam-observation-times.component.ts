import { Component, OnInit, Input } from '@angular/core';
import { Salticam } from '../../../../types/salticam';

@Component({
  selector: 'wm-salticam-observation-times',
  templateUrl: './salticam-observation-times.component.html',
  styleUrls: ['./salticam-observation-times.component.scss'],
})
export class SalticamObservationTimesComponent implements OnInit {
  @Input() salticam!: Salticam;

  constructor() {}

  ngOnInit(): void {}
}