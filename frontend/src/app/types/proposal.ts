import { ExecutedObservation, PartnerCode, PartnerName } from './common';
import { Phase1Target } from './target';
import { Block, BlockSummary } from './block';

export interface Affiliation {
  partnerName: PartnerName;
  partnerCode: PartnerCode;
  institute: string;
  department: string;
}

interface BaseProposal {
  proposalCode: string;
  semester: string;
  generalInfo: GeneralProposalInfo;
  investigators: Investigator[];
}

export interface ChargedTime {
  priority0: number;
  priority1: number;
  priority2: number;
  priority3: number;
  priority4: number;
}

export interface ContactDetails {
  givenName: string;
  familyName: string;
  email: string;
}

export interface GeneralProposalInfo {
  title: string;
  abstract: string;
  currentSubmission: string;
  firstSubmission: string;
  submissionNumber: number;
  semesters: string[]; // TODO semester need to be handled correctly
  status: ProposalStatus; // TODO you should remove a ProposalStatus and add display it correctly on General.
  proposalType: string;
  targetOfOpportunity: boolean;
  totalRequestedTime: number;
  dataReleaseDate: string;
  liaisonSaltAstronomer: string;
  summaryForSaltAstronomer: string;
  summaryForNightLog: string;
  observationComments: ObservationComment[];
}

export interface Investigator {
  userId: number;
  givenName: string;
  familyName: string;
  email: string;
  affiliation: Affiliation;
  isPc: boolean;
  isPi: boolean;
  hasApprovedProposal: boolean;
}

export interface ObservationComment {
  author: string;
  comment: string;
  madeAt: string;
}

export interface Phase1Proposal extends BaseProposal {
  phase: 1;
  targets: Phase1Target[];
  requestedTimes: RequestedTime[];
}

export interface Phase2Proposal extends BaseProposal {
  phase: 2;
  blocks: BlockSummary[];
  executedObservations: ExecutedObservation[];
  chargedTime: ChargedTime;
  timeAllocations: TimeAllocation[];
}

export type Proposal = Phase1Proposal | Phase2Proposal;

export interface ProposalListItem {
  id: number;
  proposalCode: string;
  semester: string;
  title: string;
  phase: 1 | 2;
  status: ProposalStatus;
  proposalType: ProposalType;
  principalInvestigator: ContactDetails;
  principalContact: ContactDetails;
  liaisonAstronomer: ContactDetails;
}

export type ProposalStatus =
  | 'Accepted'
  | 'Active'
  | 'Completed'
  | 'Deleted'
  | 'Expired'
  | 'In preparation'
  | 'Inactive'
  | 'Rejected'
  | 'Superseded'
  | 'Under scientific review'
  | 'Under technical review';

export type ProposalType =
  | 'Commissioning'
  | 'Director’s Discretionary Time'
  | 'Engineering'
  | 'Gravitational Wave Event'
  | 'Key Science Program'
  | 'Large Science Proposal'
  | 'Science'
  | 'Science - Long Term'
  | 'Science Verification';

export interface RequestedTime {
  totalRequestedTime: number;
  minimumUsefulTime: number | null;
  comment: string | null;
  semester: string;
  distribution: Array<{ partner: PartnerName; percentage: number }>;
}

export interface TimeAllocation {
  partnerName: PartnerName;
  partnerCode: PartnerCode;
  tacComment: string | null;
  priority0: number;
  priority1: number;
  priority2: number;
  priority3: number;
  priority4: number;
}
