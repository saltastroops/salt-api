import {
  FORBIDDEN_MESSAGE,
  GENERIC_ERROR_MESSAGE,
  NOT_LOGGED_IN_MESSAGE,
} from "../../../src/app/utils";
import { ObservationComments } from "../../support/components/observation-comments";
import { LoginPage } from "../../support/pages/login/login-page";
import { ProposalPage } from "../../support/pages/proposal-page";
import {
  forceAuthenticationError,
  forceForbiddenError,
  forceNetworkError,
  forceServerError,
  getApiUrl,
} from "../../support/utils";

const apiUrl = getApiUrl();

const USERNAME = "hettlage";

describe("Observation comments", () => {
  const PROPOSAL_CODE = "2020-1-SCI-007";

  beforeEach(() => {
    cy.intercept(apiUrl + "/login").as("login");

    cy.intercept(apiUrl + "/proposals/**").as("proposals");

    cy.task("updateUserPassword", USERNAME).then((password: string) => {
      // When I login
      LoginPage.visit();
      LoginPage.login(USERNAME, password);
    });

    // And I visit a proposal page
    ProposalPage.visit(PROPOSAL_CODE);

    cy.wait("@proposals");
  });

  it("should show an error if all typed comment text is removed again", () => {
    // When I start adding a new comment
    ObservationComments.startNewComment();

    // Then the button for adding a new comment is disabled
    ObservationComments.hasDisabledAddCommentButton(true);

    // Then there is no error
    ObservationComments.hasNoCommentError();
    ObservationComments.hasNoSubmissionError();

    // And type some comment text
    ObservationComments.typeComment("This is a test comment.");

    // And remove the text again
    ObservationComments.clearCommentText();

    // Then an error is displayed
    ObservationComments.hasCommentError();
    ObservationComments.hasNoSubmissionError();

    // And when I type some text again
    ObservationComments.typeComment("A");

    // Then there is no error any longer
    ObservationComments.hasNoCommentError();
    ObservationComments.hasNoSubmissionError();

    // And the button for adding a new comment is still disabled
    ObservationComments.hasDisabledAddCommentButton(true);

    // And the other buttons are enabled
    ObservationComments.hasDisabledSubmitButton(false);
    ObservationComments.hasDisabledCancelButton(false);
  });

  it("should show an error if no comment text is submitted", () => {
    // When I start adding a new comment
    ObservationComments.startNewComment();

    // Then the button for adding a new comment is disabled
    ObservationComments.hasDisabledAddCommentButton(true);

    // And when I submit without a comment text
    ObservationComments.submitComment();

    // Then an error is displayed
    ObservationComments.hasCommentError();

    // And the button for adding a new comment is still disabled
    ObservationComments.hasDisabledAddCommentButton(true);

    // And the other buttons are enabled
    ObservationComments.hasDisabledSubmitButton(false);
    ObservationComments.hasDisabledCancelButton(false);
  });

  it("should show an error if there is a network error", () => {
    // Given there will be a network error
    forceNetworkError();

    // When I add a new comment
    ObservationComments.addComment("This is a test comment.");

    // An error is displayed
    ObservationComments.hasSubmissionError(GENERIC_ERROR_MESSAGE);

    // And the button for adding a new comment is still disabled
    ObservationComments.hasDisabledAddCommentButton(true);

    // And the other buttons are enabled
    ObservationComments.hasDisabledSubmitButton(false);
    ObservationComments.hasDisabledCancelButton(false);
  });

  it("should show an error if there is a server error", () => {
    // Given there will be a server error
    forceServerError();

    // When I add a new comment
    ObservationComments.addComment("This is a test comment.");

    // An error is displayed
    ObservationComments.hasSubmissionError(GENERIC_ERROR_MESSAGE);

    // And the button for adding a new comment is still disabled
    ObservationComments.hasDisabledAddCommentButton(true);

    // And the other buttons are enabled
    ObservationComments.hasDisabledSubmitButton(false);
    ObservationComments.hasDisabledCancelButton(false);
  });

  it("should show an error if the user is not logged in", () => {
    // Given there will be an authentication error
    forceAuthenticationError();

    // When I add a new comment
    ObservationComments.addComment("This is a test comment.");

    // An error is displayed
    ObservationComments.hasSubmissionError(NOT_LOGGED_IN_MESSAGE);

    // And the button for adding a new comment is still disabled
    ObservationComments.hasDisabledAddCommentButton(true);

    // And the other buttons are enabled
    ObservationComments.hasDisabledSubmitButton(false);
    ObservationComments.hasDisabledCancelButton(false);
  });

  it("should show an error if the user is not allowed to add a comment", () => {
    // Given there will be an authorization error
    forceForbiddenError();

    // When I add a new comment
    ObservationComments.addComment("This is a test comment.");

    // An error is displayed
    ObservationComments.hasSubmissionError(FORBIDDEN_MESSAGE);

    // And the button for adding a new comment is still disabled
    ObservationComments.hasDisabledAddCommentButton(true);

    // And the other buttons are enabled
    ObservationComments.hasDisabledSubmitButton(false);
    ObservationComments.hasDisabledCancelButton(false);
  });

  it("should cancel correctly", () => {
    // When I start adding a new comment
    ObservationComments.startNewComment();

    // And I type some comment text
    ObservationComments.typeComment("Something");

    // And I cancel
    ObservationComments.cancel();

    // Then the comment is input form is not there any longer
    ObservationComments.hasNoAddCommentForm();

    // And when I again start adding a new comment
    ObservationComments.startNewComment();

    // Then the comment text area is empty
    ObservationComments.hasNoCommentText();
  });

  it("should add an observation comment", () => {
    // Given there are no comments initially
    cy.task("clearObservationComments", PROPOSAL_CODE);

    // When I add an observation comment
    ObservationComments.addComment("This is the first comment");

    // Then the new comment is displayed
    cy.get('[data-test="observation-comment"]').should("have.length", 1);

    // And there is no input form any longer
    ObservationComments.hasNoAddCommentForm();
  });
});
