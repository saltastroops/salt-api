const FILTER_COMPLETED = '#filter-completed';
const FILTER_UNOBSERVABLE = '#filter-unobservable';
const COMPLETED_BLOCK = '[data-test="completed-block"]';
const UNOBSERVABLE_BLOCK = '[data-test="unobservable-block"]';
const SORT_BY_ID_COLUMN = '[data-testid=block-summary-id]';
const SORT_BY_NAME_COLUMN = '[data-testid=block-summary-name]';
const SORT_BY_OBSERVATION_TIME_COLUMN =
  '[data-testid=block-summary-observation-time]';
const SORT_BY_PRIORITY_COLUMN = '[data-testid=block-summary-priority]';
const SORT_BY_REMAINING_NIGHTS_COLUMN =
  '[data-testid=block-summary-remaining-nights]';
const SORT_BY_MAXIMUM_SEEING_COLUMN =
  '[data-testid=block-summary-maximum-seeing]';
const SORT_BY_MAXIMUM_LUNAR_PHASE_COLUMN =
  '[data-testid=block-summary-maximum-lunar-phase]';
const BLOCK_LINK = '[data-test="block-name"]';
const DISPLAYED_BLOCK_CONTENT = '[data-test="displayed-block-content"]';


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
    cy.get(SORT_BY_NAME_COLUMN).click();
  }

  static clickBlockObservationTimeColumn() {
    cy.get(SORT_BY_OBSERVATION_TIME_COLUMN).click();
  }

  static clickBlockPriorityColumn() {
    cy.get(SORT_BY_PRIORITY_COLUMN).click();
  }

  static clickBlockMaximumSeeingColumn() {
    cy.get(SORT_BY_MAXIMUM_SEEING_COLUMN).click();
  }

  static clickBlockRemainingNightsColumn() {
    cy.get(SORT_BY_REMAINING_NIGHTS_COLUMN).click();
  }

  static clickBlockMaximumLunarPhaseColumn() {
    cy.get(SORT_BY_MAXIMUM_LUNAR_PHASE_COLUMN).click();
  }

  static blocksSortedBy(column: string, order: 'ascending' | 'descending') {
    const rowElement = '[data-test=block-' + column + ']';
    const columnElement = '[data-testid=block-summary-' + column + ']';
    const sortedBlockIds = [];
    if (order === 'ascending') {
      cy.get(columnElement).should('have.class', 'asc');
      cy.get(rowElement)
        .each(($el, index) => {
          sortedBlockIds[index] = $el.text();
        })
        .then(() => {
          expect(sortedBlockIds).to.deep.equal(sortedBlockIds.sort());
        });
    }
    if (order === 'descending') {
      cy.get(columnElement).should('have.class', 'desc');
      cy.get(rowElement)
        .each(($el, index) => {
          sortedBlockIds[index] = $el.text();
        })
        .then(() => {
          expect(sortedBlockIds).to.deep.equal(sortedBlockIds.reverse());
        });
    }
  }
  static clickBlockNameLink(elementIndex: number) {
    cy.get(BLOCK_LINK).eq(elementIndex).click();
  }

  static correctBlockLoaded(elementIndex: number) {
    cy.get(BLOCK_LINK)
      .eq(elementIndex)
      .invoke('text')
      .then((expected_block_name) => {
        cy.get(DISPLAYED_BLOCK_CONTENT).should('contain', expected_block_name);
      });
  }
}
