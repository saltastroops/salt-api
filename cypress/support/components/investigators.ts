const PROPOSAL_APPROVAL_BUTTON =
  '[data-test="proposal-approval-status-button"]';

const APPROVAL_STATUS = '[data-test="proposal-approval-status"]';

export class Investigators {
  static clickApprovalButton(elementIndex: number): void {
    cy.get(PROPOSAL_APPROVAL_BUTTON).eq(elementIndex).click();
  }

  static approvalStatusButtonUpdatedWithStatus(
    elementIndex: number,
    status: string,
  ): void {
    cy.get(PROPOSAL_APPROVAL_BUTTON)
      .eq(elementIndex)
      .then(($el) => {
        const text = $el.text().trim();

        expect(text).to.eq(status);
      });
  }

  static investigatorApprovalStatusButtonHidden(
    elementIndex: number,
    hidden: boolean,
  ): void {
    if (hidden) {
      cy.get(PROPOSAL_APPROVAL_BUTTON).eq(elementIndex).should("be.hidden");
    } else {
      cy.get(PROPOSAL_APPROVAL_BUTTON).eq(elementIndex).should("be.visible");
    }
  }

  static approvalStatusColumnHidden(hidden: boolean): void {
    if (hidden) {
      cy.get(APPROVAL_STATUS).should("not.exist");
    } else {
      cy.get(APPROVAL_STATUS).should("be.visible");
    }
  }
}
