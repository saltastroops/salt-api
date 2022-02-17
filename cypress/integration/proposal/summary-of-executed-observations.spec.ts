import { SummaryOfExecutedObservations } from "../../support/components/summary-of-executed-observations";
import { ProposalPage } from "../../support/pages/proposal-page";
import {
  forceAuthenticationError,
  forceForbiddenError,
  forceNetworkError,
  forceServerError,
  login,
} from "../../support/utils";

const USERNAME = "hettlage";

describe("Block summaries", () => {
  const PROPOSAL_CODE = "2021-2-LSP-001";

  beforeEach(() => {
    // Give I am logged in
    login(USERNAME);

    // And I visit a proposal page
    ProposalPage.visit(PROPOSAL_CODE);
  });

  it("should load the correct block content when a block name link is clicked", () => {
    SummaryOfExecutedObservations.clickBlockNameLink(8);
    SummaryOfExecutedObservations.correctBlockLoaded(8);
  });
});
