import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ProposalService } from '../service/proposal.service';
import { Observable } from 'rxjs';
import { Proposal } from '../types';
import { MockProposalService } from '../mock/service/mock-proposal.service';

@Component({
  selector: 'wm-proposal',
  templateUrl: './proposal.component.html',
  styleUrls: ['./proposal.component.scss'],
  providers: [{ provide: ProposalService, useClass: MockProposalService }],
})
export class ProposalComponent implements OnInit {
  proposalCode: string = '';
  proposal!: Observable<Proposal>;

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
