import { Investigators } from "../../support/components/investigators";
import { LoginPage } from "../../support/pages/login/login-page";
import { ProposalPage } from "../../support/pages/proposal-page";
import { getApiUrl, getEnvVariable } from "../../support/utils";

const apiUrl = getApiUrl();

describe("Investigators", () => {
  const USERNAME = getEnvVariable("investigator");

  const PROPOSAL_CODE = "2019-2-SCI-006";

  beforeEach(() => {
    cy.recordHttp(apiUrl + "/login").as("login");

    cy.recordHttp(apiUrl + "/user").as("user");

    cy.recordHttp(apiUrl + "/proposals/**").as("proposals");

    cy.recordHttp(apiUrl + "/blocks/**").as("blocks");

    cy.task("updateUserPassword", USERNAME).then((password: string) => {
      // When I login as the investigator
      LoginPage.visit();
      LoginPage.login(USERNAME, password);
    });

    // And I visit a proposal page
    ProposalPage.visit(PROPOSAL_CODE);
  });

  it("should show investigator's proposal approval status column for investigators", () => {
    Investigators.approvalStatusColumnHidden(false);
  });

  it(
    "should show an investigator the proposal approval status button for themselves only, other investigators'" +
      " buttons are hidden.",
    () => {
      Investigators.investigatorApprovalStatusButtonHidden(0, true);
      Investigators.investigatorApprovalStatusButtonHidden(1, true);
      Investigators.investigatorApprovalStatusButtonHidden(2, true);
      Investigators.investigatorApprovalStatusButtonHidden(3, false);
    },
  );

  it("should update approval status when the investigator click on their status button", () => {
    Investigators.clickApprovalButton(3);
    Investigators.approvalStatusButtonUpdatedWithStatus(3, "Reject");
    cy.wait(1500);
    Investigators.clickApprovalButton(3);
    Investigators.approvalStatusButtonUpdatedWithStatus(3, "Accept");
  });
});

describe("Investigators - administrators", () => {
  const USERNAME = getEnvVariable("administrator");
  const PROPOSAL_CODE = "2019-1-SCI-014";

  beforeEach(() => {
    cy.recordHttp(apiUrl + "/login").as("login");

    cy.recordHttp(apiUrl + "/user").as("user");

    cy.recordHttp(apiUrl + "/proposals/**").as("proposals");

    cy.recordHttp(apiUrl + "/blocks/**").as("blocks");

    cy.task("updateUserPassword", USERNAME).then((password: string) => {
      // When I login as the adminstrator
      LoginPage.visit();
      LoginPage.login(USERNAME, password);
    });

    // And I visit a proposal page
    ProposalPage.visit(PROPOSAL_CODE);
  });

  it("should show investigator's proposal approval status button for administrator", () => {
    Investigators.approvalStatusColumnHidden(false);
  });

  it("should show an administrator the proposal approval status button for all investigators", () => {
    Investigators.investigatorApprovalStatusButtonHidden(0, false);
    Investigators.investigatorApprovalStatusButtonHidden(1, false);
    Investigators.investigatorApprovalStatusButtonHidden(2, false);
    Investigators.investigatorApprovalStatusButtonHidden(3, false);
  });

  it("should update approval status when an administrator clicks on any status button for any investigator", () => {
    Investigators.clickApprovalButton(0);
    Investigators.approvalStatusButtonUpdatedWithStatus(0, "Reject");
    cy.wait(1500);
    Investigators.clickApprovalButton(0);
    Investigators.approvalStatusButtonUpdatedWithStatus(0, "Accept");
  });
});
