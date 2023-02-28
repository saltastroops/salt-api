import { BlockRejectionReason } from "./block";

export type BlockVisitStatus = "Accepted" | "In queue" | "Rejected";

export interface BaseBlockVisit {
  id: number;
  night: string;
  status: BlockVisitStatus;
  rejectionReason: BlockRejectionReason | null;
}

export interface BlockVisit extends BaseBlockVisit {
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
  gratings: string[] | null;
  filters: string[] | null;
}

export type Lamp =
  | "Ar"
  | "Ar and ThAr"
  | "CuAr"
  | "CuAr and Xe"
  | "HgAr"
  | "HgAr and Ne"
  | "Ne"
  | "QTH1"
  | "QTH1 and QTH2"
  | "QTH2"
  | "ThAr"
  | "Xe";

export interface ObservationProbabilities {
  moon: number;
  competition: number;
  observability: number;
  seeing: number;
  averageRanking: number;
  total: number;
}

export type PartnerName =
  | "American Museum of Natural History"
  | "Carnegie Mellon University"
  | "Dartmouth College"
  | "Durham University"
  | "Georg-August-Universität Göttingen"
  | "Hobby Eberly Telescope Board"
  | "Inter-University Centre for Astronomy & Astrophysics"
  | "Other"
  | "Poland"
  | "South Africa"
  | "Rutgers University"
  | "University of Canterbury"
  | "UK SALT Consortium"
  | "University of North Carolina - Chapel Hill"
  | "University of Wisconsin-Madison";

export type Ranking = "High" | "Low" | "Medium";

export interface TargetCoordinates {
  rightAscension: number;
  declination: number;
  equinox: number;
}

export interface TimeInterval {
  start: string;
  end: string;
}

export interface Message {
  message: string;
}

export enum Partner {
  AMNH = "American Museum of Natural History",
  CMU = "Carnegie Mellon University",
  DC = "Dartmouth College",
  DUR = "Durham University",
  GU = "Georg-August-Universität Göttingen",
  HET = "Hobby Eberly Telescope Board",
  IUCAA = "Inter-University Centre for Astronomy & Astrophysics",
  OTH = "Other",
  POL = "Poland",
  RSA = "South Africa",
  RU = "Rutgers University",
  UC = "University of Canterbury",
  UKSC = "UK SALT Consortium",
  UNC = "University of North Carolina - Chapel Hill",
  UW = "University of Wisconsin-Madison",
}

export type PartnerCode = keyof typeof Partner;
