import { Observable } from 'rxjs';
import {
  ObservationComment,
  Proposal,
  ProposalListItem,
} from '../types/proposal';

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
  public abstract getProposals(): Observable<ProposalListItem[]>;

  /**
   * Get the list of observation comments for a proposal from the API server.
   *
   * If the request fails the stream terminates with a generic error message as error.
   */
  public abstract getObservationComments(
    proposalCode: string
  ): Observable<ObservationComment[]>;

  /**
   * Submit an observation comment to the API server.
   *
   * If the request fails the stream terminates with a generic error message as error.
   */
  public abstract submitObservationComment(
    proposalCode: string,
    comment: string
  ): Observable<ObservationComment[]>;
}
