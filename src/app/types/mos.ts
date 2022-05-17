export interface MosBlock {
  proposalId: number;
  proposalCode: string;
  proposalCodeId: number;
  piSurname: string;
  blockStatus: string;
  blockName: string;
  priority: number;
  nVisits: number;
  nDone: number;
  barcode: string;
  raCenter: number;
  cutBy: string;
  cutDate: string;
  maskComment: string;
  liaisonAstronomer: string;
  otherBarcodes: string[];
  remainingNights: number;
  // mosMask: MosMask;
}

export interface MosMaskCutDetails {
  barcode: string;
  cutBy: string;
  cutDate: string;
  maskComment: string;
}
