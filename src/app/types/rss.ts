import { InstrumentSummary, Lamp } from './common';

export interface ArcBibleEntry {
  lamp: Lamp;
  isPreferredLamp: boolean;
  originalExposureTime: number;
  preferredExposureTime: number;
}

export interface Rss {
  id: number;
  configuration: RssConfiguration;
  detector: RssDetector;
  procedure: RssProcedure;
  arcBibleEntries: ArcBibleEntry[];
  observationTime: number;
  overheadTime: number;
}

export type RssBeamSplitterOperation = 'Normal' | 'Parallel';

export interface RssConfiguration {
  mode: RssMode;
  spectroscopy: RssSpectroscopy | null;
  fabryPerot: RssFabryPerot | null;
  polarimetry: RssPolarimetry | null;
  filter: string;
  mask: RssMask | RssMosMask | null;
}

export interface RssDetector {
  mode: RssDetectorMode;
  preBinnedRows: number;
  preBinnedColumns: number;
  exposureTime: number;
  iterations: number;
  exposureType: RssExposureType;
  gain: RssGain;
  readoutSpeed: RssReadoutSpeed;
  detectorCalculation: RssDetectorCalculation;
  detectorWindow: RssDetectorWindow | null;
}

export type RssDetectorCalculation =
  | 'Focus'
  | 'FP Ring Radius'
  | 'MOS Acquisition'
  | 'MOS Mask Calibration'
  | 'MOS Scan'
  | 'Nod & Shuffle'
  | 'None';

export type RssDetectorMode =
  | 'Drift Scan'
  | 'Frame Transfer'
  | 'Normal'
  | 'Shuffle'
  | 'Slot Mode';

export interface RssDetectorWindow {
  height: number;
}

export type RssExposureType =
  | 'Arc'
  | 'Bias'
  | 'Dark'
  | 'Flat Field'
  | 'Science';

export interface RssFabryPerot {
  mode: RssFabryPerotMode;
}

export type RssFabryPerotMode =
  | 'High Resolution'
  | 'Low Resolution'
  | 'Medium Resolution'
  | 'Tunable Filter';

export type RssGain = 'Bright' | 'Faint';

export type RssGrating =
  | 'Open'
  | 'pg0300'
  | 'pg0900'
  | 'pg1300'
  | 'pg1800'
  | 'pg2300'
  | 'pg3000';

export interface RssMask {
  barcode: string;
  description: string | null;
  maskType: RssMaskType;
}

export type RssMaskType =
  | 'Engineering'
  | 'Imaging'
  | 'Longslit'
  | 'MOS'
  | 'Polarimetric';

export type RssMode =
  | 'Fabry Perot'
  | 'FP polarimetry'
  | 'Imaging'
  | 'MOS'
  | 'MOS polarimetry'
  | 'Polarimetric imaging'
  | 'Spectropolarimetry'
  | 'Spectroscopy';

export interface RssMosMask extends RssMask {
  equinox: number | null;
  cutBy: string | null;
  cutDate: string | null;
  comment: string | null;
}

export interface RssPolarimetry {
  beamSplitterOrientation: RssBeamSplitterOperation;
}

export interface RssPolarimetryPattern {
  name: string;
  wavePlateAngles: Array<{
    halfWave: number | null;
    quarterWave: number | null;
  }>;
}

export interface RssProcedure {
  procedureType: RssProcedureType;
  cycles: number;
  etalonWavelengths: number[] | null;
  polarimetryPattern: RssPolarimetryPattern | null;
}

export type RssProcedureType =
  | 'Fabry Perot'
  | 'Focus'
  | 'FP Cal'
  | 'FP Polarimetry'
  | 'FP Ring'
  | 'MOS Acquisition'
  | 'MOS Calibration'
  | 'MOS Peakup'
  | 'Node and Shuffle'
  | 'Normal'
  | 'Polarimetry';

export type RssReadoutSpeed = 'Fast' | 'None' | 'Slow';

export interface RssSpectroscopy {
  grating: RssGrating;
  gratingAngle: number;
  cameraAngle: number;
}

export interface RssSummary extends InstrumentSummary {
  name: 'RSS';
  modes: RssMode[];
  gratings: RssGrating[];
}
