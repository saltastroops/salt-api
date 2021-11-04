import { GENERIC_ERROR_MESSAGE } from '../../../src/app/utils';

export const HOME_URL = '/';

const WELCOME_MESSAGE = '[data-test="welcome-message"]';
const INLINE_LOGIN_ERROR = '[data-test="inline-login-error"]';
const INLINE_LOGIN_SUBMIT = '[data-test="inline-login-submit"]';

export class HomePage {
  static visit() {
    cy.visit(HOME_URL);
  }
}
