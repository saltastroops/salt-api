export const LOGIN_URL = '/login';

const USERNAME_INPUT = "[data-test='login-username']";
const PASSWORD_INPUT = "[data-test='login-password']";
const ERROR = "[data-test='error']";

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
    cy.get(ERROR)
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
    cy.get(ERROR)
      .contains(/password/i)
      .should('exist');
  }

  static submit() {
    cy.get("[data-test='login-submit']").click();
  }

  static hasGenericError() {
    cy.get(ERROR).should('contain', 'wrong');
  }

  static hasUsernameOrPasswordError() {
    cy.get(ERROR)
      .contains(/username or password/i)
      .should('exist');
  }
}
