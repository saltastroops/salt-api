import { storeAccessToken } from '../../src/app/utils';

/**
 * Log in as a user.
 *
 * The user password is updated first.
 */
export function login(username: string) {
  cy.task('updateUserPassword', username)
    .then((password: string) => {
      return cy.request({
        url: 'http://localhost:8001/token',
        method: 'POST',
        form: true,
        body: { username, password },
      });
    })
    .then((response) => {
      const tokenData = response.body;
      storeAccessToken({
        accessToken: tokenData.access_token,
        expiresAt: tokenData.expires_at,
        tokenType: tokenData.token_type,
      });
    });
}

/**
 * Intercept all HTTP queries so that they give a network error.
 *
 * This function internally uses Cypress' intercept method.
 */
export function forceNetworkError() {
  cy.intercept('/**', { forceNetworkError: true });
}

/**
 * Intercept all HTTP queries so that they give a server error (with status code 500).
 *
 * This function internally uses Cypress' intercept method.
 */
export function forceServerError() {
  cy.intercept('/**', {
    statusCode: 500,
    body: { detail: 'This is a server error' },
  });
}
