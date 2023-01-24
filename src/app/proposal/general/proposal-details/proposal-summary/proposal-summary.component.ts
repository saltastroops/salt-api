import {Component, Input} from '@angular/core';
import {GeneralProposalInfo} from "../../../../types/proposal";

@Component({
  selector: 'wm-proposal-summary',
  templateUrl: './proposal-summary.component.html',
  styleUrls: ['./proposal-summary.component.scss']
})
export class ProposalSummaryComponent {

  @Input() generalProposalInfo!: GeneralProposalInfo;

}
