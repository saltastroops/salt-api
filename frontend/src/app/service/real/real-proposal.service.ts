import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { environment } from '../../../environments/environment';
import { ProposalService } from '../proposal.service';
import { Proposal } from '../../types';
import { catchError } from 'rxjs/operators';

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
    const uri = environment.apiUrl + '/proposal/' + proposalCode;
    return this.http.get<Proposal>(uri).pipe(
      catchError(() => {
        return throwError('The request has failed.');
      })
    );
  }
}
