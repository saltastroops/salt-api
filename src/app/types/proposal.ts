import { BlockSummary, Transparency } from "./block";
import { BlockVisit, PartnerCode, PartnerName } from "./common";
import { Phase1Target } from "./target";

export interface Affiliation {
  partnerName: PartnerName;
  partnerCode: PartnerCode;
  institution: string;
  department: string;
}

export interface ChargedTime {
  priority0: number;
  priority1: number;
  priority2: number;
  priority3: number;
  priority4: number;
}

export interface ProposalUser extends ContactDetails {
  id: number;
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
  liaisonSaltAstronomer: ProposalUser | null;
  summaryForSaltAstronomer: string;
  summaryForNightLog: string;
  isSelfActivatable: boolean;
}

export interface Investigator extends ProposalUser {
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
  principalInvestigator: ProposalUser;
  principalContact: ProposalUser;
  liaisonAstronomer: ProposalUser | null;
}

export type ProposalStatusValue =
  | "Accepted"
  | "Active"
  | "Completed"
  | "Deleted"
  | "Expired"
  | "In preparation"
  | "Inactive"
  | "Rejected"
  | "Superseded"
  | "Under scientific review"
  | "Under technical review";

export interface ProposalStatus {
  value: ProposalStatusValue;
  reason: string | null;
}

export type ProposalType =
  | "Commissioning"
  | "Director's Discretionary Time"
  | "Engineering"
  | "Gravitational Wave Event"
  | "Key Science Program"
  | "Large Science Proposal"
  | "Science"
  | "Science - Long Term"
  | "Science Verification";

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

export interface ProposalProgress {
  requestedTime: number | null;
  semester: string | null;
  partnerRequestedPercentages: {
    partnerCode: string;
    partnerName: string;
    requestedPercentage: number;
  }[];
  maximumSeeing: number | null;
  transparency: Transparency | null;
  lastObservingConstraints: {
    seeing: number;
    transparency: string;
    description: string;
  };
  descriptionOfObservingConstraints: string;
  changeReason: string | null;
  summaryOfProposalStatus: string | null;
  strategyChanges: string | null;
  previousTimeRequests: TimeStatistics[];
}

export interface TimeStatistics {
  semester: string;
  requestedTime: number;
  allocatedTime: number;
  observedTime: number;
}
