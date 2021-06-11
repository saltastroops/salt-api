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
  name: string;
  partner: Partner;
  is_pc: boolean;
  is_pi: boolean;
  accept: boolean;
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

export interface Proposal {
  investigators: Investigator[];
  general_info: GeneralProposalInfo;
  blocks: BlockSummary[];
  executed_observations: ExecutedObservation[];
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
