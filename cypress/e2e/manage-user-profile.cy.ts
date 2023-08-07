import {ManageUserProfilePage} from "../support/pages/manage-user-profile-page";
import {LoginPage} from "../support/pages/login/login-page";
import {getEnvVariable} from "../support/utils";
import {ManageUserProfile} from "../support/components/manage-user-profile";

let USERNAME = getEnvVariable("defaultUsername");
describe("Manage user profile", () => {
  beforeEach(() => {
    cy.task("updateUserPassword", USERNAME).then((password: string) => {
      // When I login
      LoginPage.visit();
      LoginPage.login(USERNAME, password);
    });

    ManageUserProfilePage.visit();
  });

  it('should show selected user\'s details', function () {
    const givenName = "Chaka";
    const familyName = "Mofokeng"
    ManageUserProfile.selectUser(familyName, givenName);
    ManageUserProfile.isUserSelected(familyName, givenName);
  });
})
