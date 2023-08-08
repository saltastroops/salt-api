export const REGISTER_USER_BASE_URL = "register";

export class RegisterUserPage {
  static visit(): void {
    cy.visit(REGISTER_USER_BASE_URL);
  }
}
