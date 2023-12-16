export interface Nir {
  id: number;
  configuration: NirConfiguration;
  procedure: NirProcedure;
  observationTime: number;
  overheadTime: number;
}

export interface NirConfiguration {
  grating: string;
  gratingAngle: number;
  cameraStation: number;
  cameraAngle: number;
  cameraFilterWheel: NirCameraFilterWheel;
  filter: string;
}

export interface NirDetector {
  mode: NirSamplingMode;
  ramps: number;
  groups: number;
  readsPerSample: number;
  exposureTime: number;
  iterations: number;
  gain: NirGain;
}

export interface NirProcedure {
  cycles: number;
  procedureType: NirProcedureType;
  ditherPattern: NirDitherStep[];
}

export interface NirDitherStep {
  offset: NirDitherOffset;
  offsetType: NirOffsetType;
  detector: NirDetector;
  exposureType: NirExposureType;
}

export interface NirDitherOffset {
  x: number;
  y: number;
}

export type NirGain = "Bright" | "Faint";

export type NirCameraFilterWheel =
  | "Block"
  | "Clear"
  | "Cutoff 1.5um"
  | "Cutoff 1.7um"
  | "Diffuser";

export type NirOffsetType =
  | "FIF Offset"
  | "Bundle Separation Offset"
  | "Tracker Guided Offset"
  | "Unguided Offset";

export type NirExposureType =
  | "Arc"
  | "Bias"
  | "Dark"
  | "Flat Field"
  | "Science"
  | "Sky";

export type NirSamplingMode = "Normal" | "Focus";

export type NirProcedureType = "Fowler" | "Up-the-Ramp Group";
