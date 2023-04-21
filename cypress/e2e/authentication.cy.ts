import { ObservationComments } from "../support/components/observation-comments";
import { LoginPage } from "../support/pages/login/login-page";
import {
  PROPOSAL_BASE_URL,
  ProposalPage,
} from "../support/pages/proposal-page";
import { getApiUrl, userDetailsAreStored } from "../support/utils";

const apiUrl = getApiUrl();

const USERNAME = "hettlage";

describe("Authentication", () => {
  beforeEach(() => {
    cy.intercept(apiUrl + "/login").as("login");

    cy.intercept(apiUrl + "/proposals/**").as("proposals");
  });

  it("should handle HTTP requests with a missing authentication cookie", () => {
    cy.task("updateUserPassword", USERNAME).then((password: string) => {
      // When I login
      LoginPage.visit();
      LoginPage.login(USERNAME, password);

      // Then user details are stored
      userDetailsAreStored();

      // And I can load a proposal page
      ProposalPage.visit("2020-2-SCI-043");

      cy.wait("@proposals");

      cy.url().should("contain", PROPOSAL_BASE_URL);

      // And when I then delete the authentication cookie
      cy.clearCookie("secondary_auth_token");

      // And try to add an observation comment
      ObservationComments.addComment("This is a test comment.");

      // Then I get an error message
      ObservationComments.hasSubmissionError("logged in");

      // And the user details are removed
      cy.window()
        .its("sessionStorage")
        .invoke("getItem", "user")
        .should("be.null");
    });
  });

  it("should handle HTTP requests with an invalid authentication cookie", () => {
    cy.task("updateUserPassword", USERNAME).then((password: string) => {
      // When I login
      LoginPage.visit();
      LoginPage.login(USERNAME, password);

      // Then user details are stored
      userDetailsAreStored();

      // And I can load a proposal page
      ProposalPage.visit("2020-2-SCI-043");

      cy.wait("@proposals");

      // And when I then tamper with the authentication token
      cy.setCookie("secondary_auth_token", "asdf");

      // And try to add an observation comment
      ObservationComments.addComment("This is a test comment.");

      // Then I get an error message
      ObservationComments.hasSubmissionError("logged in");

      // And the authentication token and user details are removed
      cy.window()
        .its("sessionStorage")
        .invoke("getItem", "user")
        .should("be.null");
    });
  });

  it("should request the user details when logging in", () => {
    cy.task("updateUserPassword", USERNAME).then((password: string) => {
      // When I login
      LoginPage.visit();
      LoginPage.login(USERNAME, password);

      // Then user details are stored
      userDetailsAreStored();
    });
  });

  it("should request the user details on page load", () => {
    cy.task("updateUserPassword", USERNAME).then((password: string) => {
      // When I login
      LoginPage.visit();
      LoginPage.login(USERNAME, password);

      // And remove the user details again after they have been saved
      cy.window()
        .its("sessionStorage")
        .invoke("getItem", "user")
        .should("not.be.null");
      cy.window().its("sessionStorage").invoke("removeItem", "user");

      // And go to a proposal page
      ProposalPage.visit("2020-2-SCI-043");

      cy.wait("@proposals");

      // Then the proposal page is loaded
      cy.url().should("contain", PROPOSAL_BASE_URL);

      // Then user details are stored
      userDetailsAreStored();
    });
  });

  it("should remove the authentication cookie and user details when the user logs out", () => {
    cy.task("updateUserPassword", USERNAME).then((password: string) => {
      // Ensure the logout link is not hidden because of the screen size
      cy.viewport(1500, 2000);

      // When I login
      LoginPage.visit();
      LoginPage.login(USERNAME, password);

      // Then the authentication cookie and user details are stored
      cy.getCookie("secondary_auth_token").should("not.be.null");
      userDetailsAreStored();

      // And when I log out again
      LoginPage.logout();

      // Then the authentication token and user details are removed
      cy.getCookie("secondary_auth_token").should("be.null");
      cy.window()
        .its("sessionStorage")
        .invoke("getItem", "user")
        .should("be.null");
    });
  });
});
