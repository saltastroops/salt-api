import { BlockSummaries } from "../../support/components/block-summaries";
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

  it("should have checkboxes deselected initially", () => {
    BlockSummaries.filterCompletedChecked(false);
    BlockSummaries.filterUnobservableChecked(false);
  });

  it("should filter completed blocks when the filter-completed checkbox is clicked", () => {
    BlockSummaries.hasCompletedBlocks(true);
    BlockSummaries.clickFilterCompleted();
    BlockSummaries.filterCompletedChecked(true);
    BlockSummaries.filterUnobservableChecked(false);
    BlockSummaries.hasCompletedBlocks(false);
  });

  it("should filter unobservable blocks when the filter-unobservable checkbox is clicked", () => {
    BlockSummaries.hasUnobservableBlocks(true);
    BlockSummaries.clickFilterUnobservable();
    BlockSummaries.filterUnobservableChecked(true);
    BlockSummaries.filterCompletedChecked(false);
    BlockSummaries.hasUnobservableBlocks(false);
  });

  it("should filter unobservable and completed blocks when the checkboxes are clicked", () => {
    BlockSummaries.hasCompletedBlocks(true);
    BlockSummaries.hasUnobservableBlocks(true);
    BlockSummaries.clickFilterCompleted();
    BlockSummaries.clickFilterUnobservable();
    BlockSummaries.filterCompletedChecked(true);
    BlockSummaries.filterUnobservableChecked(true);
    BlockSummaries.hasCompletedBlocks(false);
    BlockSummaries.hasUnobservableBlocks(false);
  });

  it("should have the checkboxes still checked and content filtered when the checkboxes are clicked the page is reloaded", () => {
    BlockSummaries.hasCompletedBlocks(true);
    BlockSummaries.hasUnobservableBlocks(true);
    BlockSummaries.clickFilterCompleted();
    BlockSummaries.clickFilterUnobservable();
    cy.reload();
    BlockSummaries.filterCompletedChecked(true);
    BlockSummaries.filterUnobservableChecked(true);
    BlockSummaries.hasCompletedBlocks(false);
    BlockSummaries.hasUnobservableBlocks(false);
  });

  it("should have the table sorted by IDs when the block ID column is clicked", () => {
    BlockSummaries.clickBlockIdColumn();
    BlockSummaries.blocksSortedBy("id", "ascending");
    BlockSummaries.clickBlockIdColumn();
    BlockSummaries.blocksSortedBy("id", "descending");
  });

  it("should have the table sorted by names when the block name column is clicked", () => {
    BlockSummaries.clickBlockNameColumn();
    BlockSummaries.blocksSortedBy("name", "ascending");
    BlockSummaries.clickBlockNameColumn();
    BlockSummaries.blocksSortedBy("name", "descending");
  });

  it("should have the table sorted by observation time when the observation time column is clicked", () => {
    BlockSummaries.clickBlockObservationTimeColumn();
    BlockSummaries.blocksSortedBy("observation-time", "ascending");
    BlockSummaries.clickBlockObservationTimeColumn();
    BlockSummaries.blocksSortedBy("observation-time", "descending");
  });

  it("should have the table sorted by priority when the priority column is clicked", () => {
    BlockSummaries.clickBlockPriorityColumn();
    BlockSummaries.blocksSortedBy("priority", "ascending");
    BlockSummaries.clickBlockPriorityColumn();
    BlockSummaries.blocksSortedBy("priority", "descending");
  });

  it("should have the table sorted by maximum seeing when the maximum seeing column is clicked", () => {
    BlockSummaries.clickBlockMaximumSeeingColumn();
    BlockSummaries.blocksSortedBy("maximum-seeing", "ascending");
    BlockSummaries.clickBlockMaximumSeeingColumn();
    BlockSummaries.blocksSortedBy("maximum-seeing", "descending");
  });

  it("should have the table sorted by remaining nights when the remaining nights column is clicked", () => {
    BlockSummaries.clickBlockRemainingNightsColumn();
    BlockSummaries.blocksSortedBy("remaining-nights", "ascending");
    BlockSummaries.clickBlockRemainingNightsColumn();
    BlockSummaries.blocksSortedBy("remaining-nights", "descending");
  });

  it("should have the table sorted by maximum lunar phase when the maximum lunar phase column is clicked", () => {
    BlockSummaries.clickBlockMaximumLunarPhaseColumn();
    BlockSummaries.blocksSortedBy("maximum-lunar-phase", "ascending");
    BlockSummaries.clickBlockMaximumLunarPhaseColumn();
    BlockSummaries.blocksSortedBy("maximum-lunar-phase", "descending");
  });

  it("should have the table sorted correctly when clicking on different columns", () => {
    BlockSummaries.clickBlockNameColumn();
    BlockSummaries.blocksSortedBy("name", "ascending");
    BlockSummaries.clickBlockNameColumn();
    BlockSummaries.blocksSortedBy("name", "descending");
    BlockSummaries.clickBlockMaximumLunarPhaseColumn();
    BlockSummaries.blocksSortedBy("maximum-lunar-phase", "ascending");
    BlockSummaries.clickBlockNameColumn();
    BlockSummaries.blocksSortedBy("name", "ascending");
  });

  it("should load the correct block content when a block name link is clicked", () => {
    BlockSummaries.clickBlockNameLink(4);
    BlockSummaries.correctBlockLoaded(4);
  });
});
