require("dotenv").config();

const db = require("./database");

/**
 * @type {Cypress.PluginConfig}
 */
// eslint-disable-next-line no-unused-vars
module.exports = (on, config) => {
  on("task", {
    updateUserPassword(credentials) {
      db.updateUserPassword(credentials);
      return null;
    },
  });
};
