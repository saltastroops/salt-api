const SELECT_USER = '[data-test="select-user"]';
const SELECTED_USER = '[data-test="selected-user"]';

const GIVEN_NAME = '[data-test="given-name"]';
const FAMILY_NAME = '[data-test="family-name"]';
const PASSWORD = '[data-test="password"]';
const CONFIRM_PASSWORD = '[data-test="confirm-password"]';

export class ManageUserProfile {
  static typeGivenName(givenName: string): void {
    cy.get(GIVEN_NAME).type(givenName);
  }

  static typeFamilyName(familyName: string): void {
    cy.get(FAMILY_NAME).type(familyName);
  }

  static typePassword(password: string): void {
    cy.get(PASSWORD).type(password);
  }

  static typeConfirmPassword(confirmPassword: string): void {
    cy.get(CONFIRM_PASSWORD).type(confirmPassword);
  }

  static selectUser(familyName: string, givenName: string): void {
    cy.get(SELECT_USER).select(`${familyName}, ${givenName}`);
  }

  static isUserSelected(familyName: string, givenName: string): void {
    cy.get(SELECTED_USER).should("be.visible").and("contain.text", `Edit contacts for '${givenName} ${familyName}'`)
  }
}
