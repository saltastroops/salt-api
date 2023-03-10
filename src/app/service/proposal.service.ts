import { Observable } from "rxjs";

import {
  NewProprietaryPeriod,
  ObservationComment,
  Proposal,
  ProposalListItem,
  ProposalProgress,
  ProposalStatus,
  SelfActivation,
} from "../types/proposal";
import { LiaisonAstronomer } from "../types/user";

export abstract class ProposalService {
  /**
   * Get details about a proposal. These include general proposal information such as
   * investigators, but exclude block details.
   *
   * @param proposalCode Proposal code.
   */
  public abstract getProposal(proposalCode: string): Observable<Proposal>;

  /**
   * Get a list of proposals from the API server.
   *
   * If the request fails the stream terminates with a generic error message as error.
   */
  public abstract getProposals(
    from_semester: string,
    to_semester: string,
  ): Observable<ProposalListItem[]>;

  /**
   * Get the list of observation comments for a proposal from the API server.
   *
   * If the request fails the stream terminates with a generic error message as error.
   */
  public abstract getObservationComments(
    proposalCode: string,
  ): Observable<ObservationComment[]>;

  /**
   * Submit an observation comment to the API server.
   *
   * If the request fails the stream terminates with a generic error message as error.
   */
  public abstract submitObservationComment(
    proposalCode: string,
    comment: string,
  ): Observable<ObservationComment[]>;

  public abstract getProgressReport(
    proposalCode: string,
    semester: string,
  ): Observable<ProposalProgress>;

  public abstract putProgressReport(
    proposalCode: string,
    semester: string,
    proposalProgressFormData: FormData,
    additional_pdf: File | null,
  ): Observable<ProposalProgress>;

  public abstract getProgressReportsUrls(
    proposalCode: string,
  ): // eslint-disable-next-line @typescript-eslint/no-explicit-any
  Observable<any>;

  public abstract submitProprietaryPeriod(
    proposalCode: string,
    period: number,
    motivation: string | null,
  ): Observable<NewProprietaryPeriod>;

  public abstract submitProposalStatus(
    proposalCode: string,
    proposalStatus: string,
    proposalStatusReason: string | null,
  ): Observable<ProposalStatus>;

  public abstract updateSelfActivatable(
    proposalCode: string,
    isSelfActivatable: boolean,
  ): Observable<SelfActivation>;

  public abstract updateLiaisonAstronomer(
    proposalCode: string,
    liaisonAstronomerId: number | null,
  ): Observable<LiaisonAstronomer>;
}
