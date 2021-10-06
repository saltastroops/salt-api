require("dotenv").config();

const db = require("./database");

/**
 * @type {Cypress.PluginConfig}
 */
// eslint-disable-next-line no-unused-vars

// The SMTP testing has been adapted from
// https://www.cypress.io/blog/2021/05/11/testing-html-emails-using-cypress/

const ms = require("smtp-tester");

module.exports = (on, config) => {
  // Start the SMTP server on port 7777
  const port = 7777;
  const mailServer = ms.init(port);
  console.log(`Mail server listening on port ${port}`);

  let emailInbox = [];

  //  Process all mails
  mailServer.bind((addr, id, email) => {
    emailInbox.push({
      to: email.headers.to,
      body: email.body,
      html: email.html,
    });
  });

  on("task", {
    getEmailInbox() {
      // cy.task cannot return undefined
      // thus we return null as a fallback
      return [...emailInbox];
    },

    clearEmailInbox() {
      emailInbox = [];
      return null;
    },

    getEmailAddress(username) {
      return db.getEmailAddress(username);
    },

    updateUserPassword(credentials) {
      db.updateUserPassword(credentials);
      return null;
    },
  });
};
