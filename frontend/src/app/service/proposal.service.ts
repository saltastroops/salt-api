import { Observable } from 'rxjs';
import { Phase2Proposal } from '../types/proposal';

export abstract class ProposalService {
  /**
   * Get details about a proposal. These include general proposal information such as
   * investigators, but exclude block details.
   *
   * @param proposalCode Proposal code.
   */
  public abstract getProposal(proposalCode: string): Observable<Phase2Proposal>;
}
