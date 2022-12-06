import { LoginPage } from "../../support/pages/login/login-page";
import { ProposalPage } from "../../support/pages/proposal-page";
import {
  forceNetworkError,
  forceServerError,
  getApiUrl,
  interceptIndefinitely,
  userDetailsAreStored,
} from "../../support/utils";

const apiUrl = getApiUrl();

const USERNAME = "hettlage";

const PROPOSAL_CODE = "2020-1-DDT-009";

describe("Proposal loading", () => {
  beforeEach(() => {
    cy.recordHttp(apiUrl + "/login").as("login");

    cy.recordHttp(apiUrl + "/user").as("user");

    cy.task("updateUserPassword", USERNAME).then((password: string) => {
      // When I login
      LoginPage.visit();
      LoginPage.login(USERNAME, password);
    });
  });

  it("should be indicated", () => {
    interceptIndefinitely(apiUrl + "/proposals/**", {});

    ProposalPage.visit(PROPOSAL_CODE);

    cy.get(".loading").should("exist");
  });

  it("should not be indicated any longer after loading is complete", () => {
    cy.recordHttp(apiUrl + "/proposals/**").as("proposals");

    ProposalPage.visit(PROPOSAL_CODE);
    cy.wait("@proposals");

    cy.get(".loading").should("not.exist");
  });

  it("should show an error if there is an error", () => {
    forceNetworkError(apiUrl + "/proposals/**");

    ProposalPage.visit(PROPOSAL_CODE);

    cy.get(".error").should("exist");
    cy.get(".loading").should("not.exist");
  });
});
