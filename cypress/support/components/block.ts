const BLOCK_STATUS = '[data-test="block-status"]';
const EDIT_BLOCK_STATUS_BUTTON = '[data-test="edit-block-status-button"]';

const EDIT_BLOCK_STATUS_MODAL = '[data-test="block-status-modal"]';
const BLOCK_STATUS_VALUE = '[data-test="block-status-value"]';
const BLOCK_STATUS_REASON = '[data-test="block-status-reason"]';
const SUBMIT_BLOCK_STATUS_BUTTON = '[data-test="submit-block-status"]';

export class Block {
  static clickEditBlockStatusButton(): void {
    cy.get(EDIT_BLOCK_STATUS_BUTTON).click();
  }

  static editBlockStatusButtonExists(exists: boolean): void {
    if (exists) {
      cy.get(EDIT_BLOCK_STATUS_BUTTON).should("exist");
    } else {
      cy.get(EDIT_BLOCK_STATUS_BUTTON).should("not.exist");
    }
  }

  static editBlockStatusModalExists(exists: boolean): void {
    if (exists) {
      cy.get(EDIT_BLOCK_STATUS_MODAL).should("exist");
    } else {
      cy.get(EDIT_BLOCK_STATUS_MODAL).should("not.exist");
    }
  }

  static selectBlockStatus(status: string): void {
    cy.get(BLOCK_STATUS_VALUE).select(status);
  }

  static typeBlockStatusReason(reason: string): void {
    cy.get(BLOCK_STATUS_REASON).clear().type(reason);
  }

  static blockStatusUpdatedWithStatus(status: string): void {
    cy.get(BLOCK_STATUS).should("contain", status.trim());
  }

  static blockStatusReasonUpdatedWithReason(reason: string): void {
    cy.get(BLOCK_STATUS_REASON).should("have.value", reason.trim());
  }

  static clickSubmitButton(): void {
    cy.get(SUBMIT_BLOCK_STATUS_BUTTON).click();
  }
}
