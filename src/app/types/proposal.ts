import { BlockVisit, PartnerCode, PartnerName } from './common';
import { Phase1Target } from './target';
import { Block, BlockSummary } from './block';

export interface Affiliation {
  partnerName: PartnerName;
  partnerCode: PartnerCode;
  institute: string;
  department: string;
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
  liaisonSaltAstronomer: ContactDetails | null;
  summaryForSaltAstronomer: string;
  summaryForNightLog: string;
  isSelfActivatable: boolean;
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
  commentDate: string;
}

export interface Proposal {
  proposalCode: string;
  phase: 1;
  semester: string;
  generalInfo: GeneralProposalInfo;
  investigators: Investigator[];
  targets: Phase1Target[] | null;
  requestedTimes: RequestedTime[] | null;
  blocks: BlockSummary[];
  blockVisits: BlockVisit[];
  chargedTime: ChargedTime;
  timeAllocations: TimeAllocation[];
  observationComments: ObservationComment[];
}

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
  liaisonAstronomer: ContactDetails | null;
}

export type ProposalStatusValue =
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

export interface ProposalStatus {
  value: ProposalStatusValue;
  reason: string | null;
}

export type ProposalType =
  | 'Commissioning'
  | "Director's Discretionary Time"
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
