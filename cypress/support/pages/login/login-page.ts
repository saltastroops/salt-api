import { GENERIC_ERROR_MESSAGE } from "../../../../src/app/utils";

export const LOGIN_URL = "/login";

const USERNAME_INPUT = "[data-test='login-username']";
const PASSWORD_INPUT = "[data-test='login-password']";
const ERROR = "[data-test='error']";

export class LoginPage {
  static visit(): void {
    cy.visit(LOGIN_URL);
  }

  static typeUsername(username: string): void {
    cy.get(USERNAME_INPUT).type(username);
  }

  static clearUsername(): void {
    cy.get(USERNAME_INPUT).clear();
  }

  static hasUsernameError(): void {
    cy.get(ERROR)
      .contains(/username/i)
      .should("be.visible");
  }

  static typePassword(password: string): void {
    cy.get(PASSWORD_INPUT).type(password);
  }

  static clearPassword(): void {
    cy.get(PASSWORD_INPUT).clear();
  }

  static login(username: string, password: string): void {
    LoginPage.typeUsername(username);
    LoginPage.typePassword(password);
    LoginPage.submit();
    // wait for login request to finish
    cy.wait("@login");
  }

  static logout(): void {
    cy.get('[data-test="logout"]').click();
  }

  static submit(): void {
    cy.get("[data-test='login-submit']").click();
  }

  static hasPasswordError(): void {
    cy.get(ERROR)
      .contains(/password/i)
      .should("be.visible");
  }

  static hasGenericError(): void {
    cy.get(ERROR).should("contain", GENERIC_ERROR_MESSAGE).and("be.visible");
  }

  static hasUsernameOrPasswordError(): void {
    cy.get(ERROR)
      .contains(/username or password/i)
      .should("be.visible");
  }

  static forgotPasswordLink(): Cypress.Chainable {
    return cy.get("[data-test='forgot-password-link']");
  }
}
