import { LoginPage } from "../../support/pages/login/login-page";
import { SwitchUserPage } from "../../support/pages/login/switch-user-page";
import { SWITCH_USER_URL } from "../../support/pages/login/switch-user-page";
import { getEnvVariable } from "../../support/utils";

let USERNAME: string = getEnvVariable("defaultUsername");

describe("Switch user page", () => {
  beforeEach(() => {
    cy.viewport(1500, 2000);
  });
  it("should redirect if user not logged in", () => {
    SwitchUserPage.visit();
    cy.url().should("not.contain", SWITCH_USER_URL);
  });

  it("should fail to load users if user is an Investigator", () => {
    USERNAME = getEnvVariable("investigator");
    cy.task("updateUserPassword", USERNAME).then((password: string) => {
      // When I login
      LoginPage.visit();
      LoginPage.login(USERNAME, password);
    });
    SwitchUserPage.visit();
    SwitchUserPage.hasLoadingError();
  });

  it("should fail to load users if the user is not an administrator", () => {
    USERNAME = getEnvVariable("pcUsername");
    cy.task("updateUserPassword", USERNAME).then((password: string) => {
      // When I login
      LoginPage.visit();
      LoginPage.login(USERNAME, password);
    });
    SwitchUserPage.visit();
    SwitchUserPage.hasLoadingError();
  });

  it("should switch to the selected user", () => {
    cy.task("updateUserPassword", USERNAME).then((password: string) => {
      // When I login
      LoginPage.visit();
      LoginPage.login(USERNAME, password);
      SwitchUserPage.visit();
    });
    SwitchUserPage.selectUser("423");
    SwitchUserPage.switch();
    SwitchUserPage.checkName("Daniel");
  });
});
