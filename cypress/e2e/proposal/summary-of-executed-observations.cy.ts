import { SummaryOfExecutedObservations } from "../../support/components/summary-of-executed-observations";
import { LoginPage } from "../../support/pages/login/login-page";
import { ProposalPage } from "../../support/pages/proposal-page";
import { getApiUrl, userDetailsAreStored } from "../../support/utils";

const apiUrl = getApiUrl();

const USERNAME = "hettlage";

describe("Block summaries", () => {
  const PROPOSAL_CODE = "2021-2-LSP-001";

  beforeEach(() => {
    cy.recordHttp(apiUrl + "/token").as("token");

    cy.recordHttp(apiUrl + "/user").as("user");

    cy.recordHttp(apiUrl + "/proposals/**").as("proposals");

    cy.recordHttp(apiUrl + "/blocks/**").as("blocks");

    cy.task("updateUserPassword", USERNAME).then((password: string) => {
      // When I login
      LoginPage.visit();
      LoginPage.login(USERNAME, password);
    });
    // Then user details are stored
    userDetailsAreStored();

    // And I visit a proposal page
    ProposalPage.visit(PROPOSAL_CODE);
  });

  it("should load the correct block content when a block name link is clicked", () => {
    SummaryOfExecutedObservations.clickBlockNameLink(8);
    SummaryOfExecutedObservations.correctBlockLoaded(8);
  });
});
