import "cypress-network-idle";

import { LoginPage } from "../../support/pages/login/login-page";
import { ProposalPage } from "../../support/pages/proposal-page";
import { getApiUrl } from "../../support/utils";

describe("Finder charts", () => {
  const apiUrl = getApiUrl();

  const USERNAME = "hettlage";

  beforeEach(() => {
    cy.task("updateUserPassword", USERNAME).then((password: string) => {
      // Login
      LoginPage.visit();
      LoginPage.login(USERNAME, password);
    });

    const now = Date.UTC(2021, 3, 27, 19, 12, 3, 7);
    cy.clock(now, ["Date"]);
  });

  it("should show the correct finder chart validity date range", () => {
    ProposalPage.visit("2020-1-DDT-009");
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    cy.get('[data-test="finder-chart-validity"]')
      .contains("27 April 2021")
      .and("contain", "28 April 2021");
  });

  it("should show finder charts with no specific validity range", () => {
    ProposalPage.visit("2020-1-DDT-009");
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    cy.get('[data-test="finder-chart"]').should("have.length", 2);
  });

  it("should show only valid finder charts", () => {
    ProposalPage.visit("2020-2-SCI-043");
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    cy.get('[data-test="finder-chart"]').should("have.length", 2);
    cy.get(
      '[data-test="finder-chart"]:nth-of-type(1) td:nth-of-type(2)',
    ).should("contain.text", "27 April");
    cy.get(
      '[data-test="finder-chart"]:nth-of-type(2) td:nth-of-type(2)',
    ).should("contain.text", "27 April");
  });
});
