import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { environment } from '../../../environments/environment';
import { ProposalService } from '../proposal.service';
import { catchError, map } from 'rxjs/operators';
import * as camelcaseKeys from 'camelcase-keys';
import { Proposal, ProposalListItem } from '../../types/proposal';

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
  getProposal(proposalCode: string): Observable<Proposal> {
    const uri = environment.apiUrl + '/proposals/' + proposalCode;
    return this.http.get<Proposal>(uri).pipe(
      map((proposal: Proposal) => camelcaseKeys(proposal, { deep: true })),
      catchError(() => {
        return throwError(
          `The request to get proposal "${proposalCode}" has failed.`
        );
      })
    );
  }

  /**
   * Get a list of proposals from the API server.
   *
   * If the request fails the stream terminates with a generic error message as error.
   */
  getProposals(): Observable<ProposalListItem[]> {
    const uri = environment.apiUrl + '/proposals/';
    return this.http.get<ProposalListItem[]>(uri).pipe(
      map((proposals) => {
        return proposals.map((proposal) =>
          camelcaseKeys(proposal, { deep: true })
        );
      }),
      catchError(() => {
        return throwError('Oops. Something is wrong.');
      })
    );
  }
}