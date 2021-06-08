import {Component, Input, OnInit} from '@angular/core';
import {GeneralProposalInfo} from "../../types";

@Component({
  selector: 'wm-details',
  templateUrl: './proposal-details.component.html',
  styleUrls: ['./proposal-details.component.scss']
})
export class ProposalDetailsComponent implements OnInit {
  @Input() general_proposal_info!: GeneralProposalInfo;
  constructor() { }

  ngOnInit(): void {}

}
