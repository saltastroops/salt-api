import "cypress-network-idle";

import { currentSemester } from "../../../src/app/utils";
import { HomeUser } from "../../support/components/home-user";
import { HomePage } from "../../support/pages/home-page";
import { LoginPage } from "../../support/pages/login/login-page";
import { freezeDate, getApiUrl, getEnvVariable } from "../../support/utils";

const apiUrl = getApiUrl();

let USERNAME = getEnvVariable("defaultUsername");

describe("Home User", () => {
  beforeEach(() => {
    freezeDate(2020, 6);

    cy.intercept(apiUrl + "/login").as("login");

    cy.task("updateUserPassword", USERNAME).then((password: string) => {
      // When I login
      LoginPage.visit();
      LoginPage.login(USERNAME, password);
    });

    // And I visit the home page
    HomePage.visit();
  });

  it("should show an alert regarding the hard limit", () => {
    HomeUser.semesterRangeInputsDisabled(true);
    HomeUser.semesterSelectDisabled(true);
    cy.on("window:alert", (text) => {
      expect(text).contains(
        "1000 or more proposals satisfy the filter criteria.",
      );
    });
  });

  it("should show proposals for the current semester", () => {
    HomeUser.semesterRangeInputsDisabled(true);
    HomeUser.semesterSelectDisabled(true);
    HomeUser.clickCurrentSemesterRadioButton();
    HomeUser.filteredBySingleSemester(currentSemester());
  });

  it("should show proposals for the current semester when the page is reloaded after clicking the current semester filter", () => {
    HomeUser.clickCurrentSemesterRadioButton();
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.filteredBySingleSemester(currentSemester());
    cy.reload();
    HomeUser.currentSemesterRadioButtonChecked(true);
    HomeUser.filteredBySingleSemester(currentSemester());
  });

  it("should show proposals for the current and next semester", () => {
    HomeUser.clickCurrentAndNextSemesterRadioButton();
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.filteredByCurrentAndNextSemester();
  });

  it("should show proposals for the current and next semester when the page is reloaded after clicking the current and next semester filter", () => {
    HomeUser.clickCurrentAndNextSemesterRadioButton();
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.filteredByCurrentAndNextSemester();
    cy.reload();
    HomeUser.currentAndNextSemesterRadioButtonChecked(true);
    HomeUser.filteredByCurrentAndNextSemester();
  });

  it("should show proposals for the given input semester range", () => {
    const start_semester = "2019-1";
    const end_semester = "2021-2";
    HomeUser.clickSemesterRangeRadioButton();
    HomeUser.semesterRangeInputsDisabled(false);
    HomeUser.semesterSelectDisabled(true);
    HomeUser.typeSemesterRanges(start_semester, end_semester);
    HomeUser.clickApplyButton();
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.filteredBySemesterRange(start_semester, end_semester);
  });

  it("should show proposals for the given input semester range when the page is reloaded after clicking the semester range filter", () => {
    const start_semester = "2018-1";
    const end_semester = "2020-2";
    HomeUser.clickSemesterRangeRadioButton();
    HomeUser.typeSemesterRanges(start_semester, end_semester);
    HomeUser.clickApplyButton();
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.filteredBySemesterRange(start_semester, end_semester);
    cy.reload();
    HomeUser.semesterRangeRadioButtonChecked(true);
    HomeUser.filteredBySemesterRange(start_semester, end_semester);
  });

  it("should show an error message when no input semester is provided", () => {
    HomeUser.clickSemesterRangeRadioButton();
    HomeUser.clickApplyButton();
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.noInputSemesterError();
  });

  it("should trigger an alert when a wrong input semester is provided", () => {
    const start_semester = "2010-3";
    HomeUser.clickSemesterRangeRadioButton();
    HomeUser.typeSemesterRanges(start_semester, "");
    HomeUser.clickApplyButton();
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.wrongInputSemesterError(start_semester);
  });

  it("should trigger an alert and show no proposals when a wrong input semester is provided and the page is reloaded", () => {
    const start_semester = "2010-3";
    HomeUser.clickSemesterRangeRadioButton();
    HomeUser.typeSemesterRanges(start_semester, "");
    HomeUser.clickApplyButton();
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.wrongInputSemesterError(start_semester);
    cy.reload();
    HomeUser.wrongInputSemesterError(start_semester);
    HomeUser.proposalsListEmpty();
  });

  it("should show proposals from the given input start semester onwards", () => {
    const start_semester = "2018-1";
    HomeUser.clickSemesterRangeRadioButton();
    HomeUser.typeSemesterRanges(start_semester, "");
    HomeUser.clickApplyButton();
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.filteredBySemesterRange(start_semester, "");
  });

  it("should show proposals up to the given input semester", () => {
    const end_semester = "2018-1";
    HomeUser.clickSemesterRangeRadioButton();
    HomeUser.typeSemesterRanges("", end_semester);
    HomeUser.clickApplyButton();
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.filteredBySemesterRange("", end_semester);
  });

  it("should show proposals for the selected semester when the semester is selected from the options", () => {
    const select_semester = "2020-1";
    HomeUser.clickSingleSemesterRadioButton();
    HomeUser.semesterRangeInputsDisabled(true);
    HomeUser.semesterSelectDisabled(false);
    HomeUser.selectSemester(select_semester);
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.filteredBySingleSemester(select_semester);
  });

  it("should show proposals for the selected semester when the semester is selected from the options and the page is reloaded", () => {
    const select_semester = "2020-1";
    HomeUser.clickSingleSemesterRadioButton();
    HomeUser.selectSemester(select_semester);
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.filteredBySingleSemester(select_semester);
    cy.reload();
    HomeUser.singleSemesterRadioButtonChecked(true);
    HomeUser.filteredBySingleSemester(select_semester);
  });

  it("should show proposals for the current and then show proposals for the selected semester", () => {
    const select_semester = "2018-1";
    HomeUser.clickCurrentSemesterRadioButton();
    HomeUser.filteredBySingleSemester(currentSemester());
    HomeUser.clickSingleSemesterRadioButton();
    HomeUser.selectSemester(select_semester);
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.filteredBySingleSemester(select_semester);
  });

  it("should show only unchecked proposals", () => {
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.clickUncheckedCheckbox();
    HomeUser.filteredUncheckedProposals();
  });

  it("should show only unchecked proposals when the unchecked checkbox is checked and the page is reloaded", () => {
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.clickUncheckedCheckbox();
    HomeUser.filteredUncheckedProposals();
    cy.reload();
    HomeUser.uncheckedFilterCheckboxChecked(true);
    HomeUser.filteredUncheckedProposals();
  });

  it("should show only unassigned proposals", () => {
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.clickUnassignedCheckbox();
    HomeUser.filteredUnassignedProposals();
  });

  it("should show only unassigned proposals when the unassigned checkbox is checked and the page is reloaded", () => {
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.clickUnassignedCheckbox();
    HomeUser.filteredUnassignedProposals();
    cy.reload();
    HomeUser.unassignedFilterCheckboxChecked(true);
    HomeUser.filteredUnassignedProposals();
  });

  it("should show only completed proposals", () => {
    const start_semester = "2006-1";
    HomeUser.clickSemesterRangeRadioButton();
    HomeUser.typeSemesterRanges(start_semester, "");
    HomeUser.clickApplyButton();
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.clickCompletedCheckbox();
    HomeUser.filteredCompletedProposals();
  });

  it("should show only completed proposals when the completed checkbox is clicked and the page is reloaded", () => {
    const start_semester = "2006-1";
    HomeUser.clickSemesterRangeRadioButton();
    HomeUser.typeSemesterRanges(start_semester, "");
    HomeUser.clickApplyButton();
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.clickCompletedCheckbox();
    HomeUser.filteredCompletedProposals();
    cy.reload();
    HomeUser.completedFilterCheckboxChecked(true);
    HomeUser.filteredCompletedProposals();
  });

  it("should show only rejected, completed and expired proposals", () => {
    const start_semester = "2006-1";
    HomeUser.clickSemesterRangeRadioButton();
    HomeUser.typeSemesterRanges(start_semester, "");
    HomeUser.clickApplyButton();
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.clickRejectedCompletedExpiredCheckbox();
    HomeUser.filteredRejectedCompletedExpiredProposals();
  });

  it("should show only active proposals when the active checkbox is clicked", () => {
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.clickActiveCheckbox();
    HomeUser.filteredActiveProposals();
  });

  it("should show only active proposals when the active checkbox is clicked and the page is reloaded", () => {
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.clickActiveCheckbox();
    HomeUser.filteredActiveProposals();
    cy.reload();
    HomeUser.activeFilterCheckboxChecked(true);
    HomeUser.filteredActiveProposals();
  });

  it("should show only DDT proposals when the DDT checkbox is clicked", () => {
    const start_semester = "2006-1";
    HomeUser.clickSemesterRangeRadioButton();
    HomeUser.typeSemesterRanges(start_semester, "");
    HomeUser.clickApplyButton();
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.clickDDTCheckbox();
    HomeUser.filteredDDTProposals();
  });

  it("should show only DDT proposals when the DDT checkbox is clicked and the page is reloaded", () => {
    const start_semester = "2006-1";
    HomeUser.clickSemesterRangeRadioButton();
    HomeUser.typeSemesterRanges(start_semester, "");
    HomeUser.clickApplyButton();
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.clickDDTCheckbox();
    HomeUser.filteredDDTProposals();
    cy.reload();
    HomeUser.ddtFilterCheckboxChecked(true);
    HomeUser.filteredDDTProposals();
  });

  it("should show only non-GW proposals by default", () => {
    const start_semester = "2019-1";
    HomeUser.clickSemesterRangeRadioButton();
    HomeUser.typeSemesterRanges(start_semester, "");
    HomeUser.clickApplyButton();
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.filteredNonGWProposals();
  });

  it("should show GW proposals as well when the GW checkbox is clicked", () => {
    const start_semester = "2019-1";
    HomeUser.clickSemesterRangeRadioButton();
    HomeUser.typeSemesterRanges(start_semester, "");
    HomeUser.clickApplyButton();
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.clickNonGWCheckbox();
    HomeUser.includedGWProposal();
  });

  it("should show GW proposals as well when the GW checkbox is clicked and the page is reloaded", () => {
    const start_semester = "2019-1";
    HomeUser.clickSemesterRangeRadioButton();
    HomeUser.typeSemesterRanges(start_semester, "");
    HomeUser.clickApplyButton();
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.clickNonGWCheckbox();
    HomeUser.includedGWProposal();
    cy.reload();
    HomeUser.nonGWFilterCheckboxChecked(true);
    HomeUser.includedGWProposal();
  });

  it("should show only ORP proposals when the ORP checkbox is clicked", () => {
    const start_semester = "2021-1";
    HomeUser.clickSemesterRangeRadioButton();
    HomeUser.typeSemesterRanges(start_semester, "");
    HomeUser.clickApplyButton();
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.clickORPCheckbox();
    HomeUser.filteredORPProposals();
  });

  it("should show only ORP proposals when the ORP checkbox is clicked and the page is reloaded", () => {
    const start_semester = "2019-1";
    HomeUser.clickSemesterRangeRadioButton();
    HomeUser.typeSemesterRanges(start_semester, "");
    HomeUser.clickApplyButton();
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.clickORPCheckbox();
    HomeUser.filteredORPProposals();
    cy.reload();
    HomeUser.orpFilterCheckboxChecked(true);
    HomeUser.filteredORPProposals();
  });

  it("should show only commissioning proposals when the commissioning checkbox is clicked", () => {
    const start_semester = "2006-1";
    HomeUser.clickSemesterRangeRadioButton();
    HomeUser.typeSemesterRanges(start_semester, "");
    HomeUser.clickApplyButton();
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.clickCommissioningCheckbox();
    HomeUser.filteredCommissioningProposals();
  });

  it("should show only commissioning proposals when the commissioning checkbox is clicked and the page is reloaded", () => {
    const start_semester = "2006-1";
    HomeUser.clickSemesterRangeRadioButton();
    HomeUser.typeSemesterRanges(start_semester, "");
    HomeUser.clickApplyButton();
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.clickCommissioningCheckbox();
    HomeUser.filteredCommissioningProposals();
    cy.reload();
    HomeUser.commissioningFilterCheckboxChecked(true);
    HomeUser.filteredCommissioningProposals();
  });

  it("should show only science proposals when the science checkbox is clicked", () => {
    HomeUser.clickScienceCheckbox();
    HomeUser.filteredScienceProposals();
  });

  it("should show only science proposals when the science checkbox is clicked and the page is reloaded", () => {
    HomeUser.clickScienceCheckbox();
    HomeUser.filteredScienceProposals();
    cy.reload();
    HomeUser.scienceFilterCheckboxChecked(true);
    HomeUser.filteredScienceProposals();
  });

  it("should show current and next semester, and additionally filter unchecked proposals", () => {
    HomeUser.semesterRangeInputsDisabled(true);
    HomeUser.semesterSelectDisabled(true);
    freezeDate(2021, 6);
    HomeUser.clickCurrentAndNextSemesterRadioButton();
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.filteredByCurrentAndNextSemester();
    HomeUser.clickUncheckedCheckbox();
    HomeUser.filteredUncheckedProposals();
  });

  it("should show only phase 1 proposals", () => {
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.clickPhase1Checkbox();
    HomeUser.filteredPhase1Proposals();
  });

  it("should show only phase 1 proposals when phase 1 checkbox is checked and the page is reloaded", () => {
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.clickPhase1Checkbox();
    HomeUser.filteredPhase1Proposals();
    cy.reload();
    HomeUser.phase1FilterCheckboxChecked(true);
    HomeUser.filteredPhase1Proposals();
  });

  it("should show only phase 2 proposals", () => {
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.clickPhase2Checkbox();
    HomeUser.filteredPhase2Proposals();
  });

  it("should show only phase 2 proposals when phase 2 checkbox is checked and the page is reloaded", () => {
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.clickPhase2Checkbox();
    HomeUser.filteredPhase2Proposals();
    cy.reload();
    HomeUser.phase2FilterCheckboxChecked(true);
    HomeUser.filteredPhase2Proposals();
  });

  it("should have the table sorted by ids when the proposal id column is clicked", () => {
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.clickProposalIdColumn();
    HomeUser.proposalsSortedBy("id", "ascending");
    HomeUser.clickProposalIdColumn();
    HomeUser.proposalsSortedBy("id", "descending");
  });

  it("should have the table sorted by codes when the proposal code column is clicked", () => {
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.clickProposalCodeColumn();
    HomeUser.proposalsSortedBy("code", "ascending");
    HomeUser.clickProposalCodeColumn();
    HomeUser.proposalsSortedBy("code", "descending");
  });

  it("should have the table sorted by titles when the proposal title column is clicked", () => {
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.clickProposalTitleColumn();
    HomeUser.proposalsSortedBy("title", "ascending");
    HomeUser.clickProposalTitleColumn();
    HomeUser.proposalsSortedBy("title", "descending");
  });

  it("should have the table sorted by semesters when the proposal semester column is clicked", () => {
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.clickProposalSemesterColumn();
    HomeUser.proposalsSortedBy("semester", "ascending");
    HomeUser.clickProposalSemesterColumn();
    HomeUser.proposalsSortedBy("semester", "descending");
  });

  it("should have the table sorted by phases when the proposal phase column is clicked", () => {
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.clickProposalPhaseColumn();
    HomeUser.proposalsSortedBy("phase", "ascending");
    HomeUser.clickProposalPhaseColumn();
    HomeUser.proposalsSortedBy("phase", "descending");
  });

  it("should have the table sorted by statuses when the proposal status column is clicked", () => {
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.clickProposalStatusColumn();
    HomeUser.proposalsSortedBy("status", "ascending");
    HomeUser.clickProposalStatusColumn();
    HomeUser.proposalsSortedBy("status", "descending");
  });

  it("should have the table sorted by types when the proposal type column is clicked", () => {
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.clickProposalTypeColumn();
    HomeUser.proposalsSortedBy("type", "ascending");
    HomeUser.clickProposalTypeColumn();
    HomeUser.proposalsSortedBy("type", "descending");
  });

  it("should have the table sorted by astronomers when the proposal astronomer column is clicked", () => {
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.clickProposalAstronomerColumn();
    HomeUser.proposalsSortedBy("astronomer", "ascending");
    HomeUser.clickProposalAstronomerColumn();
    HomeUser.proposalsSortedBy("astronomer", "descending");
  });

  it("should have the table correctly sorted when the proposal id column is clicked three times", () => {
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.clickProposalIdColumn();
    HomeUser.proposalsSortedBy("id", "ascending");
    HomeUser.clickProposalIdColumn();
    HomeUser.proposalsSortedBy("id", "descending");
    HomeUser.clickProposalIdColumn();
    HomeUser.proposalsSortedBy("id", "ascending");
  });
});

describe("Home User - Investigator", () => {
  beforeEach(() => {
    USERNAME = getEnvVariable("piUsername");
    cy.intercept(apiUrl + "/login").as("login");

    cy.intercept(apiUrl + "/user").as("user");

    cy.intercept(apiUrl + "/proposals/**").as("proposals");
    cy.task("updateUserPassword", USERNAME).then((password: string) => {
      // Given I am logged in
      LoginPage.visit();
      LoginPage.login(USERNAME, password);
    });

    // And I visit the home page
    HomePage.visit();
  });

  it("should show investigator's proposals only", () => {
    const proposalCodes = [
      "2016-2-LSP-001",
      "2017-1-DDT-009",
      "2017-1-SCI-012",
      "2017-1-SCI-007",
    ];
    HomeUser.clickSingleSemesterRadioButton();
    HomeUser.selectSemester("2017-1");
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.clickMyProposalsCheckbox();
    HomeUser.filteredMyProposals(proposalCodes);
  });
});

describe("Home User - SALT Astronomer", () => {
  beforeEach(() => {
    USERNAME = getEnvVariable("saltAstronomerUsername");
    cy.intercept(apiUrl + "/login").as("login");

    cy.intercept(apiUrl + "/user").as("user");

    cy.intercept(apiUrl + "/proposals/**").as("proposals");
    cy.task("updateUserPassword", USERNAME).then((password: string) => {
      // Given I am logged in
      LoginPage.visit();
      LoginPage.login(USERNAME, password);
    });

    // And I visit the home page
    HomePage.visit();
  });

  it("should show only proposals requiring astronomer's attention", () => {
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.clickRequiringAttentionCheckbox();
    HomeUser.filteredProposalsRequiringAttention(USERNAME);
  });

  it("should show only astronomer's proposals", () => {
    const proposalCodes = [
      "2018-2-SCI-020",
      "2018-2-MLT-007",
      "2017-1-MLT-014",
      "2017-2-MLT-003",
      "2018-2-SCI-002",
    ];
    HomeUser.clickSingleSemesterRadioButton();
    HomeUser.selectSemester("2018-2");
    cy.waitForNetworkIdle(apiUrl + "/*", "*", 2000);
    HomeUser.clickMyProposalsCheckbox();
    HomeUser.filteredMyProposals(proposalCodes);
  });
});
