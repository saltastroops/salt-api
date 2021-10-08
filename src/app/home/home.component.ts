import { Component, OnInit } from '@angular/core';
import { ProposalService } from '../service/proposal.service';
import { ProposalListItem } from '../types/proposal';
import { Observable } from 'rxjs';

@Component({
  selector: 'wm-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit {
  proposals?: ProposalListItem[];

  constructor(private proposalService: ProposalService) {}

  ngOnInit() {
    this.proposalService.getProposals().subscribe((p) => (this.proposals = p));
  }
}
