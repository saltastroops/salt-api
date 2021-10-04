import { storeAccessToken } from '../../src/app/utils';

const userPasswords: Record<string, string> = {};

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
export function updateUserPassword(username: string): any {
  return cy
    .task('updateUserPassword', username)
    .then((password: string) => (userPasswords[username] = password));
}

/**
 * Return a user's password.
 *
 * The password must have been updated with the updateUserPassword function before it
 * can be retrieved with the getUserPassword function.
 *
 * @param username
 */
export function getUserPassword(username: string): string {
  if (!userPasswords.hasOwnProperty(username)) {
    throw new Error(
      `updateUserPassword must be called before you can get the password of ${username}.`
    );
  }
  return userPasswords[username];
}

/**
 * Log in as a user.
 *
 * The user password is updated first.
 */
export function login(username: string) {
  updateUserPassword(username).then((password: string) => {
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
        cy.log(localStorage['accessToken']);
      });
  });
}
