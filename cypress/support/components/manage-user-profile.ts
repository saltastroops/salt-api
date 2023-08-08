const SELECT_USER = '[data-test="select-user"]';
const SELECTED_USER = '[data-test="selected-user"]';

const GIVEN_NAME = '[data-test="given-name"]';
const FAMILY_NAME = '[data-test="family-name"]';
const PASSWORD = '[data-test="password"]';
const CONFIRM_PASSWORD = '[data-test="confirm-password"]';
const EMAIL = '[data-test="email"]';

const LEGAL_STATUS_SA_CITIZEN = '[data-test="legal-status-sa-citizen"]';
const LEGAL_STATUS_PERMANENT_RESIDENT =
  '[data-test="legal-status-permanent-resident"]';
const LEGAL_STATUS_OTHER = '[data-test="legal-status-other"]';

const HAS_PHD_RADIO_BUTTON = '[data-test="has-phd"]';
const HAS_NO_PHD_RADIO_BUTTON = '[data-test="has-no-phd"]';

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

  static checkSACitizenLegalStatus(): void {
    cy.get(LEGAL_STATUS_SA_CITIZEN).check();
  }

  static checkPermanentResidentLegalStatus(): void {
    cy.get(LEGAL_STATUS_PERMANENT_RESIDENT).check();
  }

  static checkOtherLegalStatus(): void {
    cy.get(LEGAL_STATUS_OTHER).check();
  }

  static checkGender(gender: "male" | "female" | "define-type"): void {
    cy.get('[data-test="gender-' + gender + '"]').check();
  }

  static checkHasPhd(): void {
    cy.get(HAS_PHD_RADIO_BUTTON).check();
  }

  static checkHasNoPhd(): void {
    cy.get(HAS_NO_PHD_RADIO_BUTTON).check();
  }

  static checkRace(
    race: "african" | "coloured" | "indian" | "white" | "prefer-not-to-say",
  ): void {
    cy.get('[data-test="race-' + race + '"]').check();
  }

  static isErrorRaisedWithMessage(
    raised: boolean,
    attributeValue: string,
    message: string | null,
  ): void {
    if (raised) {
      cy.get(`[data-test=${attributeValue}-error]`)
        .should("be.visible")
        .and("contain.text", message);
    } else {
      cy.get(`[data-test=${attributeValue}-error]`).should("not.exist");
    }
  }

  static errorRemovedByProvidingValidValue(
    dataTestAttribute: string,
    validValue: string | null,
    errorMessage: string | null,
  ): void {
    if (
      dataTestAttribute.includes("legal-status") ||
      dataTestAttribute.includes("gender") ||
      dataTestAttribute.includes("race") ||
      dataTestAttribute.includes("phd")
    ) {
      this.isErrorRaisedWithMessage(true, dataTestAttribute, errorMessage);
      if (dataTestAttribute.includes("legal-status")) {
        this.checkSACitizenLegalStatus();
      } else if (dataTestAttribute.includes("gender")) {
        this.checkGender("male");
      } else if (dataTestAttribute.includes("race")) {
        this.checkRace("african");
      } else {
        this.checkHasNoPhd();
      }
      this.isErrorRaisedWithMessage(false, dataTestAttribute, null);
    } else {
      cy.get(`[data-test="${dataTestAttribute}"]`).type("{backspace}");
      this.isErrorRaisedWithMessage(true, dataTestAttribute, errorMessage);
      cy.get(`[data-test="${dataTestAttribute}"]`).type(validValue);
      this.isErrorRaisedWithMessage(false, dataTestAttribute, null);
    }
  }
}
