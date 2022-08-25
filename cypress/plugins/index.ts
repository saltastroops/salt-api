import { PathLike } from "fs";

import {
  clearObservationComments,
  getUser,
  updateUserPassword,
} from "./database";

// eslint-disable-next-line @typescript-eslint/no-var-requires
require("dotenv").config();

// eslint-disable-next-line @typescript-eslint/no-var-requires
const ms = require("smtp-tester");

// eslint-disable-next-line @typescript-eslint/no-var-requires
const fs = require("fs");

// eslint-disable-next-line @typescript-eslint/no-var-requires
const usernames = require("../salt-testdata/usernames.json");

/**
 * @type {Cypress.PluginConfig}
 */
// eslint-disable-next-line no-unused-vars

// The SMTP testing has been adapted from
// https://www.cypress.io/blog/2021/05/11/testing-html-emails-using-cypress/

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export default (on, config): void => {
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

  const recordHttpConfig = JSON.parse(
    process.env.CYPRESS_recordHttpConfig || "{}",
  );
  const mockIntercepts = recordHttpConfig["mockIntercepts"] || false;
console.log(Object.keys(usernames));
  for (const key in Object.keys(JSON.parse(usernames))) {
    // console.log(JSON.parse(usernames)[key]);
    config.env[key] = JSON.parse(usernames)[key];
  }

  on("task", {
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
     * Clear all sent emails.
     */
    clearEmailInbox() {
      emailInbox = [];
      return null;
    },

    /**
     * Return a promise with user details
     */
    getUser(username) {
      if (mockIntercepts) {
        return username;
      }
      return getUser(username);
    },

    /**
     * Update a user's password and return a promise with the new password.
     */
    updateUserPassword(username) {
      if (mockIntercepts) {
        return (
          Math.random().toString(36).substring(2, 15) +
          Math.random().toString(36).substring(2, 15)
        );
      }
      return updateUserPassword(username);
    },

    /**
     * Delete all observation comments for a proposal.
     */
    clearObservationComments(proposalCode: string) {
      if (mockIntercepts) {
        return true;
      }
      return clearObservationComments(proposalCode);
    },

    /**
     * Read a file with JSON content and return its content as an object.
     */
    readJsonFile(filePath: PathLike) {
      if (!fs.existsSync(filePath)) {
        return null;
      }
      return JSON.parse(fs.readFileSync(filePath, "utf8"));
    },

    /**
     * Create a directory and any non-existing parent directories.
     */
    createDirectory(filePath: PathLike) {
      if (!fs.existsSync(filePath)) {
        fs.mkdirSync(filePath, { recursive: true });
      }
      return null;
    },
  });
};
