const ADD_COMMENT_FORM = '[data-test="add-observation-comment-form"]';
const ADD_COMMENT_BUTTON = '[data-test="add-observation-comment-button"]';
const ADD_COMMENT_TEXT = '[data-test="add-observation-comment-text"]';
const ADD_COMMENT_SUBMIT = '[data-test="add-observation-comment-submit"]';
const ADD_COMMENT_CANCEL = '[data-test="add-observation-comment-cancel"]';
const COMMENT_ERROR = '[data-test="observation-comment-text-error"]';
const SUBMISSION_ERROR = '[data-test="observation-comment-submission-error"]';

export class ObservationComments {
  static startNewComment(): void {
    cy.get(ADD_COMMENT_BUTTON).click();
  }

  static typeComment(comment: string): void {
    cy.get(ADD_COMMENT_TEXT).type(comment);
  }

  static clearCommentText(): void {
    cy.get(ADD_COMMENT_TEXT).clear();
  }

  static submitComment(): void {
    cy.get(ADD_COMMENT_SUBMIT).click();
  }

  static cancel(): void {
    cy.get(ADD_COMMENT_CANCEL).click();
  }

  static addComment(comment: string): void {
    this.startNewComment();
    this.typeComment(comment);
    this.submitComment();
  }

  static hasNoAddCommentForm(): void {
    cy.get(ADD_COMMENT_FORM).should("not.exist");
  }

  static hasNoCommentText(): void {
    cy.get(ADD_COMMENT_TEXT).should("have.value", "");
  }

  static hasDisabledAddCommentButton(disabled: boolean): void {
    if (disabled) {
      cy.get(ADD_COMMENT_BUTTON).should("be.disabled");
    } else {
      cy.get(ADD_COMMENT_BUTTON).should("not.be.disabled");
    }
  }

  static hasDisabledSubmitButton(disabled: boolean): void {
    if (disabled) {
      cy.get(ADD_COMMENT_SUBMIT).should("be.disabled");
    } else {
      cy.get(ADD_COMMENT_SUBMIT).should("not.be.disabled");
    }
  }

  static hasDisabledCancelButton(disabled: boolean): void {
    if (disabled) {
      cy.get(ADD_COMMENT_CANCEL).should("be.disabled");
    } else {
      cy.get(ADD_COMMENT_CANCEL).should("not.be.disabled");
    }
  }

  static hasCommentError(): void {
    cy.get(COMMENT_ERROR).should("be.visible").and("contain", "comment text");
  }

  static hasNoCommentError(): void {
    cy.get(COMMENT_ERROR).should("not.exist");
  }

  static hasSubmissionError(text: string): void {
    cy.get(SUBMISSION_ERROR).should("be.visible").and("contain", text);
  }

  static hasNoSubmissionError(): void {
    cy.get(SUBMISSION_ERROR).should("not.exist");
  }
}
