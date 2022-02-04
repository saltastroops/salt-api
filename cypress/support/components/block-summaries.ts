const FILTER_COMPLETED = '#filter-completed';
const FILTER_UNOBSERVABLE = '#filter-unobservable';
const COMPLETED_BLOCK = '[data-test="completed-block"]';
const UNOBSERVABLE_BLOCK = '[data-test="unobservable-block"]';
const SORT_BY_ID_COLUMN = '[data-testid=block-summary-id]';
const SORT_BY_NAME_COLUMN = '[data-testid=block-summary-name]';
const BLOCK_ID_ROW = '[data-test=block-id]';
const BLOCK_NAME_ROW = '[data-test=block-name]';

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

  static clickBlockIdColumn() {
    cy.get(SORT_BY_ID_COLUMN).click();
  }

  static clickBlockNameColumn() {
    cy.get(SORT_BY_ID_COLUMN).click();
  }

  static blocksSortedByIdInAscending(ascending: boolean) {
    let sortedBlockIds = [];
    if (ascending) {
      cy.get(BLOCK_ID_ROW)
        .each(($el, index) => {
          sortedBlockIds[index] = $el.text();
        })
        .then(() => {
          expect(sortedBlockIds).to.deep.equal(sortedBlockIds.sort());
        });
    } else {
      cy.get(BLOCK_ID_ROW)
        .each(($el, index) => {
          sortedBlockIds[index] = $el.text();
        })
        .then(() => {
          expect(sortedBlockIds).to.deep.equal(sortedBlockIds.reverse());
        });
    }
  }

  static blocksSortedByNameInAscending(ascending: boolean) {
    let sortedNames = [];
    if (ascending) {
      cy.get(BLOCK_NAME_ROW)
        .each(($el, index) => {
          sortedNames[index] = $el.text();
        })
        .then(() => {
          expect(sortedNames).to.deep.equal(sortedNames.sort());
        });
    } else {
      cy.get(BLOCK_NAME_ROW)
        .each(($el, index) => {
          sortedNames[index] = $el.text();
        })
        .then(() => {
          expect(sortedNames).to.deep.equal(sortedNames.reverse());
        });
    }
  }
}
