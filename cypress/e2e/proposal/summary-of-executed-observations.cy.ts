import { SummaryOfExecutedObservations } from "../../support/components/summary-of-executed-observations";
import { LoginPage } from "../../support/pages/login/login-page";
import { ProposalPage } from "../../support/pages/proposal-page";
import { getApiUrl, userDetailsAreStored } from "../../support/utils";

const apiUrl = getApiUrl();

const USERNAME = "hettlage";

describe("Block summaries", () => {
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
    // Then user details are stored
    userDetailsAreStored();

    // And I visit a proposal page
    ProposalPage.visit(PROPOSAL_CODE);
  });

  it("should load the correct block content when a block name link is clicked", () => {
    SummaryOfExecutedObservations.clickBlockNameLink(1);
    SummaryOfExecutedObservations.correctBlockLoaded(1);
  });

  it("should have the table sorted by names when the block name column is clicked", () => {
    SummaryOfExecutedObservations.clickBlockNameColumn();
    SummaryOfExecutedObservations.blocksSortedBy("block-name", "ascending");
    SummaryOfExecutedObservations.clickBlockNameColumn();
    SummaryOfExecutedObservations.blocksSortedBy("block-name", "descending");
  });

  it("should have the table sorted by observation time when the observation time column is clicked", () => {
    SummaryOfExecutedObservations.clickBlockObservationTimeColumn();
    SummaryOfExecutedObservations.blocksSortedBy(
      "observation-time",
      "ascending",
    );
    SummaryOfExecutedObservations.clickBlockObservationTimeColumn();
    SummaryOfExecutedObservations.blocksSortedBy(
      "observation-time",
      "descending",
    );
  });

  it("should have the table sorted by priority when the priority column is clicked", () => {
    SummaryOfExecutedObservations.clickBlockPriorityColumn();
    SummaryOfExecutedObservations.blocksSortedBy("priority", "ascending");
    SummaryOfExecutedObservations.clickBlockPriorityColumn();
    SummaryOfExecutedObservations.blocksSortedBy("priority", "descending");
  });

  it("should have the table sorted by maximum lunar phase when the maximum lunar phase column is clicked", () => {
    SummaryOfExecutedObservations.clickBlockMaximumLunarPhaseColumn();
    SummaryOfExecutedObservations.blocksSortedBy(
      "maximum-lunar-phase",
      "ascending",
    );
    SummaryOfExecutedObservations.clickBlockMaximumLunarPhaseColumn();
    SummaryOfExecutedObservations.blocksSortedBy(
      "maximum-lunar-phase",
      "descending",
    );
  });

  it("should have the table sorted correctly when clicking on different columns", () => {
    SummaryOfExecutedObservations.clickBlockPriorityColumn();
    SummaryOfExecutedObservations.blocksSortedBy("priority", "ascending");
    SummaryOfExecutedObservations.clickBlockPriorityColumn();
    SummaryOfExecutedObservations.blocksSortedBy("priority", "descending");
    SummaryOfExecutedObservations.clickBlockMaximumLunarPhaseColumn();
    SummaryOfExecutedObservations.blocksSortedBy(
      "maximum-lunar-phase",
      "ascending",
    );
    SummaryOfExecutedObservations.clickBlockNameColumn();
    SummaryOfExecutedObservations.blocksSortedBy("block-name", "ascending");
  });

  it("should have the table sorted by targets when the targets column is clicked", () => {
    SummaryOfExecutedObservations.clickBlockTargetsColumn();
    SummaryOfExecutedObservations.blocksSortedBy("targets", "ascending");
    SummaryOfExecutedObservations.clickBlockTargetsColumn();
    SummaryOfExecutedObservations.blocksSortedBy("targets", "descending");
  });

  it("should have the table sorted by observation date when the observation date column is clicked", () => {
    SummaryOfExecutedObservations.clickBlockObservationDateColumn();
    SummaryOfExecutedObservations.blocksSortedBy(
      "observation-date",
      "ascending",
    );
    SummaryOfExecutedObservations.clickBlockObservationDateColumn();
    SummaryOfExecutedObservations.blocksSortedBy(
      "observation-date",
      "descending",
    );
  });

  it("should have the table sorted by observation status when the observation status column is clicked", () => {
    SummaryOfExecutedObservations.clickBlockObservationStatusColumn();
    SummaryOfExecutedObservations.blocksSortedBy(
      "observation-status",
      "ascending",
    );
    SummaryOfExecutedObservations.clickBlockObservationStatusColumn();
    SummaryOfExecutedObservations.blocksSortedBy(
      "observation-status",
      "descending",
    );
  });

  it("should have the table sorted correctly when the block name column ia clicked three times", () => {
    SummaryOfExecutedObservations.clickBlockNameColumn();
    SummaryOfExecutedObservations.blocksSortedBy("block-name", "ascending");
    SummaryOfExecutedObservations.clickBlockNameColumn();
    SummaryOfExecutedObservations.blocksSortedBy("block-name", "descending");
    SummaryOfExecutedObservations.clickBlockNameColumn();
    SummaryOfExecutedObservations.blocksSortedBy("block-name", "ascending");
  });
});
