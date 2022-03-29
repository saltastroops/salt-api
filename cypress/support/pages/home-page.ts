export const HOME_URL = "/";

export class HomePage {
  static visit(): void {
    cy.visit(HOME_URL);

    // wait for all proposals to be loaded
    cy.wait(5000);
  }
}
