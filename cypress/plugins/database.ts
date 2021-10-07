const { createConnection } = require('mysql');

/**
 * Update a user's password.
 *
 * A random string is chosen as the new password. The function returns a promise which
 * resolves to the new password.
 */
export function updateUserPassword(username) {
  return new Promise((resolve, reject) => {
    // Taken from https://gist.github.com/6174/6062387
    const password =
      Math.random().toString(36).substring(2, 15) +
      Math.random().toString(36).substring(2, 15);

    const connection = createConnection(process.env['TEST_DATABASE']);
    const sql = 'UPDATE PiptUser SET Password=MD5(?) WHERE Username=?';
    connection.query(sql, [password, username], (error) => {
      if (error) {
        reject(error);
        return;
      }
      resolve(password);
    });
  });
}

/**
 * Return a promise with a user's preferred email address.
 */
export function getEmailAddress(username) {
  return new Promise((resolve, reject) => {
    const connection = createConnection(process.env['TEST_DATABASE']);
    const sql = `
      SELECT Email AS email
      FROM Investigator I
             JOIN PiptUser PU ON I.Investigator_Id = PU.Investigator_Id
      WHERE PU.Username = ?
    `;
    connection.query(sql, [username], (error, results) => {
      if (error) {
        reject(error);
        return;
      }
      if (!results.length) {
        reject(`Unknown username: ${username}`);
        return;
      }
      resolve(results[0].email);
    });
  });
}
