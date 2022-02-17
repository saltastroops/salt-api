const BLOCK_LINK = '[data-test="executed-observations-block-link"]';
const DISPLAYED_BLOCK_CONTENT = '[data-test="displayed-block-content"]';

export class SummaryOfExecutedObservations {
  static clickBlockNameLink(elementIndex: number) {
    cy.get(BLOCK_LINK).eq(elementIndex).click();
  }

  static correctBlockLoaded(elementIndex: number) {
    cy.get(BLOCK_LINK)
      .eq(elementIndex)
      .invoke("text")
      .then((expected_block_name) => {
        cy.get(DISPLAYED_BLOCK_CONTENT).should("contain", expected_block_name);
      });
  }
}
