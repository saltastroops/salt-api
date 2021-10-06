import { GENERIC_ERROR_MESSAGE } from '../../../src/app/utils';

export const FORGOT_PASSWORD_URL = '/forgot-password';

export class ForgotPasswordPage {
  static visit() {
    cy.visit(FORGOT_PASSWORD_URL);
  }

  static typeUsernameOrEmail(usernameOrEmail: string) {
    cy.get("[data-test='username-email']").type(usernameOrEmail);
  }

  static clearUsernameOrEmail() {
    cy.get("[data-test='username-email']").clear();
  }

  static submit() {
    cy.get("[data-test='submit-request']").click();
  }

  static hasMissingUsernameOrEmailError() {
    cy.get("[data-test='error']")
      .contains(/required/i)
      .should('be.visible');
  }

  static hasUnknownUsernameOrEmailError() {
    cy.get("[data-test='error']")
      .contains(/unknown/i)
      .should('be.visible');
  }

  static hasGenericError() {
    cy.get("[data-test='error']")
      .contains(GENERIC_ERROR_MESSAGE)
      .should('be.visible');
  }
}
