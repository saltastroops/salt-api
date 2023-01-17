export const HOME_URL = "/";

export class HomePage {
  static visit(): void {
    cy.visit(HOME_URL);
    cy.wait('@proposals');
  }
}
