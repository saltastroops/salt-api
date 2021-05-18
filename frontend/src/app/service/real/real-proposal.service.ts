import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { ProposalService } from '../proposal.service';
import { Proposal } from '../../types';

@Injectable({
  providedIn: 'root',
})
export class RealProposalService implements ProposalService {
  constructor(private http: HttpClient) {}

  // TODO: Handle the not-so-happy paths as well!
  getProposal(proposalCode: string): Observable<Proposal> {
    const uri = environment.apiUrl + '/proposal/' + proposalCode;
    return this.http.get<Proposal>(uri.replace('//', '/'));
  }
}
