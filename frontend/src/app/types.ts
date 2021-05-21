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
}
