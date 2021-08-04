import { Component, OnInit, Input } from '@angular/core';
import { Salticam } from '../../../types/salticam';

@Component({
  selector: 'wm-salticam',
  templateUrl: './salticam.component.html',
  styleUrls: ['./salticam.component.scss'],
})
export class SalticamComponent implements OnInit {
  @Input() salticam!: Salticam;

  constructor() {}

  ngOnInit(): void {}
}
