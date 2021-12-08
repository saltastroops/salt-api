import { Component, Input } from '@angular/core';
import { Investigator } from '../../types/proposal';

@Component({
  selector: 'wm-investigators',
  templateUrl: './investigators.component.html',
  styleUrls: ['./investigators.component.scss'],
})
export class InvestigatorsComponent {
  @Input() investigators!: Investigator[];
}
