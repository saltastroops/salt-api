export interface BaseExecutedObservation {
  id: number;
  night: string;
  accepted: boolean;
  rejectionReason: string | null;
}

export interface ExecutedObservation extends BaseExecutedObservation {
  blockId: number;
  blockName: string;
  observationTime: number;
  priority: number;
  targets: string[];
  maximumLunarPhase: number;
}

export interface InstrumentSummary {
  name: string;
  modes: string[];
}

export type Lamp =
  | 'Ar'
  | 'Ar and ThAr'
  | 'CuAr'
  | 'CuAr and Xe'
  | 'HgAr'
  | 'HgAr and Ne'
  | 'Ne'
  | 'QTH1'
  | 'QTH1 and QTH2'
  | 'QTH2'
  | 'ThAr'
  | 'Xe';

export interface ObservationProbabilities {
  moon: number;
  competition: number;
  observability: number;
  seeing: number;
  averageRanking: number;
  total: number;
}

export type PartnerCode =
  | 'AMNH'
  | 'CMU'
  | 'DC'
  | 'DUR'
  | 'GU'
  | 'HET'
  | 'IUCAA'
  | 'OTH'
  | 'POL'
  | 'RSA'
  | 'RU'
  | 'UC'
  | 'UKSC'
  | 'UNC'
  | 'UW';

export type PartnerName =
  | 'American Museum of Natural History'
  | 'Carnegie Mellon University'
  | 'Dartmouth College'
  | 'Durham University'
  | 'Georg-August-Universität Göttingen'
  | 'Hobby Eberly Telescope Board'
  | 'Inter-University Centre for Astronomy & Astrophysics'
  | 'Other'
  | 'Poland'
  | 'South Africa'
  | 'Rutgers University'
  | 'University of Canterbury'
  | 'UK SALT Consortium'
  | 'University of North Carolina - Chapel Hill'
  | 'University of Wisconsin-Madison';

export type Ranking = 'High' | 'Low' | 'Medium';

export interface TargetCoordinates {
  rightAscension: number;
  declination: number;
  equinox: number;
}

export interface TimeInterval {
  start: string;
  end: string;
}
