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
const BLOCK_ID_ELEMENT = '[data-test=block-id]';
const BLOCK_NAME_ELEMENT = '[data-test=block-name]';
const BLOCK_OBSERVATION_TIME_ELEMENT = '[data-test=observation-time]';
const BLOCK_PRIORITY_ELEMENT = '[data-test=block-priority]';
const BLOCK_MAXIMUM_SEEING_ELEMENT = '[data-test=block-maximum-sseing]';
const BLOCK_REMAINING_NIGHTS_ELEMENT = '[data-test=block-remaining-nights]';
const BLOCK_MAXIMUM_LUNAR_PHASE_ELEMENT =
  '[data-test=block-maximum-lunar-phase]';

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
    let columnElement = '';
    switch (column) {
      case 'id':
        columnElement = BLOCK_ID_ELEMENT;
        break;
      case 'name':
        columnElement = BLOCK_NAME_ELEMENT;
        break;
      case 'observation-time':
        columnElement = BLOCK_OBSERVATION_TIME_ELEMENT;
        break;
      case 'priority':
        columnElement = BLOCK_PRIORITY_ELEMENT;
        break;
      case 'remaining-nights':
        columnElement = BLOCK_REMAINING_NIGHTS_ELEMENT;
        break;
      case 'maximum-seeing':
        columnElement = BLOCK_MAXIMUM_SEEING_ELEMENT;
        break;
      case 'maximum-lunar-phase':
        columnElement = BLOCK_MAXIMUM_LUNAR_PHASE_ELEMENT;
    }

    let sortedBlockIds = [];
    if (order==='ascending') {
      cy.get(BLOCK_ID_ELEMENT)
        .each(($el, index) => {
          sortedBlockIds[index] = $el.text();
        })
        .then(() => {
          expect(sortedBlockIds).to.deep.equal(sortedBlockIds.sort());
        });
    }
    if (order==='descending') {
      cy.get(BLOCK_ID_ELEMENT)
        .each(($el, index) => {
          sortedBlockIds[index] = $el.text();
        })
        .then(() => {
          expect(sortedBlockIds).to.deep.equal(sortedBlockIds.reverse());
        });
    }
  }
}
