import { ProposalPage } from '../../support/pages/proposal-page';
import { BlockSummaries } from '../../support/components/block-summaries';
import {
  forceAuthenticationError,
  forceForbiddenError,
  forceNetworkError,
  forceServerError,
  login,
} from '../../support/utils';

const USERNAME = 'hettlage';

describe('Block summaries', () => {
  const PROPOSAL_CODE = '2021-2-LSP-001';

  beforeEach(() => {
    // Give I am logged in
    login(USERNAME);

    // And I visit a proposal page
    ProposalPage.visit(PROPOSAL_CODE);
  });

  it('should have checkboxes deselected initially', () => {
    BlockSummaries.filterCompletedChecked(false);
    BlockSummaries.filterUnobservableChecked(false);
  });

  it('should filter completed blocks when filter-completed checkbox is clicked', () => {
    BlockSummaries.hasCompletedBlocks(true);
    BlockSummaries.clickFilterCompleted();
    BlockSummaries.filterCompletedChecked(true);
    BlockSummaries.filterUnobservableChecked(false);
    BlockSummaries.hasCompletedBlocks(false);
  });

  it('should filter unobservable blocks when filter-unobservable checkbox is clicked', () => {
    BlockSummaries.hasUnobservableBlocks(true);
    BlockSummaries.clickFilterUnobservable();
    BlockSummaries.filterUnobservableChecked(true);
    BlockSummaries.filterCompletedChecked(false);
    BlockSummaries.hasUnobservableBlocks(false);
  });

  it('should filter unobservable and completed blocks when checkboxes are clicked', () => {
    BlockSummaries.hasCompletedBlocks(true);
    BlockSummaries.hasUnobservableBlocks(true);
    BlockSummaries.clickFilterCompleted();
    BlockSummaries.clickFilterUnobservable();
    BlockSummaries.filterCompletedChecked(true);
    BlockSummaries.filterUnobservableChecked(true);
    BlockSummaries.hasCompletedBlocks(false);
    BlockSummaries.hasUnobservableBlocks(false);
  });

  it('should have the checkboxes still checked and content filtered when the checkboxes are clicked the page is reloaded', () => {
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
});
