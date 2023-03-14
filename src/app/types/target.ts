import { ObservationProbabilities, Ranking, TargetCoordinates } from "./common";

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
  observingTime: number;
  isOptional: boolean;
  requestedObservations: number;
  maxLunarPhase: number;
  ranking: Ranking;
  nightCount: number;
  observingProbabilities: ObservationProbabilities;
  trackCount: number;
}

export interface ProperMotion {
  rightAscensionSpeed: number;
  declinationSpeed: number;
  epoch: string;
}

export interface TargetType {
  type: string;
  subType: string;
}

export interface Target {
  id: number;
  name: string;
  coordinates: TargetCoordinates | null;
  properMotion: ProperMotion | null;
  magnitude: Magnitude | null;
  targetType: TargetType | null;
  periodEphemeris: PeriodEphemeris | null;
  horizonsIdentifier: string | null;
  nonSidereal: boolean;
}

export type TimeBase =
  | "BJD" // Barycentric Julian Date
  | "HJD" // Heliocentric Julian Date
  | "JD" // Julian Date
  | "UT"; // Universal Time
