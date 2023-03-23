const BLOCK_LINK = '[data-test="executed-observations-block-name"]';
const DISPLAYED_BLOCK_CONTENT = '[data-test="displayed-block-content"]';
const BLOCK_REJECTION_REASON =
  '[data-test="executed-observations-block-rejection-reason"]';

const SORT_BY_NAME_COLUMN =
  "[data-test=executed-observations-block-name-header]";
const SORT_BY_OBSERVATION_TIME_COLUMN =
  "[data-test=executed-observations-observation-time-header]";
const SORT_BY_PRIORITY_COLUMN =
  "[data-test=executed-observations-priority-header]";
const SORT_BY_MAXIMUM_LUNAR_PHASE_COLUMN =
  "[data-test=executed-observations-maximum-lunar-phase-header]";
const SORT_BY_TARGETS_COLUMN =
  "[data-test=executed-observations-targets-header]";
const SORT_BY_OBSERVATION_DATE_COLUMN =
  "[data-test=executed-observations-observation-date-header]";
const SORT_BY_OBSERVATION_STATUS_COLUMN =
  "[data-test=executed-observations-observation-status-header]";

const TOGGLE_EXECUTED_OBSERVATIONS_LINK =
  "[data-test=show-executed-observations]";

const EDIT_BLOCK_VISIT_STATUS_BUTTON =
  "[data-test=executed-observations-status-edit-button]";

const EDIT_BLOCK_VISIT_MODAL = "[data-test=block-visit-status-modal]";

const ERROR = "[data-test=error]";

const BLOCK_VISIT_STATUS_OPTIONS = "[data-test=block-visit-status-value]";

const BLOCK_REJECTION_REASON_OPTIONS = "[data-test=block-rejection-reason]";

const SUBMIT_BLOCK_VISIT_STATUS_BUTTON =
  "[data-test=submit-block-visit-status]";

export class SummaryOfExecutedObservations {
  static clickBlockNameLink(elementIndex: number): void {
    cy.get(BLOCK_LINK).eq(elementIndex).click();
  }

  static clickBlockNameColumn(): void {
    cy.get(SORT_BY_NAME_COLUMN).click();
  }

  static clickBlockObservationTimeColumn(): void {
    cy.get(SORT_BY_OBSERVATION_TIME_COLUMN).click();
  }

  static clickBlockPriorityColumn(): void {
    cy.get(SORT_BY_PRIORITY_COLUMN).click();
  }

  static clickBlockMaximumLunarPhaseColumn(): void {
    cy.get(SORT_BY_MAXIMUM_LUNAR_PHASE_COLUMN).click();
  }

  static clickBlockTargetsColumn(): void {
    cy.get(SORT_BY_TARGETS_COLUMN).click();
  }

  static clickBlockObservationDateColumn(): void {
    cy.get(SORT_BY_OBSERVATION_DATE_COLUMN).click();
  }

  static clickBlockObservationStatusColumn(): void {
    cy.get(SORT_BY_OBSERVATION_STATUS_COLUMN).click();
  }

  static correctBlockLoaded(elementIndex: number): void {
    cy.get(BLOCK_LINK)
      .eq(elementIndex)
      .invoke("text")
      .then((expected_block_name) => {
        cy.get(DISPLAYED_BLOCK_CONTENT)
          .invoke("text")
          .should("contain", expected_block_name.trim());
      });
  }

  static blocksSortedBy(
    column: string,
    order: "ascending" | "descending",
  ): void {
    const valueElement = "[data-test=executed-observations-" + column + "]";
    const headerElement =
      "[data-test=executed-observations-" + column + "-header" + "]";
    const values = [];
    if (order === "ascending") {
      cy.get(headerElement).should("have.class", "asc");
      cy.get(valueElement)
        .each(($el, index) => {
          values[index] = $el.text();
        })
        .then(() => {
          expect(values).to.deep.equal(values.sort());
        });
    }
    if (order === "descending") {
      cy.get(headerElement).should("have.class", "desc");
      cy.get(valueElement)
        .each(($el, index) => {
          values[index] = $el.text();
        })
        .then(() => {
          expect(values).to.deep.equal(values.reverse());
        });
    }
  }

  static clickShowObservationsLink(): void {
    cy.get(TOGGLE_EXECUTED_OBSERVATIONS_LINK).click();
  }

  static editBlockStatusModalShown(shown: boolean): void {
    if (shown) {
      cy.get(EDIT_BLOCK_VISIT_MODAL).should("be.visible");
    } else {
      cy.get(EDIT_BLOCK_VISIT_MODAL).should("not.exist");
    }
  }

  static clickEditBlockVisitStatus(elementIndex: number): void {
    cy.get(EDIT_BLOCK_VISIT_STATUS_BUTTON).eq(elementIndex).click();
  }

  static errorContainsMessage(txt: string): void {
    cy.get(ERROR).then(($el) => {
      const text = $el.text().trim();

      expect(text).to.eq(txt);
    });
  }

  static blockRejectionReasonUpdatedWithReason(
    elementIndex: number,
    rejectionReason: string,
  ): void {
    cy.get(BLOCK_REJECTION_REASON)
      .eq(elementIndex)
      .then(($el) => {
        const text = $el.text().trim();

        expect(text).to.eq(rejectionReason);
      });
  }

  static selectBlockVisitStatus(elementIndex: number): void {
    cy.get(BLOCK_VISIT_STATUS_OPTIONS).select(elementIndex);
  }

  static selectBlockRejectionReason(elementIndex: number): void {
    cy.get(BLOCK_REJECTION_REASON_OPTIONS).select(elementIndex);
  }

  static clickSubmitBlockVisitStatus(): void {
    cy.get(SUBMIT_BLOCK_VISIT_STATUS_BUTTON).click();
  }

  static submitBlockVisitStatusButtonHidden(
    elementIndex: number,
    hidden: boolean,
  ): void {
    if (hidden) {
      cy.get(EDIT_BLOCK_VISIT_STATUS_BUTTON).should("not.exist");
    } else {
      cy.get(EDIT_BLOCK_VISIT_STATUS_BUTTON)
        .eq(elementIndex)
        .should("not.be.hidden");
    }
  }
}
