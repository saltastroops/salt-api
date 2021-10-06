const { createConnection } = require("mysql");

/**
 * Update a user's password.
 *
 * The user credentials must be passed as an object with the username and password,
 */
function updateUserPassword(credentials) {
  const { username, password } = credentials;
  const connection = createConnection(process.env["TEST_DATABASE"]);
  const sql = "UPDATE PiptUser SET Password=MD5(?) WHERE Username=?";
  connection.query(sql, [password, username], (err) => {
    if (err) throw err;
  });
}

/**
 * Return a promise with a user's preferred email address.
 */
function getEmailAddress(username) {
  return new Promise((resolve, reject) => {
    const connection = createConnection(process.env["TEST_DATABASE"]);
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

module.exports = {
  updateUserPassword: updateUserPassword,
  getEmailAddress: getEmailAddress,
};
