const { createConnection } = require("mysql");

function updateUserPassword(credentials) {
  const { username, password } = credentials;
  const connection = createConnection(process.env["TEST_DATABASE"]);
  const sql = "UPDATE PiptUser SET Password=MD5(?) WHERE Username=?";
  connection.query(sql, [password, username], (err) => {
    if (err) throw err;
  });
}

module.exports = {
  updateUserPassword: updateUserPassword,
};
