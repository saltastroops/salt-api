import {
  HttpResponseInterceptor,
  RouteMatcher,
  StaticResponse,
} from "cypress/types/net-stubbing";

import { storeAccessToken } from "../../src/app/utils";

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
        url: "http://localhost:8001/token",
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
