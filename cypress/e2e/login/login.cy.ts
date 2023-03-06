import { passBoolean } from "protractor/built/util";

import { NavigationBar } from "../../support/components/navigation-bar";
import { FORGOT_PASSWORD_URL } from "../../support/pages/forgot-password-page";
import { HomePage } from "../../support/pages/home-page";
import { LOGIN_URL, LoginPage } from "../../support/pages/login/login-page";
import {
  PROPOSAL_BASE_URL,
  ProposalPage,
} from "../../support/pages/proposal-page";
import {
  forceNetworkError,
  forceServerError,
  getApiUrl,
  randomPassword,
} from "../../support/utils";

const apiUrl = getApiUrl();

const USERNAME = "hettlage";

describe("Login page", () => {
  beforeEach(() => {
    cy.recordHttp(apiUrl + "/login").as("login");

    cy.recordHttp(apiUrl + "/logout").as("logout");

    cy.recordHttp(apiUrl + "/user").as("user");

    cy.recordHttp(apiUrl + "/proposals/**").as("proposals");

    cy.recordHttp(apiUrl + "/blocks/**").as("blocks");
    LoginPage.visit();
  });

  it("should give an error for a missing username", () => {
    LoginPage.typePassword("secret");
    LoginPage.submit();
    LoginPage.hasUsernameError();
  });

  it("should give an error for a missing password", () => {
    LoginPage.typeUsername("someone");
    LoginPage.submit();
    LoginPage.hasPasswordError();
  });

  it("should give an error after the username is removed again", () => {
    LoginPage.typeUsername("someone");
    LoginPage.clearUsername();
    LoginPage.hasUsernameError();
  });

  it("should give an error after the password is removed again", () => {
    LoginPage.typePassword("secret");
    LoginPage.clearPassword();
    LoginPage.hasPasswordError();
  });

  it("should give an error if there is a server error", () => {
    cy.task("updateUserPassword", USERNAME).then((password: string) => {
      forceServerError();
      LoginPage.typeUsername(USERNAME);
      LoginPage.typePassword(password);
      LoginPage.submit();
      LoginPage.hasGenericError();
    });
  });

  it("should give an error if there is a network error", () => {
    cy.task("updateUserPassword", USERNAME).then((password: string) => {
      forceNetworkError();
      LoginPage.typeUsername(USERNAME);
      LoginPage.typePassword(password);
      LoginPage.submit();
      LoginPage.hasGenericError();
    });
  });

  it("should give an error if you login with an incorrect password", () => {
    LoginPage.login(USERNAME, "incorrect");
    LoginPage.hasUsernameOrPasswordError();
  });

  it("should log you in if you use the correct username and password", () => {
    cy.url().should("contain", LOGIN_URL);
    cy.task("updateUserPassword", USERNAME).then((password: string) => {
      LoginPage.typeUsername(USERNAME);
      LoginPage.typePassword(password);
      LoginPage.submit();
      cy.url().should("not.contain", LOGIN_URL);
    });
  });

  it.only("should handle logging in again after an error", () => {
    cy.task("updateUserPassword", USERNAME).then((password: string) => {
      // Ensure the inline login form is not hidden because of a small screen size
      cy.viewport(1500, 2000);

      let serverDown = false;

      cy.intercept(apiUrl + "/**", (req) => {
        if (serverDown) {
          return req.reply({ statusCode: 500, body: { message: "Server ." } });
        }
        req.continue();
      });

      // When go the home page
      HomePage.visit();

      // And login
      NavigationBar.typeUsername(USERNAME);
      NavigationBar.typePassword(password);
      NavigationBar.submitLogin();

      // I get to the home page for logged-in users
      cy.get('[data-test="home-page-user"]')
        .should("exist")
        .then(() => {
          // When I now stop the backend server
          serverDown = true;
        });

      // And reload the page
      HomePage.visit();

      // And try to log in
      // The username and password are still filled in from the previous login attempt
      NavigationBar.submitLogin();

      // Then I get to the home page for non-logged-in users
      cy.get('[data-test="home-page-guest"]')
        .should("exist")
        .then(() => {
          // When I now restart the backend server
          serverDown = false;
        });

      // And try to log in
      NavigationBar.typeUsername(USERNAME);
      NavigationBar.typePassword(password);
      NavigationBar.submitLogin();

      // Then I get to the home page for logged-in users
      cy.get('[data-test="home-page-user"]').should("exist");
    });
  });

  it("should redirect to another page if you are logged in already", () => {
    cy.task("updateUserPassword", USERNAME).then((password: string) => {
      LoginPage.login(USERNAME, password);
      cy.url().should("not.contain", LOGIN_URL);
    });
  });

  it("should take me to the originally requested page after logging in", () => {
    // When I'm not logged in
    // And I go to a proposal page
    // Then I'm redirected to the login page
    // And when I then login
    // Then I'm redirected to the originally requested proposal page
    ProposalPage.visit("2020-2-SCI-043");
    cy.url().should("not.contain", PROPOSAL_BASE_URL);
    cy.task("updateUserPassword", USERNAME).then((password: string) => {
      LoginPage.typeUsername(USERNAME);
      LoginPage.typePassword(password);
      LoginPage.submit();
      cy.url().should("contain", PROPOSAL_BASE_URL);
    });
  });

  it("should link to the password reset page", () => {
    LoginPage.forgotPasswordLink().click();
    cy.url().should("contain", FORGOT_PASSWORD_URL);
  });
});
