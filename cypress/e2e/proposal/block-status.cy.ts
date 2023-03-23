import { Block } from "../../support/components/block";
import { BlockSummaries } from "../../support/components/block-summaries";
import { LoginPage } from "../../support/pages/login/login-page";
import { ProposalPage } from "../../support/pages/proposal-page";
import { getApiUrl, getEnvVariable } from "../../support/utils";

const apiUrl = getApiUrl();

const USERNAME = getEnvVariable("defaultUsername");

describe("Block", () => {
  const PROPOSAL_CODE = "2019-1-SCI-014";

  beforeEach(() => {
    cy.recordHttp(apiUrl + "/login").as("login");

    cy.recordHttp(apiUrl + "/user").as("user");

    cy.recordHttp(apiUrl + "/proposals/**").as("proposals");

    cy.recordHttp(apiUrl + "/blocks/**").as("blocks");
    cy.task("updateUserPassword", USERNAME).then((password: string) => {
      // When I login
      LoginPage.visit();
      LoginPage.login(USERNAME, password);
    });

    // And I visit a proposal page
    ProposalPage.visit(PROPOSAL_CODE);
  });

  it("should not show edit block status modal before clicking edit button", () => {
    Block.editBlockStatusModalExists(false);
  });

  it("should show edit block status modal after clicking edit button", () => {
    BlockSummaries.clickBlockNameLink(0);
    Block.clickEditBlockStatusButton();
    Block.editBlockStatusModalExists(true);
  });

  it("should update the block status", () => {
    BlockSummaries.clickBlockNameLink(1);
    Block.clickEditBlockStatusButton();
    Block.selectBlockStatus("On hold");
    Block.clickSubmitButton();
    Block.blockStatusUpdatedWithStatus("On hold");
  });

  it("should update the block status and reason", () => {
    BlockSummaries.clickBlockNameLink(2);
    Block.clickEditBlockStatusButton();
    Block.selectBlockStatus("On hold");
    Block.typeBlockStatusReason("Time not available");
    Block.clickSubmitButton();
    cy.wait("@blocks");
    Block.blockStatusUpdatedWithStatus("On hold");
    Block.clickEditBlockStatusButton();
    Block.blockStatusReasonUpdatedWithReason("Time not available");
  });
});

describe("Block - edit block status (SA)", () => {
  const USERNAME = getEnvVariable("saltAstronomerUsername");
  const PROPOSAL_CODE = "2020-1-DDT-009";

  beforeEach(() => {
    cy.recordHttp(apiUrl + "/login").as("login");

    cy.recordHttp(apiUrl + "/user").as("user");

    cy.recordHttp(apiUrl + "/proposals/**").as("proposals");

    cy.recordHttp(apiUrl + "/blocks/**").as("blocks");

    cy.task("updateUserPassword", USERNAME).then((password: string) => {
      // When I login
      LoginPage.visit();
      LoginPage.login(USERNAME, password);
    });

    // And I visit a proposal page
    ProposalPage.visit(PROPOSAL_CODE);
  });

  it("should show a button for editing block status for a SA", () => {
    BlockSummaries.clickBlockNameLink(1);
    Block.editBlockStatusButtonExists(true);
  });
});

describe("Block - edit block status (PI)", () => {
  const USERNAME = getEnvVariable("piUsername");
  const PROPOSAL_CODE = "2018-2-LSP-001";

  beforeEach(() => {
    cy.recordHttp(apiUrl + "/login").as("login");

    cy.recordHttp(apiUrl + "/user").as("user");

    cy.recordHttp(apiUrl + "/proposals/**").as("proposals");

    cy.recordHttp(apiUrl + "/blocks/**").as("blocks");

    cy.task("updateUserPassword", USERNAME).then((password: string) => {
      // When I login
      LoginPage.visit();
      LoginPage.login(USERNAME, password);
    });

    // And I visit a proposal page
    ProposalPage.visit(PROPOSAL_CODE);
  });

  it("should show a button for editing block status for a PI", () => {
    BlockSummaries.clickBlockNameLink(-1);
    Block.editBlockStatusButtonExists(true);
  });
});

describe("Block - edit block status (PC)", () => {
  const USERNAME = getEnvVariable("pcUsername");
  const PROPOSAL_CODE = "2021-1-SCI-014";

  beforeEach(() => {
    cy.recordHttp(apiUrl + "/login").as("login");

    cy.recordHttp(apiUrl + "/user").as("user");

    cy.recordHttp(apiUrl + "/proposals/**").as("proposals");

    cy.recordHttp(apiUrl + "/blocks/**").as("blocks");

    cy.task("updateUserPassword", USERNAME).then((password: string) => {
      // When I login
      LoginPage.visit();
      LoginPage.login(USERNAME, password);
    });

    // And I visit a proposal page
    ProposalPage.visit(PROPOSAL_CODE);
  });

  it("should show a button for editing block status for a PC", () => {
    BlockSummaries.clickBlockNameLink(-1);
    Block.editBlockStatusButtonExists(true);
  });
});
