import { NavigationBar } from "../support/components/navigation-bar";
import { HomePage } from "../support/pages/home-page";
import { LoginPage } from "../support/pages/login/login-page";
import { User } from "../support/types";
import {
  forceNetworkError,
  forceServerError,
  getApiUrl,
  getEnvVariable,
  interceptIndefinitely,
} from "../support/utils";

const apiUrl = getApiUrl();

const USERNAME = getEnvVariable("defaultUsername");
const ADMINISTRATOR = getEnvVariable("administrator");
const INVESTIGATOR = getEnvVariable("investigator");
const SALT_ASTRONOMER = getEnvVariable("saltAstronomerUsername");
const TAC_MEMBER = getEnvVariable("tacMember");

describe("Inline login form", () => {
  beforeEach(() => {
    // Ensure the inline login form is not hidden because of a small screen size
    cy.viewport(1500, 2000);

    cy.intercept(apiUrl + "/login").as("login");
  });

  it("should give an error if the username is missing", () => {
    HomePage.visit();
    NavigationBar.typePassword("secret");
    NavigationBar.submitLogin();
    NavigationBar.hasUsernameError();
  });

  it("should give an error if the username is missing", () => {
    HomePage.visit();
    NavigationBar.typeUsername("someone");
    NavigationBar.submitLogin();
    NavigationBar.hasPasswordError();
  });

  it("should give an error if there is a network error", () => {
    HomePage.visit();
    forceNetworkError();
    NavigationBar.typeUsername("someone");
    NavigationBar.typePassword("secret");
    NavigationBar.submitLogin();
    NavigationBar.hasGenericLoginError();
  });

  it("should give an error if there is a server error", () => {
    HomePage.visit();
    forceServerError();
    NavigationBar.typeUsername("someone");
    NavigationBar.typePassword("secret");
    NavigationBar.submitLogin();
    NavigationBar.hasGenericLoginError();
  });

  it("should give an error if the username or password is incorrect", () => {
    cy.task("updateUserPassword");
    HomePage.visit();
    NavigationBar.typeUsername(USERNAME);
    NavigationBar.typePassword("secret");
    NavigationBar.submitLogin();
    NavigationBar.hasUsernameOrPasswordError();
  });

  it("should log the user in if the username and password are valid", () => {
    cy.task("updateUserPassword", USERNAME).then((password: string) => {
      cy.task("getUser", USERNAME).then((user: User) => {
        HomePage.visit();
        NavigationBar.typeUsername(USERNAME);
        NavigationBar.typePassword(password);
        NavigationBar.submitLogin();
        NavigationBar.hasNoLoginForm();
        NavigationBar.hasWelcomeMessage(user.givenName);
      });
    });
  });

  it("should indicate a loading state until a successful login request finishes", () => {
    cy.task("updateUserPassword", USERNAME).then((password: string) => {
      const interception = interceptIndefinitely("login");
      HomePage.visit();
      NavigationBar.typeUsername(USERNAME);
      NavigationBar.typePassword(password);
      NavigationBar.submitLogin();
      NavigationBar.loginIsLoading().then(() => {
        interception.sendResponse();
        NavigationBar.loginIsNotLoading();
      });
    });
  });

  it("should indicate a loading state until an unsuccessful login request finishes", () => {
    cy.task("updateUserPassword", USERNAME).then(() => {
      const interception = interceptIndefinitely("login");
      HomePage.visit();
      NavigationBar.typeUsername(USERNAME);
      NavigationBar.typePassword("incorrect");
      NavigationBar.submitLogin();
      NavigationBar.loginIsLoading().then(() => {
        interception.sendResponse();
        NavigationBar.loginIsNotLoading();
      });
    });
  });
  // TODO the tab should be removed when the user logout
});

describe("Navigation bar", () => {
  beforeEach(() => {
    // Ensure the inline login form is not hidden because of a small screen size
    cy.viewport(1500, 2000);

    cy.intercept(apiUrl + "/login").as("login");
  });

  it("should show all tabs for admin", () => {
    cy.task("updateUserPassword", ADMINISTRATOR).then((password: string) => {
      cy.task("getUser", ADMINISTRATOR).then(() => {
        HomePage.visit();
        NavigationBar.typeUsername(ADMINISTRATOR);
        NavigationBar.typePassword(password);
        NavigationBar.submitLogin();

        // When the user had logged in the following tabs should be visible
        NavigationBar.hasHomeTab();
        NavigationBar.hasSOPageTab();
        NavigationBar.hasSAPagesTab();
        NavigationBar.hasOptionsTab();
        NavigationBar.hasGravitationalWavesTab();
        NavigationBar.hasAdminTab();
      });
    });
  });

  it("should show tabs only available to Investigators", () => {
    cy.task("updateUserPassword", INVESTIGATOR).then((password: string) => {
      cy.task("getUser", INVESTIGATOR).then(() => {
        HomePage.visit();
        NavigationBar.typeUsername(INVESTIGATOR);
        NavigationBar.typePassword(password);
        NavigationBar.submitLogin();

        // When the user had logged in the following tabs should be visible
        NavigationBar.hasHomeTab();
        NavigationBar.hasNoSOPageTab();
        NavigationBar.hasNoSAPagesTab();
        NavigationBar.hasOptionsTab();
        NavigationBar.hasGravitationalWavesTab();
        NavigationBar.hasNoAdminTab();
      });
    });
  });

  it("should show tabs only available to SALT Astronomers", () => {
    cy.task("updateUserPassword", SALT_ASTRONOMER).then((password: string) => {
      cy.task("getUser", SALT_ASTRONOMER).then(() => {
        HomePage.visit();
        NavigationBar.typeUsername(SALT_ASTRONOMER);
        NavigationBar.typePassword(password);
        NavigationBar.submitLogin();

        // When the user had logged in the following tabs should be visible
        NavigationBar.hasHomeTab();
        NavigationBar.hasSOPageTab();
        NavigationBar.hasSAPagesTab();
        NavigationBar.hasOptionsTab();
        NavigationBar.hasGravitationalWavesTab();
        NavigationBar.hasNoAdminTab();
      });
    });
  });

  it("should show tabs only available to TAC members", () => {
    cy.task("updateUserPassword", TAC_MEMBER).then((password: string) => {
      cy.task("getUser", TAC_MEMBER).then(() => {
        HomePage.visit();
        NavigationBar.typeUsername(TAC_MEMBER);
        NavigationBar.typePassword(password);
        NavigationBar.submitLogin();

        // When the user had logged in the following tabs should be visible
        NavigationBar.hasHomeTab();
        NavigationBar.hasNoSOPageTab();
        NavigationBar.hasNoSAPagesTab();
        NavigationBar.hasOptionsTab();
        NavigationBar.hasGravitationalWavesTab();
        NavigationBar.hasNoAdminTab();
      });
    });
  });
});

describe("Go to proposal form", () => {
  beforeEach(() => {
    // Ensure the form is not hidden because of a small screen size
    cy.viewport(1500, 2000);

    cy.intercept(apiUrl + "/login").as("login");

    cy.task("updateUserPassword", SALT_ASTRONOMER).then((password: string) => {
      // When I login
      LoginPage.visit();
      LoginPage.login(SALT_ASTRONOMER, password);
    });

    HomePage.visit();
  });

  it("should load the proposal page when you click its submit button", () => {
    NavigationBar.typeProposalCode("2021-2-DDT-001");
    NavigationBar.submitGoToProposalForm();

    cy.get(".title").should("contain.text", "2021-2-DDT-001");
  });

  it("should load the proposal page when you hit enter", () => {
    NavigationBar.typeProposalCode("2021-2-DDT-001{enter}");
    cy.get(".title").should("contain.text", "2021-2-DDT-001");
  });

  it("should clear the input after loading the page", () => {
    NavigationBar.typeProposalCode("2021-2-DDT-001{enter}");
    cy.get(".title").should("contain.text", "2021-2-DDT-001");

    NavigationBar.isNotShowingProposalCodeInForm();
  });

  it("should reload the proposal page when you are on a proposal page already", () => {
    NavigationBar.typeProposalCode("2021-2-DDT-001{enter}");
    cy.get(".title").should("contain.text", "2021-2-DDT-001");

    NavigationBar.typeProposalCode("2022-2-SCI-017{enter}");
    cy.get(".title").should("contain.text", "2022-2-SCI-017");
  });
});
