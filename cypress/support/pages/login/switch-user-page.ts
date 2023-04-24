export const SWITCH_USER_URL = "/switch-user/";

export class SwitchUserPage {
  static visit(): void {
    cy.visit("/switch-user");
  }

  static hasLoadingError(): void {
    cy.get("[data-test='error']")
      .should("be.visible")
      .and("contains.text", /Failed to fetch users/i);
  }

  static hasSelector(): void {
    cy.get("[data-test='switch-user-selector']").should("be.visible");
  }

  static hasSwitchButton(): void {
    cy.get("[data-test='switch-button']")
      .should("be.visible")
      .and("contains.text", "Switch");
  }

  static selectHasValues(value: number): void {
    cy.get("[data-test='switch-user-selector']")
      .should("be.visible")
      .and("have.value", `${value}`);
  }

  static selectUser(select_index: string): void {
    cy.get("[data-test='switch-user-selector']").select(select_index);
  }

  static switch(): void {
    cy.get("[data-test='switch-button']").click();
  }

  static checkName(name: string): void {
    cy.get("[data-test='welcome-message']")
      .should("be.visible")
      .and("contains.text", name);
  }
}
