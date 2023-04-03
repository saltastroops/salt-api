import { HttpClient, HttpParams } from "@angular/common/http";
import { Injectable } from "@angular/core";

import * as camelcaseKeys from "camelcase-keys";
import { Observable, throwError } from "rxjs";
import { catchError, map, switchMap } from "rxjs/operators";

import { environment } from "../../../environments/environment";
import { Message } from "../../types/common";
import {
  NewProprietaryPeriod,
  ObservationComment,
  ProgressReportsUrls,
  Proposal,
  ProposalListItem,
  ProposalProgress,
  ProposalStatus,
  SelfActivation,
} from "../../types/proposal";
import { LiaisonAstronomer } from "../../types/user";
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
    additionalPdf: File,
  ): Observable<ProposalProgress> {
    const uri = environment.apiUrl + `/progress/${proposalCode}/${semester}`;
    if (additionalPdf) {
      proposalProgressFormData.append("additional_pdf", additionalPdf);
    }
    return this.http.put<ProposalProgress>(uri, proposalProgressFormData).pipe(
      map((progressReport: ProposalProgress) => {
        return camelcaseKeys(progressReport, { deep: true });
      }),
      catchError(() => {
        return throwError("Oops. Something is wrong.");
      }),
    );
  }

  /**
   * Get all progress reports links from the API server.
   */
  getProgressReportsUrls(
    proposalCode: string,
  ): Observable<ProgressReportsUrls> {
    const uri = environment.apiUrl + `/progress/${proposalCode}/`;
    return this.http.get<ProgressReportsUrls>(uri).pipe(
      map((progressReportsUrls: ProgressReportsUrls) => {
        const reportsUrls: ProgressReportsUrls = {};
        for (const [k, v] of Object.entries(progressReportsUrls)) {
          reportsUrls[k] = camelcaseKeys(v, { deep: true });
        }
        return reportsUrls;
      }),
    );
  }

  /**
   * Submit a proprietary period to the API server.
   */
  public submitProprietaryPeriod(
    proposalCode: string,
    period: number,
    motivation: string | null = null,
  ): Observable<NewProprietaryPeriod> {
    const uri =
      environment.apiUrl + "/proposals/" + proposalCode + "/proprietary-period";
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    return this.http
      .put<NewProprietaryPeriod>(uri, {
        proprietary_period: period,
        motivation: motivation,
      })
      .pipe(
        map((proprietaryPeriod: NewProprietaryPeriod) => {
          return camelcaseKeys(proprietaryPeriod, { deep: true });
        }),
        catchError(() => {
          return throwError("Oops. Something is wrong.");
        }),
      );
  }

  public submitProposalStatus(
    proposalCode: string,
    proposalStatus: string,
    proposalStatusComment: string | null,
  ): Observable<ProposalStatus> {
    const uri = environment.apiUrl + "/proposals/" + proposalCode + "/status";
    return this.http
      .put<ProposalStatus>(uri, {
        value: proposalStatus,
        comment: proposalStatusComment,
      })
      .pipe(
        map((proposalStatus: ProposalStatus) => {
          return camelcaseKeys(proposalStatus, { deep: true });
        }),
        catchError(() => {
          return throwError("Oops. Something is wrong.");
        }),
      );
  }

  /**
   * Update the proposal self activation.
   */
  public updateSelfActivatable(
    proposalCode: string,
    isSelfActivatable: boolean,
  ): Observable<SelfActivation> {
    const uri =
      environment.apiUrl + "/proposals/" + proposalCode + "/self-activation";
    return this.http
      .put<SelfActivation>(uri, { allowed: isSelfActivatable })
      .pipe(
        map((selfActivatable: SelfActivation) => {
          return camelcaseKeys(selfActivatable, { deep: true });
        }),
        catchError(() => {
          return throwError("Oops. Something is wrong.");
        }),
      );
  }

  /**
   * Update the liaison astronomer.
   */
  public updateLiaisonAstronomer(
    proposalCode: string,
    liaisonAstronomerId: number | null,
  ): Observable<LiaisonAstronomer> {
    const uri =
      environment.apiUrl + "/proposals/" + proposalCode + "/liaison-astronomer";
    return this.http
      .put<LiaisonAstronomer>(uri, { id: liaisonAstronomerId })
      .pipe(
        map((liaisonAstronomer) => {
          return camelcaseKeys(liaisonAstronomer, { deep: true });
        }),
        catchError(() => {
          return throwError("Oops. Something is wrong.");
        }),
      );
  }

  /**
   * Submit an investigator's proposal approval status to the API server.
   */
  public updateInvestigatorProposalApprovalStatus(
    investigatorId: number,
    proposalCode: string,
    approved: boolean,
  ): Observable<void> {
    const uri = `${environment.apiUrl}/proposals/${proposalCode}/approvals/${investigatorId}`;
    return this.http.put<void>(uri, { approved: approved });
  }

  public requestData(
    proposalCode: string,
    requestedObservationIds: number[],
    requestedDataFormats: string[],
  ): Observable<Message> {
    const uri =
      environment.apiUrl + "/proposals/" + proposalCode + "/request-data";
    return this.http
      .post<Message>(uri, {
        observation_ids: requestedObservationIds,
        data_formats: requestedDataFormats,
      })
      .pipe(
        map((message) => {
          return camelcaseKeys(message, { deep: true });
        }),
        catchError(() => {
          return throwError("Oops. Something is wrong.");
        }),
      );
  }
}
