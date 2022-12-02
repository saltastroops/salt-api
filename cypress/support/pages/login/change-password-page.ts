import {
  GENERIC_ERROR_MESSAGE,
  NOT_LOGGED_IN_MESSAGE,
} from "../../../../src/app/utils";

export const CHANGE_PASSWORD_BASE_URL = "/change-password/";

export class ChangePasswordPage {
  static visit(token: string): void {
    cy.visit(CHANGE_PASSWORD_BASE_URL + token);
  }

  static typeNewPassword(password: string): void {
    cy.get("[data-test='change-password-password']").type(password);
  }

  static typeRetypedNewPassword(rePassword: string): void {
    cy.get("[data-test='change-password-retyped-password']").type(rePassword);
  }

  static hasNewPassword(password: string): void {
    cy.get("[data-test='change-password-password']").should(
      "have.value",
      password,
    );
  }

  static hasRetypedNewPassword(retypedPassword: string): void {
    cy.get("[data-test='change-password-retyped-password']").should(
      "have.value",
      retypedPassword,
    );
  }

  static clearNewPassword(): void {
    cy.get("[data-test='change-password-password']").clear();
  }

  static clearRetypedNewPassword(): void {
    cy.get("[data-test='change-password-retyped-password']").clear();
  }

  static submit(): void {
    cy.get("[data-test='submit-request']").click();
  }

  static changePassword(password: string): void {
    ChangePasswordPage.typeNewPassword(password);
    ChangePasswordPage.typeRetypedNewPassword(password);
    ChangePasswordPage.submit();
  }

  static hasMissingNewPasswordError(): void {
    cy.get("[data-test='password-error']")
      .contains(/cannot be empty/i)
      .should("be.visible");
  }

  static hasMissingRetypedNewPassword(): void {
    cy.get("[data-test='retyped-password-error']")
      .contains(/cannot be empty/i)
      .should("be.visible");
  }

  static hasPasswordMismatchError(): void {
    cy.get("[data-test='error']")
      .contains(/mismatch/i)
      .should("be.visible");
  }

  static hasUnknownUsernameOrEmailError(): void {
    cy.get("[data-test='error']")
      .contains(/unknown/i)
      .should("be.visible");
  }

  static hasGenericError(): void {
    cy.get("[data-test='error']")
      .contains(GENERIC_ERROR_MESSAGE)
      .should("be.visible");
  }

  static hasAuthenticationError(): void {
    cy.get("[data-test='error']")
      .contains(NOT_LOGGED_IN_MESSAGE)
      .should("be.visible");
  }

  static isLoading(): Cypress.Chainable {
    return cy
      .get('[data-test="submit-request"]')
      .should("have.class", "is-loading");
  }

  static isNotLoading(): void {
    cy.get('[data-test="submit-request"]').should(
      "not.have.class",
      "is-loading",
    );
  }
}
