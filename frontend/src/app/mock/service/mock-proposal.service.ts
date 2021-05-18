import { Injectable, isDevMode } from '@angular/core';
import { Observable, of } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { ProposalService } from '../../service/proposal.service';
import { Proposal } from '../../types';
import { proposal } from '../proposal-data';

@Injectable({
  providedIn: 'root',
})
export class MockProposalService implements ProposalService {
  constructor(private http: HttpClient) {}

  getProposal(proposalCode: string): Observable<Proposal> {
    return of(proposal);
  }
}
