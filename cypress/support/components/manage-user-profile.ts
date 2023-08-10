const SELECT_USER = '[data-test="select-user"]';
const SELECTED_USER = '[data-test="selected-user"]';

const GIVEN_NAME = '[data-test="given-name"]';
const FAMILY_NAME = '[data-test="family-name"]';
const PASSWORD = '[data-test="password"]';
const CONFIRM_PASSWORD = '[data-test="confirm-password"]';
const EMAIL = '[data-test="email"]';

const PARTNER_INSTITUTIONS = '[data-test="partner-institutions"]';
const INSTITUTIONS = '[data-test="institutions"]';

const LEGAL_STATUS_SA_CITIZEN = '[data-test="legal-status-sa-citizen"]';
const LEGAL_STATUS_PERMANENT_RESIDENT =
  '[data-test="legal-status-permanent-resident"]';
const LEGAL_STATUS_OTHER = '[data-test="legal-status-other"]';

const HAS_PHD_RADIO_BUTTON = '[data-test="has-phd"]';
const HAS_NO_PHD_RADIO_BUTTON = '[data-test="has-no-phd"]';

const SUBMIT_BUTTON = '[data-test="update-user-details"]';

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

  static clearPassword(): void {
    cy.get(PASSWORD).clear();
  }

  static typeConfirmPassword(confirmPassword: string): void {
    cy.get(CONFIRM_PASSWORD).type(confirmPassword);
  }

  static clickSubmit(): void {
    cy.get(SUBMIT_BUTTON).click();
  }

  static clearConfirmPassword(): void {
    cy.get(CONFIRM_PASSWORD).clear();
  }

  static isSelectUserDropdownDisplayed(displayed: boolean): void {
    if (displayed) {
      cy.get(SELECT_USER).should("be.visible");
    } else {
      cy.get(SELECT_USER).should("not.exist");
    }
  }

  static isUserDemographicsDisplayed(displayed: boolean): void {
    if (displayed) {
      cy.get('[data-test="gender-male"]').should("exist").and("be.visible");
      cy.get('[data-test="gender-female"]').should("exist").and("be.visible");
    } else {
      cy.get('[data-test="gender-male"]').should("not.exist");
      cy.get('[data-test="gender-female"]').should("not.exist");
    }
  }

  static selectUser(familyName: string, givenName: string): void {
    cy.get(SELECT_USER).select(`${familyName}, ${givenName}`);
  }

  static displayedDetailsForUser(familyName: string, givenName: string): void {
    cy.get(SELECTED_USER)
      .should("be.visible")
      .and("contain.text", `Edit contacts for '${givenName} ${familyName}'`);
    cy.get(GIVEN_NAME).should("be.visible").and("have.value", givenName);
    cy.get(FAMILY_NAME).should("be.visible").and("have.value", familyName);
    cy.get(EMAIL).invoke("val").should("not.be.empty");
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

  static isInstitutionControlsDisabled(disabled: boolean): void {
    if (disabled) {
      cy.get(PARTNER_INSTITUTIONS).should("be.disabled");
      cy.get(INSTITUTIONS).should("be.disabled");
    } else {
      cy.get(PARTNER_INSTITUTIONS).should("not.be.disabled");
      cy.get(INSTITUTIONS).should("not.be.disabled");
    }
  }
}
