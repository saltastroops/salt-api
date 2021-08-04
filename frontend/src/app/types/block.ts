import { SalticamSummary } from './salticam';
import { RssSummary } from './rss';
import { HrsSummary } from './hrs';
import { BvitSummary } from './bvit';
import {
  BaseExecutedObservation,
  InstrumentSummary,
  ObservationProbabilities,
  Ranking,
  TimeInterval,
} from './common';
import { Observation } from './observation';

export interface Block {
  id: number;
  name: string;
  proposalCode: string;
  semester: string;
  status: BlockStatus;
  priority: 0 | 1 | 2 | 3 | 4;
  ranking: Ranking | null;
  comment: string;
  waitPeriod: number;
  requestedObservations: number;
  executedObservations: BaseExecutedObservation[];
  observingConditions: ObservingConditions;
  observationTime: number;
  overheadTime: number;
  observingWindows: TimeInterval[];
  observationProbabilities: ObservationProbabilities;
  observations: Observation[];
}

export type BlockStatus =
  | 'Active'
  | 'Completed'
  | 'Deleted'
  | 'Expired'
  | 'Not set'
  | 'On Hold'
  | 'Superseded';

export interface BlockSummary {
  id: number;
  name: string;
  observationTime: number;
  priority: number;
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
  transparency: string;
  maximumLunarPhase: number;
  minimumLunarDistance: number;
}

export type Transparency = 'Any' | 'Clear' | 'Thick cloud' | 'Thin cloud';
