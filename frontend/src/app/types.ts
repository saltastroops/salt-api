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

export interface Proposal {
  investigators: Investigator[];
}
