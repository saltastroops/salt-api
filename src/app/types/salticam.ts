import { InstrumentSummary } from "./common";

export interface Salticam {
  id: number;
  detector: SalticamDetector;
  procedure: SalticamProcedure;
  minimumSignalToNoise: number;
  observationTime: number;
  overheadTime: number;
}

export interface SalticamDetector {
  mode: SalticamDetectorMode;
  preBinnedRows: number;
  preBinnedColumns: number;
  iterations: number;
  exposureType: SalticamExposureType;
  gain: SalticamGain;
  readoutSpeed: SalticamReadoutSpeed;
  detectorWindows: SalticamDetectorWindow[] | null;
}

export type SalticamDetectorMode =
  | "Drift Scan"
  | "Frame Transfer"
  | "Normal"
  | "Slot Mode";

export interface SalticamDetectorWindow {
  centerRightAscension: number;
  centerDeclination: number;
  height: number;
  width: number;
}

export interface SalticamExposure {
  filter: SalticamFilter;
  exposureTime: number;
}

export type SalticamExposureType = "Bias" | "Flat Field" | "Science";

export interface SalticamFilter {
  name: string;
  description: string;
  isInMagazine: boolean;
}

export type SalticamGain = "Bright" | "Faint";

export interface SalticamProcedure {
  cycles: number;
  exposures: SalticamExposure[];
}

export type SalticamReadoutSpeed = "Fast" | "None" | "Slow";

export interface SalticamSummary extends InstrumentSummary {
  name: "Salticam";
  modes: Array<"">;
}
