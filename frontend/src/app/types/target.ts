import { ObservationProbabilities, Ranking, TargetCoordinates } from './common';

export interface Magnitude {
  minimumMagnitude: number;
  maximumMagnitude: number;
  bandpass: string;
}

export interface PeriodEphemeris {
  zeroPoint: number;
  period: number;
  periodChangeRate: number;
  timeBase: TimeBase;
}

export interface Phase1Target extends Target {
  isOptional: boolean;
  requestedObservations: number;
  maxLunarPhase: number;
  ranking: Ranking;
  nightCount: number;
  observingProbabilities: ObservationProbabilities;
}

export interface ProperMotion {
  rightAscensionSpeed: number;
  declinationSpeed: number;
  epoch: string;
}

export interface Target {
  id: number;
  name: string;
  coordinates: TargetCoordinates | null;
  properMotion: ProperMotion | null;
  magnitude: Magnitude | null;
  targetType: string | null;
  periodEphemeris: PeriodEphemeris | null;
  horizonsIdentifier: string | null;
}

export type TimeBase =
  | 'BJD' // Barycentric Julian Date
  | 'HJD' // Heliocentric Julian Date
  | 'JD' // Julian Date
  | 'UT'; // Universal Time