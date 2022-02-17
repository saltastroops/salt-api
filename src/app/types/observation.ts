import { Bvit } from "./bvit";
import { Lamp, TargetCoordinates, TimeInterval } from "./common";
import { Hrs } from "./hrs";
import { Rss } from "./rss";
import { Salticam } from "./salticam";
import { Target } from "./target";

export type CalibrationFilter =
  | "Blue and Red"
  | "Clear and ND"
  | "Clear and UV"
  | "ND and Clear"
  | "None"
  | "Red and Clear"
  | "UV and Blue";

export interface DitherPattern {
  horizontalTiles: number;
  verticalTiles: number;
  offsetSize: number;
  steps: number;
}

export interface FinderChart {
  id: number;
  comment: string | null;
  validFrom: string | null;
  validUntil: string | null;
}

export type GuideMethod =
  | "HRS Probe"
  | "Manual"
  | "None"
  | "QUACK"
  | "RSS Probe"
  | "SALTICAM"
  | "SALTICAM Probe"
  | "Slitviewer";

export interface GuideStar extends TargetCoordinates {
  magnitude: number;
}

export interface Instruments {
  salticam: Salticam[] | null;
  rss: Rss[] | null;
  hrs: Hrs[] | null;
  bvit: Bvit[] | null;
}

export interface Observation {
  observationTime: number;
  overheadTime: number;
  finderCharts: FinderChart[];
  target: Target;
  timeRestrictions: TimeInterval[] | null;
  phaseConstraints: PhaseInterval[] | null;
  telescopeConfigurations: TelescopeConfiguration[];
}

export interface PayloadConfiguration {
  payloadConfigurationType: PayloadConfigurationType | null;
  useCalibrationScreen: boolean | null;
  lamp: Lamp | null;
  calibrationFilter: CalibrationFilter | null;
  guideMethod: GuideMethod;
  instruments: Instruments;
}

export type PayloadConfigurationType =
  | "Acquisition"
  | "Calibration"
  | "Instrument Acquisition"
  | "Science";

export interface PhaseInterval {
  start: number;
  end: number;
}

export interface TelescopeConfiguration {
  iterations: number;
  positionAngle: number | null;
  useParallacticAngle: boolean;
  ditherPattern: DitherPattern | null;
  guideStar: GuideStar | null;
  payloadConfigurations: PayloadConfiguration[];
}
