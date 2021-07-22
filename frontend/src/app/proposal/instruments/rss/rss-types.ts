import {Instrument} from '../../../types';

export type ReadoutSpeed = 'Slow' | 'None' | 'Fast';
export type Gain = 'Faint' | 'Bright';
export type Mode = 'Drift Scan' | 'Frame Transfer' | 'Normal' | 'Shuffle' | 'Slot Mode';
export type ExposureType= 'Arc' | 'Bias' | 'Dark' | 'Flat Field' | 'Science';
export type ConfigurationType = 'Science' | 'Calibration' | 'Acquisition';
export type GuideMethod= 'HRS Probe' | 'Manual' | 'None' | 'QUACK' | 'RSS Probe' | 'SALTICAM' | 'SALTICAM Probe' |
  'Slitviewer';

export interface Detector {
  iterations: number;
  readoutSpeed: ReadoutSpeed;
  gain: Gain;
  mode: Mode;
  binning: string;
  exposureType: ExposureType;
  exposureTime: number;
  windowHeight: number | null;
}

export interface ArcBibleEntry {
  lamp: string;
  baseExposureTime: number;
  correctedExposureTime: number;
}

export interface CalibrationSetup {
  lamp: string;
  filterSetup: string | null;
}

export interface Spectroscopy {
  filter: string;
  grating: string;
  gratingAngle: number;
  cameraStation: number;
  cameraAngle: number;
}

export interface RSSConfiguration {
  id: number;
  instrument: Instrument;
  configurationType: ConfigurationType;
  guideMethod: GuideMethod | null;
  configuration: InstrumentConfiguration;
  usedIn: any;
}

export interface SlitMask {
  maskType: string;
  description: string;
  barcode: string;
}

export interface InstrumentConfiguration {
  minSN: number;
  cycles: number;
  totalExposureTime: number;
  overhead: number;
  chargedTime: number;
  guideMethod: GuideMethod | null;
  spectroscopy: Spectroscopy | null | undefined;
  slitMask: SlitMask | null | undefined;
  detector: Detector;
  calibrations: CalibrationSetup[] | null | undefined;
  arcBibleEntries: ArcBibleEntry[] | null | undefined;
}
