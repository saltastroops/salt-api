import { SummaryOfExecutedObservations } from "../../support/components/summary-of-executed-observations";
import { LoginPage } from "../../support/pages/login/login-page";
import { ProposalPage } from "../../support/pages/proposal-page";
import { getApiUrl, getEnvVariable } from "../../support/utils";

const apiUrl = getApiUrl();

describe("Block summaries", () => {
  const USERNAME = getEnvVariable("administrator");
  const PROPOSAL_CODE = "2020-1-DDT-009";

  beforeEach(() => {
    cy.intercept(apiUrl + "/login").as("login");

    cy.intercept(apiUrl + "/proposals/**").as("proposals");

    cy.intercept(apiUrl + "/block-visits/**").as("block-visits");

    cy.task("updateUserPassword", USERNAME).then((password: string) => {
      // When I login
      LoginPage.visit();
      LoginPage.login(USERNAME, password);
    });

    // And I visit a proposal page
    ProposalPage.visit(PROPOSAL_CODE);

    cy.wait("@proposals");

    // Show executed observations list
    SummaryOfExecutedObservations.clickShowObservationsLink();

    // Show observations of the selected semester
    SummaryOfExecutedObservations.showSemesterObservations(0);
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

  it("should have the table sorted correctly when the block name column is clicked three times", () => {
    SummaryOfExecutedObservations.clickBlockNameColumn();
    SummaryOfExecutedObservations.blocksSortedBy("block-name", "ascending");
    SummaryOfExecutedObservations.clickBlockNameColumn();
    SummaryOfExecutedObservations.blocksSortedBy("block-name", "descending");
    SummaryOfExecutedObservations.clickBlockNameColumn();
    SummaryOfExecutedObservations.blocksSortedBy("block-name", "ascending");
  });

  it("should show a button for editing block visit status", () => {
    SummaryOfExecutedObservations.submitBlockVisitStatusButtonHidden(1, false);
  });

  it("should show a modal for editing block visit status when clicking on the edit block visit status button", () => {
    SummaryOfExecutedObservations.editBlockStatusModalShown(false);
    SummaryOfExecutedObservations.clickEditBlockVisitStatus(1);
    SummaryOfExecutedObservations.editBlockStatusModalShown(true);
  });

  it(
    "should show an error message the submit button is clicked when status is set to reject and no reason is" +
      " selected",
    () => {
      SummaryOfExecutedObservations.editBlockStatusModalShown(false);
      SummaryOfExecutedObservations.clickEditBlockVisitStatus(1);
      SummaryOfExecutedObservations.editBlockStatusModalShown(true);
      SummaryOfExecutedObservations.selectBlockVisitStatus(2);
      SummaryOfExecutedObservations.clickSubmitBlockVisitStatus();
      SummaryOfExecutedObservations.errorContainsMessage(
        "The block rejection reason is required",
      );
    },
  );

  it(
    "should show an updated status when the submit button is clicked and status is set to reject and reason is" +
      " selected",
    () => {
      SummaryOfExecutedObservations.editBlockStatusModalShown(false);
      SummaryOfExecutedObservations.clickEditBlockVisitStatus(1);
      SummaryOfExecutedObservations.editBlockStatusModalShown(true);
      // Select "Rejected" status
      SummaryOfExecutedObservations.selectBlockVisitStatus(2);
      // Select "Telescope technical problems" rejection reason
      SummaryOfExecutedObservations.selectBlockRejectionReason(3);
      SummaryOfExecutedObservations.clickSubmitBlockVisitStatus();
      // Wait for the updates
      cy.wait("@block-visits");
      SummaryOfExecutedObservations.blockRejectionReasonUpdatedWithReason(
        1,
        "Telescope technical problems",
      );
    },
  );
});

describe("Block summaries - edit block visit status (SA)", () => {
  const USERNAME = getEnvVariable("saltAstronomerUsername");
  const PROPOSAL_CODE = "2020-1-DDT-009";

  beforeEach(() => {
    cy.intercept(apiUrl + "/login").as("login");

    cy.intercept(apiUrl + "/proposals/**").as("proposals");

    cy.task("updateUserPassword", USERNAME).then((password: string) => {
      // When I login
      LoginPage.visit();
      LoginPage.login(USERNAME, password);
    });

    // And I visit a proposal page
    ProposalPage.visit(PROPOSAL_CODE);

    cy.wait("@proposals");

    // Show executed observations list
    SummaryOfExecutedObservations.clickShowObservationsLink();

    // Show observations of the selected semester
    SummaryOfExecutedObservations.showSemesterObservations(0);
  });

  it("should show a button for editing block visit status for a SA", () => {
    SummaryOfExecutedObservations.submitBlockVisitStatusButtonHidden(1, false);
  });

  it("should show a modal for editing block visit status for a SA clicking on the edit block visit status button", () => {
    SummaryOfExecutedObservations.editBlockStatusModalShown(false);
    SummaryOfExecutedObservations.clickEditBlockVisitStatus(1);
    SummaryOfExecutedObservations.editBlockStatusModalShown(true);
  });
});

describe("Block summaries - edit block visit status (PI)", () => {
  const USERNAME = getEnvVariable("piUsername");
  const PROPOSAL_CODE = "2021-2-LSP-001";

  beforeEach(() => {
    cy.intercept(apiUrl + "/login").as("login");

    cy.intercept(apiUrl + "/proposals/**").as("proposals");

    cy.task("updateUserPassword", USERNAME).then((password: string) => {
      // When I login
      LoginPage.visit();
      LoginPage.login(USERNAME, password);
    });

    // And I visit a proposal page
    ProposalPage.visit(PROPOSAL_CODE);

    cy.wait("@proposals");

    // Show executed observations list
    SummaryOfExecutedObservations.clickShowObservationsLink();

    // Show observations of the selected semester
    SummaryOfExecutedObservations.showSemesterObservations(0);
  });

  it("should not show a button for editing block visit status for a PI", () => {
    SummaryOfExecutedObservations.submitBlockVisitStatusButtonHidden(1, true);
  });
});

describe("Block summaries - edit block visit status (PC)", () => {
  const USERNAME = getEnvVariable("pcUsername");
  const PROPOSAL_CODE = "2021-1-SCI-014";

  beforeEach(() => {
    cy.intercept(apiUrl + "/login").as("login");

    cy.intercept(apiUrl + "/proposals/**").as("proposals");

    cy.task("updateUserPassword", USERNAME).then((password: string) => {
      // When I login
      LoginPage.visit();
      LoginPage.login(USERNAME, password);
    });

    // And I visit a proposal page
    ProposalPage.visit(PROPOSAL_CODE);

    cy.wait("@proposals");

    // Show executed observations list
    SummaryOfExecutedObservations.clickShowObservationsLink();

    // Show observations of the selected semester
    SummaryOfExecutedObservations.showSemesterObservations(0);
  });

  it("should not show a button for editing block visit status for a PC", () => {
    SummaryOfExecutedObservations.submitBlockVisitStatusButtonHidden(1, true);
  });
});
