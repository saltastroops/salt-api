import { NavigationBar } from "../support/components/navigation-bar";
import { HomePage } from "../support/pages/home-page";
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

// load and register the grep feature using "require" function
// https://github.com/cypress-io/cypress-grep
// eslint-disable-next-line @typescript-eslint/no-var-requires
const registerCypressGrep = require("cypress-grep");
registerCypressGrep();

describe("Inline login form", () => {
  beforeEach(() => {
    // Ensure the inline login form is not hidden because of a small screen size
    cy.viewport(1500, 2000);

    cy.recordHttp(apiUrl + "/token").as("token");

    cy.recordHttp(apiUrl + "/user").as("user");

    cy.recordHttp(apiUrl + "/proposals/**").as("proposals");

    cy.recordHttp(apiUrl + "/blocks/**").as("blocks");
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

  it(
    "should log the user in if the username and password are valid",
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore
    { tags: "@skip" },
    () => {
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
    },
  );

  it("should indicate a loading state until a successful login request finishes", () => {
    cy.task("updateUserPassword", USERNAME).then((password: string) => {
      const interception = interceptIndefinitely("token");
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
      const interception = interceptIndefinitely("token");
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

    cy.recordHttp(apiUrl + "/token").as("token");

    cy.recordHttp(apiUrl + "/user").as("user");

    cy.recordHttp(apiUrl + "/proposals/**").as("proposals");

    cy.recordHttp(apiUrl + "/blocks/**").as("blocks");
  });
  it("Should show all tabs for admin", () => {
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

  it("Should show only show tabs available to Investigators", () => {
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

  it("Should show only show tabs available to SALT Astronomers", () => {
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

  it("Should show only show tabs available to TAC members", () => {
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
