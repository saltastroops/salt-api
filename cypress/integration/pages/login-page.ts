export const LOGIN_URL = '/login';

const USERNAME_INPUT = "[data-test='login-username']";
const PASSWORD_INPUT = "[data-test='login-password']";

export class LoginPage {
  static visit() {
    cy.visit(LOGIN_URL);
  }

  static typeUsername(username: string) {
    cy.get(USERNAME_INPUT).type(username);
  }

  static clearUsername() {
    cy.get(USERNAME_INPUT).clear();
  }

  static hasUsernameError() {
    cy.get("[data-test='error']")
      .contains(/username/i)
      .should('exist');
  }

  static typePassword(password: string) {
    cy.get(PASSWORD_INPUT).type(password);
  }

  static clearPassword() {
    cy.get(PASSWORD_INPUT).clear();
  }

  static hasPasswordError() {
    cy.get("[data-test='error']")
      .contains(/password/i)
      .should('exist');
  }

  static submit() {
    cy.get("[data-test='login-submit']").click();
  }

  static hasGenericError() {
    cy.get("[data-test='error']").should('contain', 'wrong');
  }
}
