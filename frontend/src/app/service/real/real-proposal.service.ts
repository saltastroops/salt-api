import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { environment } from '../../../environments/environment';
import { ProposalService } from '../proposal.service';
import { catchError, map } from 'rxjs/operators';
import * as camelcaseKeys from 'camelcase-keys';
import { Phase2Proposal } from '../../types/proposal';

@Injectable({
  providedIn: 'root',
})
export class RealProposalService implements ProposalService {
  constructor(private http: HttpClient) {}

  /**
   * Get a proposal from the API server.
   *
   * If the request fails the stream terminates with a generic error message as error.
   *
   * @param proposalCode Proposal code.
   */
  getProposal(proposalCode: string): Observable<Phase2Proposal> {
    const uri = environment.apiUrl + '/proposals/' + proposalCode;
    return this.http.get<any>(uri).pipe(
      map((proposal: any) => camelcaseKeys(proposal, { deep: true })),
      catchError(() => {
        return throwError('The request has failed.');
      })
    );
  }
}
