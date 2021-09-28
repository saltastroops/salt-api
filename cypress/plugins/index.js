const path = require("path");
require("dotenv").config();

const browserify = require("@cypress/browserify-preprocessor");
const cucumber = require("cypress-cucumber-preprocessor").default;
const resolve = require("resolve");
const db = require("./database");

/**
 * @type {Cypress.PluginConfig}
 */
// eslint-disable-next-line no-unused-vars
module.exports = (on, config) => {
  const options = {
    ...browserify.defaultOptions,
    typescript: resolve.sync("typescript", { baseDir: config.projectRoot }),
  };
  on("file:preprocessor", cucumber(options));
  on("task", {
    updateUserPassword(message) {
      return db.updateUserPassword(message);
    },
  });
};
