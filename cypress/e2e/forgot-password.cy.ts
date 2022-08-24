import { recurse } from "cypress-recurse";

import { ForgotPasswordPage } from "../support/pages/forgot-password-page";
import { ChangePasswordPage } from "../support/pages/login/change-password-page";
import { LoginPage } from "../support/pages/login/login-page";
import { User } from "../support/types";
import {
  forceNetworkError,
  forceServerError,
  getApiUrl,
  randomPassword,
} from "../support/utils";

const apiUrl = getApiUrl();

// load and register the grep feature using "require" function
// https://github.com/cypress-io/cypress-grep
// eslint-disable-next-line @typescript-eslint/no-var-requires
const registerCypressGrep = require("cypress-grep");
registerCypressGrep();

describe("Forgot password page", () => {
  beforeEach(() => {
    cy.recordHttp(apiUrl + "/users/**").as("users");
    ForgotPasswordPage.visit();
  });

  it("should show an error if the form is submitted without input", () => {
    ForgotPasswordPage.submit();
    ForgotPasswordPage.hasMissingUsernameOrEmailError();
  });

  it("should show an error if a username or email address is input and then deleted again", () => {
    ForgotPasswordPage.typeUsernameOrEmail("someone");
    ForgotPasswordPage.clearUsernameOrEmail();
    ForgotPasswordPage.hasMissingUsernameOrEmailError();
  });

  it("should show an error if there is a network error", () => {
    forceNetworkError();
    ForgotPasswordPage.typeUsernameOrEmail("someone@example.com");
    ForgotPasswordPage.submit();
    ForgotPasswordPage.hasGenericError();
  });

  it("should show an error if there is a server error", () => {
    forceServerError();
    ForgotPasswordPage.typeUsernameOrEmail("someone@example.com");
    ForgotPasswordPage.submit();
    ForgotPasswordPage.hasGenericError();
  });

  it("should show an error if a non-existing username or email address is submitted", () => {
    ForgotPasswordPage.typeUsernameOrEmail("unknown-user");
    ForgotPasswordPage.submit();
    ForgotPasswordPage.hasUnknownUsernameOrEmailError();
  });

  it("should display a confirmation message", () => {
    const USERNAME = "hettlage";
    ForgotPasswordPage.typeUsernameOrEmail(USERNAME);
    ForgotPasswordPage.submit();
    ForgotPasswordPage.hasSuccessMessage();
  });

  it("should have the input field prepopulated when an email is requested again", () => {
    const USERNAME = "hettlage";
    ForgotPasswordPage.typeUsernameOrEmail(USERNAME);
    ForgotPasswordPage.submit();
    ForgotPasswordPage.requestAgain();
    ForgotPasswordPage.hasUsernameOrEmail(USERNAME);
  });

  // eslint-disable-next-line @typescript-eslint/ban-ts-comment
  // @ts-ignore
  it(
    "should send an email with the correct password reset link",
    { tags: "@skip" },
    () => {
      // When I request a password reset email
      const USERNAME = "hettlage";
      ForgotPasswordPage.typeUsernameOrEmail(USERNAME);
      ForgotPasswordPage.submit();
      recurse(
        () => cy.task("getEmailInbox"),
        (emails: Array<any>) => {
          // A boolean (not just a truthy value) must be returned
          return !!emails.length;
        },
        { log: false, delay: 1000, timeout: 20000 },
      ).as("emails");

      // Then one email is sent
      cy.get("@emails").should("have.length", 1);

      // And it is sent to the correct email address
      cy.task("getUser", USERNAME).then((user: User) => {
        cy.get("@emails").then((emails: any) => {
          expect(emails[0].to).to.contain(user.email);
        });
      });

      // And the email contains a link both in plain text and in html
      cy.get("@emails")
        .then((emails: any) => {
          const LINK_REGEX = /\bhttps?:\/\/[^\s"]+/;
          const email = emails[0];
          const linkInBody = LINK_REGEX.exec(email.body)[0];
          const linkInHtml = LINK_REGEX.exec(email.html)[0];
          expect(linkInBody).to.equal(linkInHtml);

          return linkInBody;
        })
        .then((link: string) => {
          // And when I click on the link I get to the password reset page
          cy.visit(link);
          cy.url().should("contain", "change-password");

          // And when I then request a password change
          const password = randomPassword();
          ChangePasswordPage.changePassword(password);

          // I get to the login page
          cy.url().should("contain", "login");

          // And when I enter my username and new password
          LoginPage.login(USERNAME, password);

          // I am logged in
          cy.url().should("not.contain", "login");
        });
    },
  );
});
