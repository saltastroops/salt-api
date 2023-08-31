const USERNAME = '[data-test="username"]';
const PASSWORD = '[data-test="password"]';
const CONFIRM_PASSWORD = '[data-test="confirm-password"]';
const GIVEN_NAME = '[data-test="given-name"]';
const FAMILY_NAME = '[data-test="family-name"]';
const PARTNER_INSTITUTIONS = '[data-test="partner-institutions"]';
const INSTITUTIONS = '[data-test="institutions"]';
const INSTITUTION_NAME = '[data-test="institution-name"]';
const INSTITUTION_DEPARTMENT = '[data-test="institution-department"]';
const INSTITUTION_URL = '[data-test="institution-url"]';
const INSTITUTION_ADDRESS = '[data-test="institution-address"]';
const EMAIL = '[data-test="email"]';

const LEGAL_STATUS_SA_CITIZEN = '[data-test="legal-status-sa-citizen"]';
const LEGAL_STATUS_PERMANENT_RESIDENT =
  '[data-test="legal-status-permanent-resident"]';
const LEGAL_STATUS_OTHER = '[data-test="legal-status-other"]';

const HAS_PHD_RADIO_BUTTON = '[data-test="has-phd"]';
const HAS_NO_PHD_RADIO_BUTTON = '[data-test="has-no-phd"]';

const REGISTER_NEW_USER_BUTTON = '[data-test="register-new-user-submit"]';

export class RegisterUser {
  static clickTopOfTheBody(): void {
    cy.get("body").click(0, 0);
  }
  static clickRegisterNewUserButton(): void {
    cy.get(REGISTER_NEW_USER_BUTTON).click();
  }

  static typeUsername(username: string): void {
    cy.get(USERNAME).type(username);
  }

  static clickUsernameField(): void {
    cy.get(USERNAME).click();
  }

  static typeGivenName(givenName: string): void {
    cy.get(GIVEN_NAME).type(givenName);
  }

  static typeFamilyName(familyName: string): void {
    cy.get(FAMILY_NAME).type(familyName);
  }

  static typePassword(password: string): void {
    cy.get(PASSWORD).type(password);
  }

  static clickPasswordField(): void {
    cy.get(PASSWORD).click();
  }

  static typeConfirmPassword(confirmPassword: string): void {
    cy.get(CONFIRM_PASSWORD).type(confirmPassword);
  }

  static clickConfirmPasswordField(): void {
    cy.get(CONFIRM_PASSWORD).click();
  }

  static typeEmail(email: string): void {
    cy.get(EMAIL).type(email);
  }

  static clickEmailField(): void {
    cy.get(EMAIL).click();
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

  static selectPartnerInstitution(partnerInstitution: string): void {
    cy.get(PARTNER_INSTITUTIONS).select(partnerInstitution);
  }

  static selectInstitution(Institution: string): void {
    cy.get(INSTITUTIONS).select(Institution);
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

  static isInstitutionsDropdownDisplayed(displayed: boolean): void {
    if (displayed) {
      cy.get(INSTITUTIONS).should("exist").and("be.visible");
    } else {
      cy.get(INSTITUTIONS).should("not.exist");
    }
  }

  static isNewInstitutionFieldsDisplayed(displayed: boolean): void {
    if (displayed) {
      cy.get(INSTITUTION_NAME).should("exist").and("be.visible");
      cy.get(INSTITUTION_DEPARTMENT).should("exist").and("be.visible");
      cy.get(INSTITUTION_URL).should("exist").and("be.visible");
      cy.get(INSTITUTION_ADDRESS).should("exist").and("be.visible");
    } else {
      cy.get(INSTITUTION_NAME).should("not.exist");
      cy.get(INSTITUTION_DEPARTMENT).should("not.exist");
      cy.get(INSTITUTION_ADDRESS).should("not.exist");
      cy.get(INSTITUTION_URL).should("not.exist");
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

  static errorRemovedByProvidingValidValue(
    dataTestAttribute: string,
    validValue: string | null,
    errorMessage: string | null,
  ): void {
    if (dataTestAttribute.includes("institutions")) {
      cy.get(`[data-test="${dataTestAttribute}"]`).select(0);
      this.clickTopOfTheBody();
      this.isErrorRaisedWithMessage(true, dataTestAttribute, errorMessage);
      cy.get(`[data-test="${dataTestAttribute}"]`).select(1);
      this.isErrorRaisedWithMessage(false, dataTestAttribute, null);
    } else if (
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
      this.clickTopOfTheBody();
      this.isErrorRaisedWithMessage(true, dataTestAttribute, errorMessage);
      cy.get(`[data-test="${dataTestAttribute}"]`).type(validValue);
      this.isErrorRaisedWithMessage(false, dataTestAttribute, null);
    }
  }
}
