import { BlockSummary, Transparency } from "./block";
import { BlockVisit, PartnerCode, PartnerName } from "./common";
import { Phase1Observation } from "./target";

export interface Affiliation {
  partnerName: PartnerName;
  partnerCode: PartnerCode;
  institutionId: number;
  name: string;
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

export interface ProprietaryPeriod {
  period: number;
  maximumPeriod: number;
  startDate: string;
  motivation: string | null;
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
  isTargetOfOpportunity: boolean;
  targetOfOpportunityReason: string | null;
  totalRequestedTime: number;
  proprietaryPeriod: ProprietaryPeriod;
  dataReleaseDate: string;
  liaisonSaltAstronomer: ProposalUser | null;
  summaryForSaltAstronomer: string;
  summaryForNightLog: string;
  isSelfActivatable: boolean;
  isTimeRestricted: boolean;
  isP4: boolean;
}
type ThesisType = "PhD" | "Masters";
interface ThesisInfo {
  thesisType: ThesisType;
  yearOfCompletion: number;
  relevanceOfProposal: string;
}

export interface Investigator extends ProposalUser {
  affiliation: Affiliation;
  isPc: boolean;
  isPi: boolean;
  hasApprovedProposal: boolean | null;
  thesis: ThesisInfo | null;
}

export interface ObservationComment {
  author: string;
  comment: string;
  commentDate: string;
}

export interface P1ScienceConfiguration {
  instrument: string;
  mode: string;
  simulations: {
    name: string;
    url: string;
    description: string | null;
  }[];
}

export interface Proposal {
  proposalCode: string;
  phase: 1 | 2;
  semester: string;
  generalInfo: GeneralProposalInfo;
  investigators: Investigator[];
  observations: Phase1Observation[] | null;
  requestedTimes: RequestedTime[];
  blocks: BlockSummary[];
  blockVisits: BlockVisit[];
  chargedTime: ChargedTime;
  timeAllocations: TimeAllocation[];
  observationComments: ObservationComment[];
  phase1ProposalSummary: string | null;
  proposalFile: string;
  scienceConfigurations: P1ScienceConfiguration[];
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
  isUserAnInvestigator: boolean;
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
  comment: string | null;
}

export type ProposalType =
  | "Commissioning"
  | "Director's Discretionary Time"
  | "Engineering"
  | "Gravitational Wave Event"
  | "Key Science Program"
  | "Large Science Proposal"
  | "OPTICON-Radionet Pilot"
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

export type ProgressReportsUrls = { [key: string]: { [key: string]: string } };

export interface NewProprietaryPeriod extends ProprietaryPeriod {
  status: string;
}

export interface SelfActivation {
  allowed: boolean;
}

export enum DataFormat {
  ALL = "All",
  CALIBRATION = "Calibration",
}
