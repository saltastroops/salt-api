import { Observable } from 'rxjs';

export interface SaltAstronomer {
  given_name: string;
  family_name: string;
  email: string;
}

export interface LoadingStreams<T> {
  content$: Observable<T>;
  error$: Observable<string | null>;
  isLoading$: Observable<boolean>;
}

export interface Partner {
  name: string;
  code: string;
  institute: string;
  department: string;
}

export interface Investigator {
  id: number;
  name: string;
  partner: Partner;
  is_pc: boolean;
  is_pi: boolean;
}

export interface GeneralProposalInfo {
  id: number;
  code: string;
  title: string;
  abstract: string;
  current_submission: Date;
  first_submission: Date;
  submission_number: number;
  phase: number;
  semesters: Semester[]; // TODO semester need to be handled correctly
  current_semester: Semester;
  status: ProposalStatus;
  type: string;
  target_of_opportunity: boolean;
  total_requested_time: number;
  proprietary_period: number;
  responsible_salt_astronomer: SaltAstronomer;
  summary_for_salt_astronomer: string;
  summary_for_night_log: string;
}

export interface BlockSummary {
  // TODO rename all as follows the rename
  id: number;
  name: string;
  obs_time: number;
  priority: number;
  requested_block_visits: number;
  done_visits: number;
  observable_tonight: boolean;
  remaining_nights: number;
  maximum_seeing: number;
  transparency: string;
  maximum_lunar_phase: number;
  instruments: Array<{ name: string; config_mode: string }>;
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
  partner: Partner;
  priority_0: number;
  priority_1: number;
  priority_2: number;
  priority_3: number;
  priority_4: number;
  tac_comment: string | null;
}

export interface Proposal {
  investigators: Investigator[];
  general_info: GeneralProposalInfo;
  blocks: BlockSummary[];
  executed_observations: ExecutedObservation[];
  time_allocations: TimeAllocation[];
  charged_time: ChargedTime;
  comments: ProposalComment[];
  proposalAcceptance: ProposalAcceptance[];
  progress: string | null;
}

export interface ChargedTime {
  priority_0: number;
  priority_1: number;
  priority_2: number;
  priority_3: number;
  priority_4: number;
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
  observation_id: number;
  block_identifier: BlockIdentifier;
  observation_time: number;
  priority: number;
  maximum_lunar_phase: number;
  targets: string[];
  observation_date: Date;
  accepted: boolean;
  rejection_reason: string | null;
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
