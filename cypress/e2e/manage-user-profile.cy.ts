import { ManageUserProfile } from "../support/components/manage-user-profile";
import { LoginPage } from "../support/pages/login/login-page";
import { ManageUserProfilePage } from "../support/pages/manage-user-profile-page";
import {getApiUrl, getEnvVariable} from "../support/utils";
import {HOME_URL} from "../support/pages/home-page";

const apiUrl = getApiUrl();
describe("Manage user profile - other users (investigator)", () => {
  const USERNAME = getEnvVariable("investigator");
  beforeEach(() => {
    cy.intercept(apiUrl + "/users/**").as("users");
    cy.task("updateUserPassword", USERNAME).then((password: string) => {
      // When I login
      LoginPage.visit();
      LoginPage.login(USERNAME, password);
    });

    ManageUserProfilePage.visit();
  });

  it("should hide users dropdown for users other than administrators", function () {
    ManageUserProfile.isSelectUserDropdownDisplayed(false);
  });

  it("should have institutions controls disabled", function () {
    ManageUserProfile.isInstitutionControlsDisabled(true);
  });

  it("should show logged in user's details", function () {
    const givenName = "Rajeev";
    const familyName = "Manick";
    ManageUserProfile.displayedDetailsForUser(familyName, givenName);
  });

  it("should raise an error when the password has less than 6 characters", function () {
    ManageUserProfile.typePassword("sca");
    ManageUserProfile.isErrorRaisedWithMessage(
      true,
      "password",
      "Password must have at least 6 characters",
    );
  });

  it("should raise a password length error when typing a password and remove it when the input it cleared", function () {
    ManageUserProfile.typePassword("sca");
    ManageUserProfile.isErrorRaisedWithMessage(
      true,
      "password",
      "Password must have at least 6 characters",
    );
    ManageUserProfile.clearPassword();
    ManageUserProfile.isErrorRaisedWithMessage(false, "password", null);
  });

  it("should raise an error when the password and confirmation password differ and remove the error when they match", function () {
    const PASSWORD = "secret";
    ManageUserProfile.typePassword(PASSWORD);
    ManageUserProfile.typeConfirmPassword("secret123");
    ManageUserProfile.isErrorRaisedWithMessage(
      true,
      "confirm-password",
      "Password mismatch",
    );
    ManageUserProfile.clearConfirmPassword();
    ManageUserProfile.typeConfirmPassword(PASSWORD);
    ManageUserProfile.isErrorRaisedWithMessage(false, "confirm-password", null);
  });

  it("should show user demographics fields when a user is a permanent resident or a citizen of South Africa", function () {
    ManageUserProfile.checkOtherLegalStatus();
    ManageUserProfile.isUserDemographicsDisplayed(false);
    ManageUserProfile.checkSACitizenLegalStatus();
    ManageUserProfile.isUserDemographicsDisplayed(true);
    ManageUserProfile.checkPermanentResidentLegalStatus();
    ManageUserProfile.isUserDemographicsDisplayed(true);
  });

  it("should remove the error when a valid value is entered", function () {
    ManageUserProfile.clickSubmit();
    ManageUserProfile.isErrorRaisedWithMessage(
      true,
      "legal-status",
      "Your legal status in South Africa is required",
    );
    ManageUserProfile.checkPermanentResidentLegalStatus();

    ManageUserProfile.clickSubmit();
    ManageUserProfile.errorRemovedByProvidingValidValue(
      "gender",
      null,
      "Gender is required",
    );
    ManageUserProfile.errorRemovedByProvidingValidValue(
      "race",
      null,
      "Race is required",
    );
    ManageUserProfile.errorRemovedByProvidingValidValue(
      "has-phd",
      null,
      "PhD status is required",
    );
  });

  it("should update logged in user's details", function () {
    // Ensure the inline login form is not hidden because of a small screen size
    cy.viewport(1500, 2000);

    const NEW_PASSWORD = "very-secret-1234-pass";

    ManageUserProfile.typePassword(NEW_PASSWORD);
    ManageUserProfile.typeConfirmPassword(NEW_PASSWORD);

    ManageUserProfile.checkOtherLegalStatus();

    ManageUserProfile.clickSubmit();

    cy.wait("@users");

    cy.on("window:alert", (text) => {
      expect(text).contains(
        "User details successfully updated",
      );
    });
    cy.wait(1000);

    LoginPage.logout()

    LoginPage.visit();
    LoginPage.login(USERNAME, NEW_PASSWORD);

    cy.url().should("contain", HOME_URL);
  });
});

describe("Manage user profile - administrator", () => {
  const USERNAME = getEnvVariable("defaultUsername");
  beforeEach(() => {
    cy.intercept("PATCH", apiUrl + "/users/**").as("users");
    cy.task("updateUserPassword", USERNAME).then((password: string) => {
      // When I login
      LoginPage.visit();
      LoginPage.login(USERNAME, password);
    });

    ManageUserProfilePage.visit();
  });

  it("should show all users dropdown", function () {
    ManageUserProfile.isSelectUserDropdownDisplayed(true);
  });

  it("should show selected user's details", function () {
    const defaultUserGivenName = "Chaka";
    const defaultUserFamilyName = "Mofokeng";
    ManageUserProfile.displayedDetailsForUser(
      defaultUserFamilyName,
      defaultUserGivenName,
    );

    const givenName = "Xola";
    const familyName = "Ndaliso";
    ManageUserProfile.selectUser(familyName, givenName);
    ManageUserProfile.displayedDetailsForUser(familyName, givenName);
  });

  it("should update selected user's details", function () {
    const givenName = "Orapeleng";
    const familyName = "Mogawana";
    ManageUserProfile.selectUser(familyName, givenName);
    ManageUserProfile.displayedDetailsForUser(familyName, givenName);

    const newGivenName = "Oraps";
    const newFamilyName = "Mokgawana";
    ManageUserProfile.clearGivenName();
    ManageUserProfile.typeGivenName(newGivenName);
    ManageUserProfile.clearFamilyName();
    ManageUserProfile.typeFamilyName(newFamilyName);

    ManageUserProfile.checkPermanentResidentLegalStatus();
    ManageUserProfile.checkGender("male");
    ManageUserProfile.checkRace("african");
    ManageUserProfile.checkHasNoPhd();

    ManageUserProfile.clickSubmit();

    cy.wait('@users').its('response.statusCode').should('eq', 200);

    cy.on("window:alert", (text) => {
      expect(text).contains(
        "User details successfully updated",
      );
    });

    cy.reload();

    ManageUserProfile.selectUser(newFamilyName, newGivenName);
    ManageUserProfile.displayedDetailsForUser(newFamilyName, newGivenName);

    ManageUserProfile.clearGivenName();
    ManageUserProfile.typeGivenName(givenName);
    ManageUserProfile.clearFamilyName();
    ManageUserProfile.typeFamilyName(familyName);

    ManageUserProfile.checkPermanentResidentLegalStatus();
    ManageUserProfile.checkGender("male");
    ManageUserProfile.checkRace("african");
    ManageUserProfile.checkHasNoPhd();

    ManageUserProfile.clickSubmit();

    cy.wait('@users').its('response.statusCode').should('eq', 200);
  });
});
