import { GENERIC_ERROR_MESSAGE } from "../../../src/app/utils";

export const FORGOT_PASSWORD_URL = "/forgot-password";

export class ForgotPasswordPage {
  static visit() {
    cy.visit(FORGOT_PASSWORD_URL);
  }

  static typeUsernameOrEmail(usernameOrEmail: string) {
    cy.get("[data-test='username-email']").type(usernameOrEmail);
  }

  static hasUsernameOrEmail(usernameOrEmail: string) {
    cy.get("[data-test='username-email']").should(
      "have.value",
      usernameOrEmail,
    );
  }

  static clearUsernameOrEmail() {
    cy.get("[data-test='username-email']").clear();
  }

  static submit() {
    cy.get("[data-test='submit-request']").click();
  }

  static requestAgain() {
    cy.get("[data-test='request-again']", { timeout: 15000 }).click();
  }

  static hasMissingUsernameOrEmailError() {
    cy.get("[data-test='error']")
      .contains(/required/i)
      .should("be.visible");
  }

  static hasUnknownUsernameOrEmailError() {
    cy.get("[data-test='error']")
      .contains(/didn't match/i)
      .should("be.visible");
  }

  static hasGenericError() {
    cy.get("[data-test='error']")
      .contains(GENERIC_ERROR_MESSAGE)
      .should("be.visible");
  }

  static hasSuccessMessage() {
    cy.get("[data-test='success']", { timeout: 15000 })
      .contains(/has been sent/i)
      .should("exist");
  }
}
