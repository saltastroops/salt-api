import { HttpClient, HttpParams } from "@angular/common/http";
import { Injectable } from "@angular/core";

import * as camelcaseKeys from "camelcase-keys";
import { Observable, throwError } from "rxjs";
import { catchError, map, switchMap } from "rxjs/operators";

import { environment } from "../../../environments/environment";
import {
  ObservationComment,
  Proposal,
  ProposalListItem,
  ProposalProgress,
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
  getProposals(
    from_semester: string,
    to_semester: string,
  ): Observable<ProposalListItem[]> {
    const uri = environment.apiUrl + "/proposals/";
    const params = new HttpParams()
      .set("from", from_semester)
      .set("to", to_semester);
    return this.http.get<ProposalListItem[]>(uri, { params }).pipe(
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
  public getProgressReport(
    proposalCode: string,
    semester: string,
  ): Observable<ProposalProgress> {
    const uri = environment.apiUrl + `/progress/${proposalCode}/${semester}`;
    return this.http.get<ProposalProgress>(uri).pipe(
      map((progressReport: ProposalProgress) =>
        camelcaseKeys(progressReport, { deep: true }),
      ),
      catchError(() => {
        return throwError("Oops. Something is wrong.");
      }),
    );
  }

  public putProgressReport(
    proposalCode: string,
    semester: string,
    proposalProgressFormData: FormData,
    additionalPdf: File
  ): Observable<ProposalProgress> {
    const uri = environment.apiUrl + `/progress/${proposalCode}/${semester}`;
    if (additionalPdf){
      proposalProgressFormData.append("additional_pdf", additionalPdf)
    }
    return this.http.put<ProposalProgress>(uri, proposalProgressFormData)
      .pipe(
        map((progressReport: ProposalProgress) => {
          return camelcaseKeys(progressReport, { deep: true })
          },
        ),
      catchError(() => {
        return throwError("Oops. Something is wrong.");
      }),
    );
  }
}
