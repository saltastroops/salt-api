// eslint-disable-next-line @typescript-eslint/no-var-requires
const { createConnection } = require("mysql");

const recordHttpConfig = process.env.CYPRESS_recordHttpConfig || {};
const mockIntercepts = recordHttpConfig["mockIntercepts"] || false;

/**
 * Update a user's password.
 *
 * A random string is chosen as the new password. The function returns a promise which
 * resolves to the new password.
 */
export function updateUserPassword(username: string): Promise<string> {
  return new Promise((resolve, reject) => {
    // Taken from https://gist.github.com/6174/6062387
    const password =
      Math.random().toString(36).substring(2, 15) +
      Math.random().toString(36).substring(2, 15);

    if (mockIntercepts) {
      resolve(password)
    } else {
      const connection = createConnection(process.env["TEST_DATABASE"]);
      const sql = "UPDATE PiptUser SET Password=MD5(?) WHERE Username=?";
      connection.query(sql, [password, username], (error) => {
        if (error) {
          reject(error);
          return;
        }
        resolve(password);
      });
    }
  });
}

/**
 * Return a promise with a user's preferred details.
 */
export function getUser(username: string): Promise<unknown> {
  return new Promise((resolve, reject) => {
    if (mockIntercepts) {
      resolve(username)
    } else {
      const connection = createConnection(process.env["TEST_DATABASE"]);
      const sql = `
      SELECT FirstName AS first_name, Surname AS surname, Email AS email
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
        const user = {
          givenName: results[0].first_name,
          familyName: results[0].surname,
          email: results[0].email,
        };
        resolve(user);
      });
    }
  });
}

/**
 * Delete all observation comments for a proposal.
 */
export function clearObservationComments(
  proposalCode: string,
): Promise<boolean> {
  return new Promise((resolve, reject) => {
    if (mockIntercepts) {
      resolve(true)
    } else {
      const connection = createConnection(process.env["TEST_DATABASE"]);
      const sql = `
      DELETE
      FROM ProposalComment
      WHERE ProposalCode_Id = (SELECT ProposalCode_Id FROM ProposalCode WHERE Proposal_Code = ?)
    `;
      connection.query(sql, [proposalCode], (error) => {
        if (error) {
          reject(error);
          return;
        }
        resolve(true);
      });
    }
  });
}
