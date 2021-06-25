import { Component, Input, OnInit } from '@angular/core';
import {Investigator, ProposalAcceptance} from '../../types';

@Component({
  selector: 'wm-investigators',
  templateUrl: './investigators.component.html',
  styleUrls: ['./investigators.component.scss'],
})
export class InvestigatorsComponent implements OnInit {
  @Input() investigators!: Investigator[];
  @Input() proposalAcceptance!: ProposalAcceptance[];

  constructor() {}

  ngOnInit(): void {}

  accepted(investigator: Investigator): boolean | null {
    const inv =  this.proposalAcceptance.find(pa => investigator.id === pa.investigatorId);
    if (inv) {
      return inv.accepted;
    }
    throw new Error('No proposal acceptance status defined for investigator.');
  }
}
