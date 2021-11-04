import { GENERIC_ERROR_MESSAGE } from '../../../src/app/utils';

export const HOME_URL = '/';

const WELCOME_MESSAGE = '[data-test="welcome-message"]';
const INLINE_LOGIN_ERROR = '[data-test="inline-login-error"]';
const INLINE_LOGIN_SUBMIT = '[data-test="inline-login-submit"]';

export class NavigationBar {
  static typeUsername(username: string) {
    cy.get('[data-test="inline-login-username"]').type(username);
  }

  static typePassword(password: string) {
    cy.get('[data-test="inline-login-password"]').type(password);
  }

  static submitLogin() {
    cy.get(INLINE_LOGIN_SUBMIT).click();
  }

  static hasUsernameError() {
    cy.get(INLINE_LOGIN_ERROR)
      .contains(/username/i)
      .should('be.visible');
  }

  static hasPasswordError() {
    cy.get(INLINE_LOGIN_ERROR)
      .contains(/password/i)
      .should('be.visible');
  }

  static hasUsernameOrPasswordError() {
    cy.get(INLINE_LOGIN_ERROR)
      .contains(/username or password/i)
      .should('be.visible');
  }

  static hasGenericLoginError() {
    cy.get(INLINE_LOGIN_ERROR)
      .contains(GENERIC_ERROR_MESSAGE)
      .should('be.visible');
  }

  static hasNoLoginForm() {
    cy.get('inline-login').should('not.exist');
  }

  static loginIsLoading() {
    return cy
      .get(INLINE_LOGIN_SUBMIT)
      .should('have.class', 'is-loading')
      .and('be.disabled');
  }

  static loginIsNotLoading() {
    return cy
      .get(INLINE_LOGIN_SUBMIT)
      .should('not.have.class', 'is-loading')
      .and('not.be.disabled');
  }

  static hasWelcomeMessage(text: string) {
    cy.get(WELCOME_MESSAGE).should('be.visible').and('contain', text);
  }

  static hasNoWelcomeMessage() {
    return cy.get(WELCOME_MESSAGE).should('not.exist');
  }
}
