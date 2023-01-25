export interface Institution {
  institutionId: number;
  partnerCode: string;
  partnerName: string;
  name: string;
  department: string | null;
}

export interface NewInstitutionDetails {
  institutionName: string;
  department: string;
  address: string;
  url: string;
}
