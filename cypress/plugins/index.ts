require('dotenv').config();

const axios = require('axios');
const ms = require('smtp-tester');

import { getEmailAddress, updateUserPassword } from './database';

/**
 * @type {Cypress.PluginConfig}
 */
// eslint-disable-next-line no-unused-vars

// The SMTP testing has been adapted from
// https://www.cypress.io/blog/2021/05/11/testing-html-emails-using-cypress/

export default (on, config) => {
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

  on('task', {
    /**
     * Return an array with all the sent emails.
     *
     * Every email is an object with three properties:
     *
     * - to: The email address, possibly including a name. Example: John Doe
     *       <john@example.com>
     * - body: Plain text content of the email.
     * - html: HTML content of the email.
     */
    getEmailInbox() {
      // cy.task cannot return undefined
      // thus we return null as a fallback
      return [...emailInbox];
    },

    /**
     * Clear all the sent emails.
     */
    clearEmailInbox() {
      emailInbox = [];
      return null;
    },

    /**
     * Return a promise with a user's email address.
     */
    getEmailAddress(username) {
      return getEmailAddress(username);
    },

    /**
     * Update a user's password and return a promise with the new password.
     */
    updateUserPassword(username) {
      return updateUserPassword(username);
    },
  });
};
