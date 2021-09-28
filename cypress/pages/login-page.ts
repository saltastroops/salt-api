const LOGIN_URL = '/login';

export class LoginPage {
  static visit() {
    cy.visit(LOGIN_URL);
  }

  static typeUsername(username: string) {
    cy.get("[data-test='login-username']").type(username);
  }

  static typePassword(password: string) {
    cy.get("[data-test='login-password']").type(password);
  }

  static submit() {
    cy.get("[data-test='login-submit']").click();
  }
}
