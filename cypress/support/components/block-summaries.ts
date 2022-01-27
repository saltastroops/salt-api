const FILTER_COMPLETED = '#filter-completed';
const FILTER_UNOBSERVABLE = '#filter-unobservable';
const COMPLETED_BLOCK = '[data-test="completed-block"]';
const UNOBSERVABLE_BLOCK = '[data-test="unobservable-block"]';

export class BlockSummaries {
  static clickFilterCompleted() {
    cy.get(FILTER_COMPLETED).click();
  }

  static clickFilterUnobservable() {
    cy.get(FILTER_UNOBSERVABLE).click();
  }

  static filterCompletedChecked(checked: boolean) {
    if (checked) {
      cy.get(FILTER_COMPLETED).should('be.checked');
    } else {
      cy.get(FILTER_COMPLETED).should('not.be.checked');
    }
  }

  static filterUnobservableChecked(checked: boolean) {
    if (checked) {
      cy.get(FILTER_UNOBSERVABLE).should('be.checked');
    } else {
      cy.get(FILTER_UNOBSERVABLE).should('not.be.checked');
    }
  }

  static hasCompletedBlocks(filtered: boolean) {
    if (filtered) {
      cy.get(COMPLETED_BLOCK);
    } else {
      cy.get(COMPLETED_BLOCK).should('not.exist');
    }
  }

  static hasUnobservableBlocks(filtered: boolean) {
    if (filtered) {
      cy.get(UNOBSERVABLE_BLOCK);
    } else {
      cy.get(UNOBSERVABLE_BLOCK).should('not.exist');
    }
  }
}
