import "cypress-network-idle";

import { RegisterUser } from "../support/components/register-user";
import { HOME_URL } from "../support/pages/home-page";
import { LoginPage } from "../support/pages/login/login-page";
import { RegisterUserPage } from "../support/pages/register-user-page";
import { getApiUrl } from "../support/utils";

const apiUrl = getApiUrl();

describe("Register new user", () => {
  beforeEach(() => {
    RegisterUserPage.visit();
  });

  it("should raise error after a required filled is touched without completing it", function () {
    RegisterUser.clickUsernameField();
    RegisterUser.clickTopOfTheBody();
    RegisterUser.isErrorRaisedWithMessage(
      true,
      "username",
      "Username is required",
    );

    RegisterUser.clickPasswordField();
    RegisterUser.clickTopOfTheBody();
    RegisterUser.isErrorRaisedWithMessage(
      true,
      "password",
      "Password is required",
    );

    RegisterUser.clickConfirmPasswordField();
    RegisterUser.clickTopOfTheBody();
    RegisterUser.isErrorRaisedWithMessage(
      true,
      "confirm-password",
      "Confirmation password is required",
    );

    RegisterUser.selectPartnerInstitution("please select partner");
    RegisterUser.clickTopOfTheBody();
    RegisterUser.clickTopOfTheBody();
    RegisterUser.isErrorRaisedWithMessage(
      true,
      "partner-institutions",
      "Partner is required",
    );

    RegisterUser.clickEmailField();
    RegisterUser.clickTopOfTheBody();
    RegisterUser.isErrorRaisedWithMessage(true, "email", "Email is required");
  });

  it("should raise an error when the password has less than 6 characters", function () {
    RegisterUser.typePassword("scrt");
    RegisterUser.clickTopOfTheBody();
    RegisterUser.isErrorRaisedWithMessage(
      true,
      "password",
      "Password must have at least 6 characters",
    );
  });

  it("should raise an error when the password and confirmation password differ", function () {
    RegisterUser.typePassword("secret");
    RegisterUser.typeConfirmPassword("scrt123");
    RegisterUser.clickTopOfTheBody();
    RegisterUser.isErrorRaisedWithMessage(
      true,
      "confirm-password",
      "Password mismatch",
    );
  });

  it("should remove the error when a valid value is entered", function () {
    RegisterUser.errorRemovedByProvidingValidValue(
      "username",
      "chaka",
      "Username is required",
    );
    RegisterUser.errorRemovedByProvidingValidValue(
      "password",
      "secret-123",
      "Password is required",
    );
    RegisterUser.errorRemovedByProvidingValidValue(
      "given-name",
      "Chaka",
      "Name is required",
    );
    RegisterUser.errorRemovedByProvidingValidValue(
      "family-name",
      "Mofokeng",
      "Surname is required",
    );
    RegisterUser.errorRemovedByProvidingValidValue(
      "partner-institutions",
      null,
      "Partner is required",
    );
    RegisterUser.errorRemovedByProvidingValidValue(
      "email",
      "cmofokeng@example.com",
      "Email is required",
    );

    RegisterUser.selectPartnerInstitution("South Africa");
    RegisterUser.errorRemovedByProvidingValidValue(
      "institutions",
      null,
      "Institute is required",
    );

    RegisterUser.selectPartnerInstitution("Other");
    RegisterUser.selectInstitution("ADD NEW INSTITUTE");
    RegisterUser.errorRemovedByProvidingValidValue(
      "institution-name",
      "Mzansi Institute for Science",
      "Institute name is required",
    );
    RegisterUser.errorRemovedByProvidingValidValue(
      "institution-department",
      "Department of Science",
      "Department is required",
    );
    RegisterUser.errorRemovedByProvidingValidValue(
      "institution-address",
      "Mzansi Institute for Science \n1 Observatory Road \n7709",
      "Address is required",
    );
    RegisterUser.errorRemovedByProvidingValidValue(
      "institution-url",
      "www.mis.ac.za",
      "URL is required",
    );

    RegisterUser.clickRegisterNewUserButton();
    RegisterUser.errorRemovedByProvidingValidValue(
      "legal-status",
      null,
      "Your legal status in South Africa is required",
    );

    RegisterUser.checkSACitizenLegalStatus();
    RegisterUser.clickRegisterNewUserButton();
    RegisterUser.errorRemovedByProvidingValidValue(
      "gender",
      null,
      "Gender is required",
    );
    RegisterUser.errorRemovedByProvidingValidValue(
      "race",
      null,
      "Race is required",
    );
    RegisterUser.errorRemovedByProvidingValidValue(
      "has-phd",
      null,
      "PhD status is required",
    );
  });

  it("should show institutions after selecting a partner", function () {
    RegisterUser.isInstitutionsDropdownDisplayed(false);
    RegisterUser.selectPartnerInstitution("Poland");
    RegisterUser.isInstitutionsDropdownDisplayed(true);
  });

  it("should show fields for adding a new institution only when ADD NEW INSTITUTION option is selected", function () {
    RegisterUser.isNewInstitutionFieldsDisplayed(false);
    RegisterUser.selectPartnerInstitution("Other");
    RegisterUser.selectInstitution("ADD NEW INSTITUTE");
    RegisterUser.isNewInstitutionFieldsDisplayed(true);

    RegisterUser.selectPartnerInstitution("South Africa");
    RegisterUser.selectInstitution("South African Astronomical Observatory");
    RegisterUser.isNewInstitutionFieldsDisplayed(false);
  });

  it("should show user demographics fields when a user is a permanent resident or a citizen of South Africa", function () {
    RegisterUser.checkOtherLegalStatus();
    RegisterUser.isUserDemographicsDisplayed(false);
    RegisterUser.checkSACitizenLegalStatus();
    RegisterUser.isUserDemographicsDisplayed(true);
    RegisterUser.checkPermanentResidentLegalStatus();
    RegisterUser.isUserDemographicsDisplayed(true);
  });

  it("should raise an error for an existing username", function () {
    const username = "cmofokeng";
    const name = "Chaka";
    const surname = "Mofokeng";
    const password = "cm-very-secret-password";
    const email = "cmofokeng@example.com";

    RegisterUser.typeUsername(username);
    RegisterUser.typePassword(password);
    RegisterUser.typeConfirmPassword(password);
    RegisterUser.typeGivenName(name);
    RegisterUser.typeFamilyName(surname);
    RegisterUser.selectPartnerInstitution("South Africa");
    RegisterUser.selectInstitution("South African Astronomical Observatory");
    RegisterUser.typeEmail(email);
    RegisterUser.checkSACitizenLegalStatus();
    RegisterUser.checkGender("male");
    RegisterUser.checkRace("african");
    RegisterUser.checkHasNoPhd();

    RegisterUser.clickRegisterNewUserButton();
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    RegisterUser.isErrorRaisedWithMessage(true, "submission", "exists already");
  });

  it("should register new user and allow them to log in", function () {
    const randomString = Math.random().toString(36).substring(2, 7);
    const username = "tchamp-" + randomString;
    const name = "Thato";
    const surname = "Champ";
    const password = "tc-very-secret-password";
    const email = `${username}@example.com`;

    RegisterUser.typeUsername(username);
    RegisterUser.typePassword(password);
    RegisterUser.typeConfirmPassword(password);
    RegisterUser.typeGivenName(name);
    RegisterUser.typeFamilyName(surname);
    RegisterUser.selectPartnerInstitution("South Africa");
    RegisterUser.selectInstitution("South African Astronomical Observatory");
    RegisterUser.typeEmail(email);
    RegisterUser.checkSACitizenLegalStatus();
    RegisterUser.checkGender("male");
    RegisterUser.checkRace("african");
    RegisterUser.checkHasNoPhd();

    RegisterUser.clickRegisterNewUserButton();

    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);

    cy.on("window:alert", (text) => {
      expect(text).contains(
        "You have successfully registered.\nYou may to proceed to log in.",
      );
    });

    LoginPage.visit();
    LoginPage.login(username, password);

    cy.url().should("contain", HOME_URL);
  });
});
