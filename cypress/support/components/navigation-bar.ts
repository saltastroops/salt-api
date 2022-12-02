import { GENERIC_ERROR_MESSAGE } from "../../../src/app/utils";

export const HOME_URL = "/";

const WELCOME_MESSAGE = '[data-test="welcome-message"]';
const INLINE_LOGIN_ERROR = '[data-test="inline-login-error"]';
const INLINE_LOGIN_SUBMIT = '[data-test="inline-login-submit"]';

const HOME_TAB = '[data-test="home-tab"]';
const SO_PAGE_TAB = '[data-test="so-page-tab"]';
const SA_PAGES_TAB = '[data-test="sa-pages-tab"]';
const OPTIONS_TAB = '[data-test="options-tab"]';
const GRAVITATIONAL_WAVES_TAB = '[data-test="gravitational-waves-tab"]';
const ADMIN_TAB = '[data-test="admin-tab"]';

export class NavigationBar {
  static typeUsername(username: string): void {
    cy.get('[data-test="inline-login-username"]').type(username);
  }

  static typePassword(password: string): void {
    cy.get('[data-test="inline-login-password"]').type(password);
  }

  static submitLogin(): void {
    cy.get(INLINE_LOGIN_SUBMIT).click();
  }

  static hasUsernameError(): void {
    cy.get(INLINE_LOGIN_ERROR)
      .contains(/username/i)
      .should("be.visible");
  }

  static hasPasswordError(): void {
    cy.get(INLINE_LOGIN_ERROR)
      .contains(/password/i)
      .should("be.visible");
  }

  static hasUsernameOrPasswordError(): void {
    cy.get(INLINE_LOGIN_ERROR)
      .contains(/username or password/i)
      .should("be.visible");
  }

  static hasGenericLoginError(): void {
    cy.get(INLINE_LOGIN_ERROR)
      .contains(GENERIC_ERROR_MESSAGE)
      .should("be.visible");
  }

  static hasNoLoginForm(): void {
    cy.get("inline-login").should("not.exist");
  }

  static loginIsLoading(): Cypress.Chainable {
    return cy
      .get(INLINE_LOGIN_SUBMIT)
      .should("have.class", "is-loading")
      .and("be.disabled");
  }

  static loginIsNotLoading(): Cypress.Chainable {
    return cy
      .get(INLINE_LOGIN_SUBMIT)
      .should("not.have.class", "is-loading")
      .and("not.be.disabled");
  }

  static hasWelcomeMessage(text: string): void {
    cy.get(WELCOME_MESSAGE).should("be.visible").and("contain", text);
  }

  static hasNoWelcomeMessage(): void {
    cy.get(WELCOME_MESSAGE).should("not.exist");
  }

  static hasHomeTab(): void {
    cy.get(HOME_TAB).should("be.visible");
  }
  static hasNoHomeTab(): void {
    cy.get(HOME_TAB).should("not.exist");
  }
  static hasSOPageTab(): void {
    cy.get(SO_PAGE_TAB).should("be.visible");
  }
  static hasNoSOPageTab(): void {
    cy.get(SO_PAGE_TAB).should("not.exist");
  }
  static hasSAPagesTab(): void {
    cy.get(SA_PAGES_TAB).should("be.visible");
  }
  static hasNoSAPagesTab(): void {
    cy.get(SA_PAGES_TAB).should("not.exist");
  }
  static hasOptionsTab(): void {
    cy.get(OPTIONS_TAB).should("be.visible");
  }
  static hasNoOptionsTab(): void {
    cy.get(OPTIONS_TAB).should("not.exist");
  }
  static hasAdminTab(): void {
    cy.get(ADMIN_TAB).should("be.visible");
  }
  static hasNoAdminTab(): void {
    cy.get(ADMIN_TAB).should("not.exist");
  }
  static hasGravitationalWavesTab(): void {
    cy.get(GRAVITATIONAL_WAVES_TAB).should("be.visible");
  }
  static hasNoGravitationalWavesTab(): void {
    cy.get(GRAVITATIONAL_WAVES_TAB).should("not.exist");
  }
}
