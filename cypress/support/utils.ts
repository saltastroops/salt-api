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
export function login(username: string) {
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
export function randomPassword() {
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
export function forceNetworkError() {
  cy.intercept("/**", { forceNetworkError: true });
}

/**
 * Intercept all HTTP queries so that they give a server error (with status code 500).
 *
 * This function internally uses Cypress' intercept method.
 */
export function forceServerError() {
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
export function forceAuthenticationError() {
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
export function forceForbiddenError() {
  cy.intercept("/**", {
    statusCode: 403,
    body: { detail: "Forbidden" },
  });
}
