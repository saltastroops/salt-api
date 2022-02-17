import { InstrumentSummary } from "./common";

export interface Hrs {
  id: number;
  configuration: HrsConfiguration;
  blueDetector: HrsBlueDetector;
  redDetector: HrsRedDetector;
  procedure: HrsProcedure;
  observationTime: number;
  overheadTime: number;
}

export interface HrsBlueDetector extends HrsDetector {
  readoutAmplifiers: 1 | 2;
}

export interface HrsConfiguration {
  mode: HrsMode;
  exposureType: HrsExposureType;
  targetLocation: HrsTargetLocation;
  fiberSeparation: number;
  iodineCellPosition: HrsIodineCellPosition;
  isThArLampOn: boolean;
  nodAndShuffle: HrsNodAndShuffle;
}

export interface HrsDetector {
  preShuffledRows: number;
  postShuffledRows: number;
  preBinnedRows: number;
  preBinnedColumns: number;
  iterations: number;
  readoutAmplifiers: number;
  readoutSpeed: HrsReadoutSpeed;
}

export type HrsExposureType =
  | "Arc"
  | "Bias"
  | "Dark"
  | "Flat Field"
  | "Science"
  | "Sky Flat";

export type HrsIodineCellPosition =
  | "Calibration"
  | "In"
  | "Out"
  | "ThAr in sky fiber"
  | "ThAr in star fiber";

export type HrsMode =
  | "High Resolution"
  | "High Stability"
  | "Int Cal Fiber"
  | "Low Resolution"
  | "Medium Resolution";

export interface HrsNodAndShuffle {
  nodInterval: number;
  nodCount: number;
}

export interface HrsProcedure {
  cycles: number;
  blueExposureTimes: Array<number | null>;
  redExposureTimes: Array<number | null>;
}

export type HrsReadoutSpeed = "Fast" | "None" | "Slow";

export interface HrsRedDetector extends HrsDetector {
  readoutAmplifiers: 1 | 4;
}

export interface HrsSummary extends InstrumentSummary {
  name: "HRS";
  modes: HrsMode[];
}

export type HrsTargetLocation =
  | "The star and sky fiber are equidistant from the optical axis"
  | "The sky fiber is placed on the optical axis"
  | "The star fiber is placed on the optical axis";
