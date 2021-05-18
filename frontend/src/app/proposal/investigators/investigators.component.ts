import { Component, Input, OnInit } from '@angular/core';
import { Investigator } from '../../types';

@Component({
  selector: 'wm-investigators',
  templateUrl: './investigators.component.html',
  styleUrls: ['./investigators.component.scss'],
})
export class InvestigatorsComponent implements OnInit {
  @Input() investigators!: Investigator[];

  constructor() {}

  ngOnInit(): void {}
}
