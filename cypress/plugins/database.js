const { createConnection } = require("mysql");

function updateUserPassword(username) {
  const connection = createConnection(process.env["TEST_DATABASE"]);
  const sql = "UPDATE PiptUser SET Password=MD5(?) WHERE Username=?";
  // Taken from https://gist.github.com/6174/6062387
  const password =
    Math.random().toString(36).substring(2, 15) +
    Math.random().toString(36).substring(2, 15);
  connection.query(sql, [password, username], (err) => {
    if (err) throw err;
  });

  return password;
}

module.exports = {
  updateUserPassword: updateUserPassword,
};
