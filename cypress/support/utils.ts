import { storeAccessToken } from '../../src/app/utils';

/**
 * Update the user password in the database.
 *
 * A random string is chosen as the new password, which can be retrieved by means of the
 * getUserPassword function.
 *
 * The function internally calls cy.task and returns the return value, which is
 * effectively a promise. In other words, the function is asynchronous in nature, and
 * you should remember that you cannot access the new password until the promise has
 * been resolved. See the login function for an example of dealing with the asynchronous
 * nature.
 *
 * @param username
 */
export function updateUserPassword(username: string): string {
  const { password } = _updateUserPassword(username);

  return password;
}

function _updateUserPassword(username: string) {
  // Taken from https://gist.github.com/6174/6062387
  const password =
    Math.random().toString(36).substring(2, 15) +
    Math.random().toString(36).substring(2, 15);
  return {
    password,
    updatePromise: cy.task('updateUserPassword', { username, password }),
  };
}

/**
 * Log in as a user.
 *
 * The user password is updated first.
 */
export function login(username: string) {
  const { password, updatePromise } = _updateUserPassword(username);
  updatePromise.then(() => {
    return cy
      .request({
        url: 'http://localhost:8001/token',
        method: 'POST',
        form: true,
        body: { username, password },
      })
      .then((response) => {
        const tokenData = response.body;
        storeAccessToken({
          accessToken: tokenData.access_token,
          expiresAt: tokenData.expires_at,
          tokenType: tokenData.token_type,
        });
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
