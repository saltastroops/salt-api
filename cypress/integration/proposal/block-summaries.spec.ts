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

  it('should have the table sorted by IDs when block ID column is clicked', () => {
    BlockSummaries.clickBlockIdColumn();
    BlockSummaries.blocksSortedBy('id', 'ascending');
    BlockSummaries.clickBlockIdColumn();
    BlockSummaries.blocksSortedBy('id', 'descending');
  });

  it('should have the table sorted by names when block name column is clicked', () => {
    BlockSummaries.clickBlockNameColumn();
    BlockSummaries.blocksSortedBy('name', 'ascending');
    BlockSummaries.clickBlockNameColumn();
    BlockSummaries.blocksSortedBy('name', 'descending');
  });

  it('should have the table sorted by observation time when observation time column is clicked', () => {
    BlockSummaries.clickBlockObservationTimeColumn();
    BlockSummaries.blocksSortedBy('observation-time', 'ascending');
    BlockSummaries.clickBlockObservationTimeColumn();
    BlockSummaries.blocksSortedBy('observation-time', 'descending');
  });

  it('should have the table sorted by priority when priority column is clicked', () => {
    BlockSummaries.clickBlockPriorityColumn();
    BlockSummaries.blocksSortedBy('priority', 'ascending');
    BlockSummaries.clickBlockPriorityColumn();
    BlockSummaries.blocksSortedBy('priority', 'descending');
  });

  it('should have the table sorted by maximum seeing when maximum seeing column is clicked', () => {
    BlockSummaries.clickBlockMaximumSeeingColumn();
    BlockSummaries.blocksSortedBy('maximum-seeing', 'ascending');
    BlockSummaries.clickBlockMaximumSeeingColumn();
    BlockSummaries.blocksSortedBy('maximum-seeing', 'descending');
  });

  it('should have the table sorted by remaining nights when remaining nights column is clicked', () => {
    BlockSummaries.clickBlockRemainingNightsColumn();
    BlockSummaries.blocksSortedBy('remaining-nights', 'ascending');
    BlockSummaries.clickBlockRemainingNightsColumn();
    BlockSummaries.blocksSortedBy('remaining-nights', 'descending');
  });

  it('should have the table sorted by maximum lunar phase when maximum lunar phase column is clicked', () => {
    BlockSummaries.clickBlockMaximumLunarPhaseColumn();
    BlockSummaries.blocksSortedBy('maximum-lunar-phase', 'ascending');
    BlockSummaries.clickBlockMaximumLunarPhaseColumn();
    BlockSummaries.blocksSortedBy('maximum-lunar-phase', 'descending');
  });

  it('should have the table sorted in ascending by maximum lunar phase when the block name column is clicked bofore clicking the maximum lunar phase column', () => {
    BlockSummaries.clickBlockNameColumn();
    BlockSummaries.blocksSortedBy('name', 'ascending');
    BlockSummaries.clickBlockNameColumn();
    BlockSummaries.blocksSortedBy('name', 'descending');
    BlockSummaries.clickBlockMaximumLunarPhaseColumn();
    BlockSummaries.blocksSortedBy('maximum-lunar-phase', 'ascending');
  });
});
