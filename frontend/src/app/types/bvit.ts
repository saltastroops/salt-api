import { InstrumentSummary } from './common';

export interface Bvit {
  id: number;
  mode: BvitMode;
  filter: BvitFilter;
  neutralDensity: BvitNeutralDensity;
  irisSize: number;
  shutterOpenTime: number;
}

export type BvitFilter = 'B' | 'H-alpha' | 'Open' | 'R' | 'U' | 'V';

export type BvitMode = 'Imaging' | 'Streaming';

export type BvitNeutralDensity =
  | '0.3'
  | '0.5'
  | '1.0'
  | '2.0'
  | '3.0'
  | '4.0'
  | 'Open';

export interface BvitSummary extends InstrumentSummary {
  name: 'BVIT';
  modes: Array<''>;
}
