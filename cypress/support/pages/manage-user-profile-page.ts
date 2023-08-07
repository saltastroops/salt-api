const MANAGE_USER_PROFILE_URL = "manage-user-profile";

export class ManageUserProfilePage {
  static visit(): void {
    cy.visit(MANAGE_USER_PROFILE_URL);
  }
}
