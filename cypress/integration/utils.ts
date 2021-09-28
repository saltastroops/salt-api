const userPasswords: Record<string, string> = {};

/**
 * Update the user password in the database.
 *
 * A random string is chosen as the new password, which can be retrieved by means of the
 * getUserPassword function.
 *
 * @param username
 */
export function updateUserPassword(username: string): void {
  cy.task('updateUserPassword', username).then(
    (password: string) => (userPasswords[username] = password)
  );
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
