import "cypress-network-idle";
import {
  HttpResponseInterceptor,
  RouteMatcher,
  StaticResponse,
} from "cypress/types/net-stubbing";

import Chainable = Cypress.Chainable;

const apiUrl = getApiUrl();

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
export function forceNetworkError(url = "/**"): Chainable {
  return cy.intercept(url, { forceNetworkError: true });
}

/**
 * Intercept all HTTP queries so that they give a server error (with status code 500).
 *
 * This function internally uses Cypress' intercept method.
 */
export function forceServerError(url = "/**"): Chainable {
  return cy.intercept(url, {
    statusCode: 500,
    body: { detail: "This is a server error" },
  });
}

/**
 * Intercept all HTTP queries so that they give a not authorized error (with status code 401).
 *
 * This function internally uses Cypress' intercept method.
 */
export function forceAuthenticationError(url = "/**"): Chainable {
  return cy.intercept(url, {
    statusCode: 401,
    body: { detail: "Not Authorized" },
  });
}

/**
 * Intercept all HTTP queries so that they give a forbidden error (with status code 403).
 *
 * This function internally uses Cypress' intercept method.
 */
export function forceForbiddenError(url = "/**"): Chainable {
  return cy.intercept(url, {
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
 * Get API Url.
 */
export function getApiUrl(): string {
  return getEnvVariable("apiUrl");
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
