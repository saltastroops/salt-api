import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";

import * as camelcaseKeys from "camelcase-keys";
import { Observable } from "rxjs";
import { map, switchMap } from "rxjs/operators";

import { environment } from "../../../environments/environment";
import {
  ObservationComment,
  Proposal,
  ProposalListItem,
} from "../../types/proposal";
import { ProposalService } from "../proposal.service";

@Injectable({
  providedIn: "root",
})
export class RealProposalService implements ProposalService {
  constructor(private http: HttpClient) {}

  /**
   * Get a proposal from the API server.
   *
   * @param proposalCode Proposal code.
   */
  getProposal(proposalCode: string): Observable<Proposal> {
    const uri = environment.apiUrl + "/proposals/" + proposalCode;
    return this.http
      .get<Proposal>(uri)
      .pipe(
        map((proposal: Proposal) => camelcaseKeys(proposal, { deep: true })),
      );
  }

  /**
   * Get a list of proposals from the API server.
   */
  getProposals(): Observable<ProposalListItem[]> {
    const uri = environment.apiUrl + "/proposals/";
    return this.http.get<ProposalListItem[]>(uri).pipe(
      map((proposals) => {
        return proposals.map((proposal) =>
          camelcaseKeys(proposal, { deep: true }),
        );
      }),
    );
  }

  /**
   * Get the list of observation comments for a proposal from the API server.
   */
  public getObservationComments(
    proposalCode: string,
  ): Observable<ObservationComment[]> {
    const uri =
      environment.apiUrl +
      "/proposals/" +
      proposalCode +
      "/observation-comments";
    return this.http.get<ObservationComment[]>(uri).pipe(
      map((observationComments) => {
        return observationComments.map((observationComment) =>
          camelcaseKeys(observationComment, { deep: true }),
        );
      }),
    );
  }

  /**
   * Submit an observation comment to the API server.
   */
  public submitObservationComment(
    proposalCode: string,
    comment: string,
  ): Observable<ObservationComment[]> {
    const uri =
      environment.apiUrl +
      "/proposals/" +
      proposalCode +
      "/observation-comments";
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    return this.http.post<any>(uri, { comment }).pipe(
      switchMap(() => this.http.get(uri)),
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      map((comments: any) => camelcaseKeys(comments, { deep: true })),
    );
  }
}
