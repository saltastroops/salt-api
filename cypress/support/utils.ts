import "cypress-network-idle";
import {
  HttpResponseInterceptor,
  RouteMatcher,
  StaticResponse,
} from "cypress/types/net-stubbing";
import { PathLike } from "fs";
import * as path from "path";

import { storeAccessToken } from "../../src/app/utils";

export let recordedResponses;
export let recordedRequestsAliases;

/**
 * Get an environment variable.
 *
 * An error is raised if the environment variable is not set.
 */
export function getEnvVariable(name: string): string {
  const value = Cypress.env(name);
  if (value === undefined) {
    throw new Error(
      "Environment variable not set: " +
        name +
        "\n\n" +
        "You can set an environment variable in the file " +
        "cypress.env.json or by passing it with the --env " +
        "command line option (e.g., --env " +
        name +
        '="abc").',
    );
  }
  return value;
}

/**
 * Reset a dictionary of recorded responses.
 */
export function resetRecordedResponse(): void {
  recordedResponses = {};
}

/**
 * Reset a list of recorded aliases.
 */
export function resetRecordedRequestsAliases(): void {
  recordedRequestsAliases = [];
}

/**
 * Save alias to list.
 */
export function saveAlias(key: string): void {
  recordedRequestsAliases.push(key);
}

/**
 * Function for delaying a request until it is explicitly triggered.
 *
 * Taken from https://blog.dai.codes/cypress-loading-state-tests/.
 */
export function interceptIndefinitely(
  requestMatcher: RouteMatcher,
  response?: StaticResponse | HttpResponseInterceptor,
): { sendResponse: () => void } {
  let sendResponse;
  const trigger = new Promise((resolve) => {
    sendResponse = resolve;
  });
  cy.intercept(requestMatcher, (request) => {
    return trigger.then(() => {
      request.reply(response);
    });
  });
  return { sendResponse };
}

/**
 * Log in as a user.
 *
 * The user password is updated first.
 */
export function login(username: string): void {
  cy.task("updateUserPassword", username)
    .then((password: string) => {
      return cy.request({
        url: "http://127.0.0.1:8001/token",
        method: "POST",
        form: true,
        body: { username, password },
      });
    })
    .then((response) => {
      const tokenData = response.body;
      storeAccessToken({
        accessToken: tokenData.access_token,
        expiresAt: tokenData.expires_at,
        tokenType: tokenData.token_type,
      });
    });
}

/**
 * Generate a random password.
 */
export function randomPassword(): string {
  // Taken from https://gist.github.com/6174/6062387
  return (
    Math.random().toString(36).substring(2, 15) +
    Math.random().toString(36).substring(2, 15)
  );
}

/**
 * Intercept all HTTP queries so that they give a network error.
 *
 * This function internally uses Cypress' intercept method.
 */
export function forceNetworkError(): void {
  cy.intercept("/**", { forceNetworkError: true });
}

/**
 * Intercept all HTTP queries so that they give a server error (with status code 500).
 *
 * This function internally uses Cypress' intercept method.
 */
export function forceServerError(): void {
  cy.intercept("/**", {
    statusCode: 500,
    body: { detail: "This is a server error" },
  });
}

/**
 * Intercept all HTTP queries so that they give a not authorized error (with status code 401).
 *
 * This function internally uses Cypress' intercept method.
 */
export function forceAuthenticationError(): void {
  cy.intercept("/**", {
    statusCode: 401,
    body: { detail: "Not Authorized" },
  });
}

/**
 * Intercept all HTTP queries so that they give a forbidden error (with status code 403).
 *
 * This function internally uses Cypress' intercept method.
 */
export function forceForbiddenError(): void {
  cy.intercept("/**", {
    statusCode: 403,
    body: { detail: "Forbidden" },
  });
}

/**
 * Override native global functions related to time.
 *
 * This function overrides the current datetime of the test setup.
 */
export function freezeDate(year: number, month: number): void {
  const now = new Date(year, month);
  cy.clock(now, ["Date"]);

  // override Date class methods to return the same year and month
  Date.prototype.getFullYear = () => {
    return year;
  };
  Date.prototype.getMonth = () => {
    return month;
  };
}

/**
 * Generate mock directory path.
 */
export function generateMockPath(directoryPath: PathLike): string[] {
  const currentTestTitle = Cypress.currentTest.title;
  const currentTestFile = path
    .basename(Cypress.spec.name.toString())
    .split(".")[0];
  const currentTestFileDirTree = path
    .dirname(Cypress.spec.relative)
    .split(path.sep)
    .slice(2);
  const mockFile =
    "test-" + currentTestTitle.toString().split(" ").join("-") + ".json";
  return [
    path.join(
      directoryPath.toString(),
      currentTestFileDirTree.join(path.sep),
      currentTestFile.toString().split(" ").join("-"),
    ),
    mockFile,
  ];
}

/**
 * Save response to a dictionary.
 */
export function saveResponse(key: string, response: string): void {
  recordedResponses[key] = response;
}

/**
 * Get the next recorded/stored responses.
 */
export function getResponse(key: string): string {
  return recordedResponses[key];
}

/**
 * Get API Url.
 */
export function getApiUrl(): string {
  return getEnvVariable("apiUrl");
}

/**
 * Disable and/or clear the browser cache.
 */
export function disableBrowserCache(): void {
  // Taken from https://docs.cypress.io/api/commands/intercept#Stubbing-a-response
  cy.intercept(
    { url: getApiUrl() + "/**/*", middleware: true },
    // Delete 'if-none-match' header from all outgoing requests
    (req) => {
      delete req.headers["if-none-match"];

      req.on("before:response", (res) => {
        // force all API responses to not be cached
        res.headers["cache-control"] = "no-store";
      });
    },
  );
}

/**
 * Prepare to capture network calls.
 */
export function prepareForNetworkIdle(): void {
  cy.waitForNetworkIdlePrepare({
    method: "*",
    pattern: getApiUrl() + "/**",
    alias: "recordHttp",
  });
}

/**
 * Check that user details are stored in session storage.
 */
export function userDetailsAreStored(): void {
  cy.window()
    .its("sessionStorage")
    .invoke("getItem", "user")
    .should("not.be.null");
}