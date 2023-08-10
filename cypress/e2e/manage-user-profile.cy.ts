import {ManageUserProfilePage} from "../support/pages/manage-user-profile-page";
import {LoginPage} from "../support/pages/login/login-page";
import {getEnvVariable} from "../support/utils";
import {ManageUserProfile} from "../support/components/manage-user-profile";

let USERNAME = getEnvVariable("defaultUsername");
describe("Manage user profile - administrator", () => {
  beforeEach(() => {
    cy.task("updateUserPassword", USERNAME).then((password: string) => {
      // When I login
      LoginPage.visit();
      LoginPage.login(USERNAME, password);
    });

    ManageUserProfilePage.visit();
  });

  it('should show all users dropdown', function () {
    ManageUserProfile.isSelectUserDropdownDisplayed(true);
  });

  it('should show selected user\'s details', function () {
    const defaultUserGivenName = "Chaka";
    const defaultUserFamilyName = "Mofokeng";
    ManageUserProfile.displayedDetailsForUser(defaultUserFamilyName, defaultUserGivenName);

    const givenName = "Xola";
    const familyName = "Ndaliso"
    ManageUserProfile.selectUser(familyName, givenName);
    ManageUserProfile.displayedDetailsForUser(familyName, givenName);
  });
});

describe("Manage user profile - investigator", () => {
  beforeEach(() => {
    USERNAME = getEnvVariable("investigator");
    cy.task("updateUserPassword", USERNAME).then((password: string) => {
      // When I login
      LoginPage.visit();
      LoginPage.login(USERNAME, password);
    });

    ManageUserProfilePage.visit();
  });

  it('should hide users dropdown for users other than administrators', function () {
    ManageUserProfile.isSelectUserDropdownDisplayed(false);
  });

  it('should have institutions controls disabled', function () {
    ManageUserProfile.isInstitutionControlsDisabled(true);
  });

  it('should show logged in user\'s details', function () {
    const givenName = "Rajeev";
    const familyName = "Manick"
    ManageUserProfile.displayedDetailsForUser(familyName, givenName);
  });

  it('should raise an error when the password has less than 6 characters', function () {
    ManageUserProfile.typePassword("sca");
    ManageUserProfile.isErrorRaisedWithMessage(true, "password", "Password must have at least 6 characters")
  });

  it('should raise a password length error when typing a password and remove it when the input it cleared', function () {
    ManageUserProfile.typePassword("sca");
    ManageUserProfile.isErrorRaisedWithMessage(true, "password", "Password must have at least 6 characters")
    ManageUserProfile.clearPassword();
    ManageUserProfile.isErrorRaisedWithMessage(false, "password", null);
  });

  it('should raise an error when the password and confirmation password differ and remove the error when they match', function () {
    const PASSWORD = "secret"
    ManageUserProfile.typePassword(PASSWORD);
    ManageUserProfile.typeConfirmPassword("secret123");
    ManageUserProfile.isErrorRaisedWithMessage(true, "confirm-password", "Password mismatch");
    ManageUserProfile.clearConfirmPassword();
    ManageUserProfile.typeConfirmPassword(PASSWORD);
    ManageUserProfile.isErrorRaisedWithMessage(false, "confirm-password", null);

  });

  it('should show user demographics fields when a user is a permanent resident or a citizen of South Africa', function () {
    ManageUserProfile.checkOtherLegalStatus();
    ManageUserProfile.isUserDemographicsDisplayed(false);
    ManageUserProfile.checkSACitizenLegalStatus();
    ManageUserProfile.isUserDemographicsDisplayed(true);
    ManageUserProfile.checkPermanentResidentLegalStatus();
    ManageUserProfile.isUserDemographicsDisplayed(true);
  });

  it.only('should remove the error when a valid value is entered', function () {
    ManageUserProfile.clickSubmit();
    ManageUserProfile.isErrorRaisedWithMessage(true, "legal-status", "Your legal status in South Africa is required");
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
});
