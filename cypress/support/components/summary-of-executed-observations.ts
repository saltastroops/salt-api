const BLOCK_LINK = '[data-test="executed-observations-block-name"]';
const DISPLAYED_BLOCK_CONTENT = '[data-test="displayed-block-content"]';

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
}
