import { Observable } from 'rxjs';
import {stringify} from "@angular/compiler/src/util";

export interface SaltAstronomer {
  givenName: string;
  familyName: string;
  email: string;
}

export interface LoadingStreams<T> {
  content$: Observable<T>;
  error$: Observable<string | null>;
  isLoading$: Observable<boolean>;
}

export interface Affiliation {
  partnerName: string;
  partnerCode: string;
  institute: string;
  department: string;
}

export interface Investigator {
  userId: number;
  familyName: string;
  email: string;
  givenName: string;
  affiliation: Affiliation;
  hasApprovedProposal: boolean;
  isPc: boolean;
  isPi: boolean;
}

export interface GeneralProposalInfo {
  id: number;
  code: string;
  title: string;
  abstract: string;
  currentSubmission: string;
  firstSubmission: string;
  submissionNumber: number;
  phase: number;
  semesters: string[]; // TODO semester need to be handled correctly
  status: ProposalStatus; // TODO you should remove a ProposalStatus and add display it correctly on General.
  proposalType: string;
  targetOfOpportunity: boolean;
  totalRequestedTime: number;
  dataReleaseDate: number;
  liaisonSaltAstronomer: SaltAstronomer;
  summaryForSaltAstronomer: string;
  summaryForNightLog: string;
}

export interface BlockSummary {
  // TODO rename all as follows the rename
  id: number;
  name: string;
  observationTime: number;
  priority: number;
  requestedObservations: number;
  acceptedObservations: number;
  isObservableTonight: boolean;
  remainingNights: number;
  instruments: Array<{ name: string; modes: Array<string> }>;
  observingConditions: {
    maximumSeeing: number;
    transparency: string;
    maximumLunarPhase: number;
  };
}

export interface Semester {
  year: number;
  semester: number;
}

interface ProposalStatus {
  status: string;
  message: string;
}

export interface TimeAllocation {
  partnerCode: string;
  partnerName: string;
  priority0: number;
  priority1: number;
  priority2: number;
  priority3: number;
  priority4: number;
  tacComment: string | null;
}

export interface Proposal {
  investigators: Investigator[];
  generalInfo: GeneralProposalInfo;
  blocks: BlockSummary[];
  semester: string;
  executedObservations: ExecutedObservation[];
  timeAllocations: TimeAllocation[];
  chargedTime: ChargedTime;
  comments: ProposalComment[];
  proposalAcceptance: ProposalAcceptance[];
  progress: string | null;
  phase: number;
  proposalCode: string;
}

export interface ChargedTime {
  priority0: number;
  priority1: number;
  priority2: number;
  priority3: number;
  priority4: number;
}

export interface BlockIdentifier {
  // the block id in the database
  id: number;
  // the block name
  name: string;
}

export interface Block {
  id: number;
  name: string;
  observingConditions: ObservingConditions;
  overheads: number;
  observationTime: number;
  priority: number;
  comment: string;
  observingWindows: ObservingWindow[];
  observationProbabilities: ObservationProbabilities;
  lastModified: Date;
  wait: number;
  visits: number;  // TODO you should consider adding a block visits
  attempted: number;
  done: number;
  shutterOpenTime: number;
}

export interface ExecutedObservation {
  blockId: number;
  blockName: string;
  observationTime: number;
  priority: number;
  maximumLunarPhase: number;
  targets: string[];
  night: string;
  accepted: boolean;
  rejectionReason: string | null;
}

export interface ProposalComment {
  author: string;
  madeAt: Date;
  comment: string;
}

export interface ProposalAcceptance {
  accepted: boolean | null;
  investigatorId: number;
}

export type Instrument = 'RSS' | 'Salticam' | 'HRS' | 'BVIT';

export interface ObservingConditions {
  transparency: string;
  minimumLunarPhase: number;
  maximumLunarPhase: number;
  minimumLunarDistance: number;
  minimumSeeing: number;
  maximumSeeing: number;
  observationTime: number;
}

export interface ObservationProbabilities {
  moon: number;
  competition: number;
  observability: number;
  seeing: number;
  averageRanking: number;
  total: number;
}

export type ObservingWindowType = 'Strict' | 'Extended' | 'Strict / Extended';

export interface ObservingWindow {
  start: Date;
  end: Date;
  type: ObservingWindowType;
}

export type ReadoutSpeed = 'Slow' | 'None' | 'Fast';
export type ExposureType= 'Arc' | 'Bias' | 'Dark' | 'Flat Field' | 'Science';
export interface ExposureTime {
  value: number
}

export interface HrsDetector {
  readoutSpeed: ReadoutSpeed;
  numberOfAmplifiers: number;
  preBinRows: number;
  preBinCols: number;
  iterations: number;
  preShuffle: number;
  postShuffle: number;
}

export type IodineCellPosition = 'IN' | 'OUT' | 'ThAr in sky (O) fiber' | 'ThAr in star (P) fiber' | 'CALIBRATION'
export type TargetLocation = 'STAR' | 'BISECT' | 'SKY'
export type HrsMode = 'LOW RESOLUTION' | 'MEDIUM RESOLUTION' | 'HIGH RESOLUTION' | 'HIGH STABILITY' | 'INT CAL FIBRE'

export interface NodAndShuffle {
  nodInterval: number|undefined;
  nodCount: number|undefined;
}

export interface HrsConfiguration {
  mode: HrsMode;
  exposureType: ExposureType;
  nodAndShuffle: NodAndShuffle;
  iodineCellPosition: IodineCellPosition;
  targetLocation: TargetLocation;
  fibreSeparation: number;
  useThArWithIodineCell: boolean;
}

export interface HrsProcedure {
  cycles: number;
  blueExposurePattern: number[];
  redExposurePattern: number[];
}

export interface Hrs {
  name: string;
  hrsConfig: HrsConfiguration;
  hrsProcedure: HrsProcedure;
  hrsBlueDetector: HrsDetector;
  hrsRedDetector: HrsDetector;

export type BvitMode = 'Imaging' | 'Streaming'
export type BvitFilter =  'Open' | 'B' | 'V' | 'R' | 'H-alpha'
export type NeutralDensityFilter = 'Open' | '0.3' | '0.5' | '1.0' | '2.0'

export interface Bvit {
  name: string;
  mode: BvitMode;
  filter: BvitFilter;
  neutralDensityFilter: NeutralDensityFilter;
  irisSize: number;
  shutterOpenTime: number;
}

export type ReadoutSpeed = 'Slow' | 'None' | 'Fast';
export type Gain = 'Faint' | 'Bright';
export type Mode = 'Drift Scan' | 'Frame Transfer' | 'Normal' | 'Shuffle' | 'Slot Mode';
export type ExposureType= 'Arc' | 'Bias' | 'Dark' | 'Flat Field' | 'Science';

export interface SalticamDetector {
  preBinRows: number;
  preBinCols: number;
  iterations: number;
  readoutSpeed: ReadoutSpeed;
  gain: Gain;
  detMode: Mode;
  exposureType: ExposureType;
}

export interface SalticamFilter {
  name: string;
  filter: string;
  exposureTime: number;
}

export interface Salticam {
  inCalibration: boolean;
  salticamDetector: SalticamDetector;
  minimumSN: number;
  cycles: number;
  name: string;
  salticamProcedure: SalticamFilter[];
  shutterOpenTime: number;
  overhead: number;
  charged: number;
}