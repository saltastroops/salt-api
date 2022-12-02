import "cypress-network-idle";
import { STATUS_CODES } from "http";
import * as path from "path";

import "./commands";
import {
  disableBrowserCache,
  generateMockPath,
  prepareForNetworkIdle,
  recordedRequestsAliases,
  recordedResponses,
  resetRecordedRequestsAliases,
  resetRecordedResponse,
  saveResponse,
} from "./utils";

// load type definitions for custom commands
/// <reference types="cypress" />
declare global {
  // eslint-disable-next-line @typescript-eslint/no-namespace
  namespace Cypress {
    interface Chainable {
      /**
       * Custom command to intercept and store API response(s), as well as stubbing/mocking the response(s).
       * @example cy.recordHttp('user/**')
       */
      recordHttp(url: string): Chainable<null>;
    }
  }
}

// Taken from https://gist.github.com/TooTallNate/4fd641f820e1325695487dfd883e5285#file-http-error-js
class HTTPError extends Error {
  private statusCode: number;
  constructor(code: number, message: string) {
    super(message || STATUS_CODES[code]);
    this.statusCode = code;
  }
}
export default HTTPError;

const recordHttpConfig = Cypress.env("recordHttpConfig") || {};
const mockIntercepts = recordHttpConfig.mockIntercepts || false;
const mockFilesDirectory = recordHttpConfig.mockFilesDirectory || null;

before(() => {
  if (!mockFilesDirectory) {
    throw new Error(
      "No mock file directory set. \nTo set mock files directory, use environment variable ``mockFilesDirectory``. " +
        "\ne.g. ``cypress run --env recordHttpConfig='{'mockFilesDirectory': 'path/to/directory/'}'``",
    );
  }
});

beforeEach(() => {
  cy.task("clearEmailInbox");

  disableBrowserCache();
  prepareForNetworkIdle();

  resetRecordedResponse();
  resetRecordedRequestsAliases();

  const [currentTestMockDirectory, currentTestMockFilePath] =
    generateMockPath(mockFilesDirectory);

  if (mockIntercepts) {
    const currentTestMockFile = path.join(
      currentTestMockDirectory,
      currentTestMockFilePath,
    );
    cy.task("readJsonFile", currentTestMockFile).then(
      (responses: [{ [key: string]: string }] | null) => {
        if (responses) {
          Object.keys(responses).forEach((key) =>
            saveResponse(key, responses[key]),
          );
        }
      },
    );
  }
});

afterEach(() => {
  if (!mockIntercepts) {
    // first, wait for the alias string to become define
    cy.waitForNetworkIdle("@recordHttp", 2000).then(() => {
      if (recordedRequestsAliases.length > 0) {
        cy.wrap("Wait for all requests")
          .should(() => {
            expect(recordedRequestsAliases).to.have.length.at.least(1);
          })
          .then(() => {
            recordedRequestsAliases.forEach((alias) => {
              // cy.wait(`@${alias}`)
              if (!recordedResponses[alias]) {
                // eslint-disable-next-line @typescript-eslint/ban-ts-comment
                // @ts-ignore
                recordedResponses[alias] = new HTTPError(
                  500,
                  "No response found",
                );
              }
            });
            cy.wrap(recordedResponses).then(
              // eslint-disable-next-line @typescript-eslint/ban-ts-comment
              // @ts-ignore
              (responses: { [key: string]: string[] }) => {
                const [currentTestMockDirectory, currentTestMockFilePath] =
                  generateMockPath(mockFilesDirectory);
                cy.task("createDirectory", currentTestMockDirectory).then(
                  () => {
                    cy.writeFile(
                      path.join(
                        currentTestMockDirectory,
                        currentTestMockFilePath,
                      ),
                      responses,
                    );
                  },
                );
              },
            );
          });
      }
    });
  }
});
