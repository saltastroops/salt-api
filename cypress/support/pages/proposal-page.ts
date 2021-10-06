export const PROPOSAL_BASE_URL = 'proposal';

export class ProposalPage {
  static visit(proposalCode: string) {
    cy.visit(`${PROPOSAL_BASE_URL}/${proposalCode}`);
  }
}
