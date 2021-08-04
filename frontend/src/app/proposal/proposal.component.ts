import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ProposalService } from '../service/proposal.service';
import { Observable } from 'rxjs';
import { Phase2Proposal } from '../types/proposal';

@Component({
  selector: 'wm-proposal',
  templateUrl: './proposal.component.html',
  styleUrls: ['./proposal.component.scss'],
})
export class ProposalComponent implements OnInit {
  proposalCode = '';
  proposal!: Observable<Phase2Proposal>;

  constructor(
    private route: ActivatedRoute,
    private proposalService: ProposalService
  ) {}

  ngOnInit(): void {
    const routeParams = this.route.snapshot.paramMap;
    this.proposalCode = routeParams.get('proposal-code') || '';
    this.proposal = this.proposalService.getProposal(this.proposalCode);
  }
}
