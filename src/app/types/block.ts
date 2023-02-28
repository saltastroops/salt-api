import {
  BaseBlockVisit,
  InstrumentSummary,
  ObservationProbabilities,
  Ranking,
  TimeInterval,
} from "./common";
import { Observation } from "./observation";

export interface Block {
  id: number;
  code: string | null;
  name: string;
  proposalCode: string;
  semester: string;
  status: BlockStatus;
  priority: 0 | 1 | 2 | 3 | 4;
  ranking: Ranking | null;
  comment: string;
  waitPeriod: number;
  requestedObservations: number;
  blockVisits: BaseBlockVisit[];
  observingConditions: ObservingConditions;
  observationTime: number;
  overheadTime: number;
  observingWindows: TimeInterval[];
  observationProbabilities: ObservationProbabilities;
  observations: Observation[];
  latestSubmissionDate: string;
}

export type BlockStatusValue =
  | "Active"
  | "Completed"
  | "Deleted"
  | "Expired"
  | "Not set"
  | "On hold"
  | "Superseded";

export interface BlockStatus {
  value: BlockStatusValue;
  reason: string | null;
}

export interface BlockSummary {
  id: number;
  semester: string;
  name: string;
  status: BlockStatus;
  observationTime: number;
  priority: 0 | 1 | 2 | 3 | 4;
  requestedObservations: number;
  acceptedObservations: number;
  isObservableTonight: boolean;
  remainingNights: number;
  observingConditions: ObservingConditions;
  instruments: InstrumentSummary[];
}

export interface ObservingConditions {
  minimumSeeing: number;
  maximumSeeing: number;
  transparency: Transparency;
  maximumLunarPhase: number;
  minimumLunarDistance: number;
}

export type Transparency = "Any" | "Clear" | "Thick cloud" | "Thin cloud";

export type BlockRejectionReason =
  | "Instrument technical problems"
  | "Observing conditions not met"
  | "Phase 2 problems"
  | "Telescope technical problems"
  | "Other";
