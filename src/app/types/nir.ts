export interface Nir {
  id: number;
  configuration: NirConfiguration;
  detector: NirDetector;
  procedure: NirProcedure;
  observationTime: number;
  overheadTime: number;
}

export interface NirConfiguration {
  mode: NirSamplingMode;
  spectroscopy: NirSpectroscopy | null;
  filter: string;
}


export interface NirDetector {
  mode: NirSamplingMode;
  resets: number;
  ramps: number;
  urgGroups: number;
  readsPerSample: number;
  exposureTime: number;
  iterations: number;
  exposureType: string;
  gain: number;
}


export interface NirSpectroscopy {
  grating: string;
  gratingAngle: number;
  cameraStation: number;
  cameraAngle: number;
}

export interface NirProcedure {
  cycles: number;
  procedureType: NirProcedureType;
}

export type NirSamplingMode = "Normal" | "Focus";

export type NirProcedureType = "Fowler" | "Up-the-Ramp Group";
