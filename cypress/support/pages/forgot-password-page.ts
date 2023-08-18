import { GENERIC_ERROR_MESSAGE } from "../../../src/app/utils";

export const FORGOT_PASSWORD_URL = "/forgot-password";

export class ForgotPasswordPage {
  static visit(): void {
    cy.visit(FORGOT_PASSWORD_URL);
  }

  static typeUsernameOrEmail(usernameOrEmail: string): void {
    cy.get("[data-test='username-email']").type(usernameOrEmail);
  }

  static hasUsernameOrEmail(usernameOrEmail: string): void {
    cy.get("[data-test='username-email']").should(
      "have.value",
      usernameOrEmail,
    );
  }

  static clearUsernameOrEmail(): void {
    cy.get("[data-test='username-email']").clear();
  }

  static submit(): void {
    cy.get("[data-test='submit-request']").click();
  }

  static requestAgain(): void {
    cy.get("[data-test='request-again']", { timeout: 15000 }).click();
  }

  static hasMissingUsernameOrEmailError(): void {
    cy.get("[data-test='error']")
      .contains(/required/i)
      .should("be.visible");
  }

  static hasUnknownUsernameOrEmailError(): void {
    cy.get("[data-test='error']")
      .should("be.visible")
      .and("contain.text", "Not found");
  }

  static hasGenericError(): void {
    cy.get("[data-test='error']")
      .contains(GENERIC_ERROR_MESSAGE)
      .should("be.visible");
  }

  static hasSuccessMessage(): void {
    cy.get("[data-test='success']", { timeout: 15000 })
      .contains(/has been sent/i)
      .should("exist");
  }
}
