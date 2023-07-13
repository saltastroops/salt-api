import { Institution } from "./institution";

export type UserRole =
  | "Administrator"
  | "SALT Astronomer"
  | "SALT Operator"
  | "TAC Chair"
  | "Technician"
  | "TAC Member";

export interface User {
  id: number;
  username: string;
  givenName: string;
  familyName: string;
  email: string;
  alternativeEmails: string[];
  roles: UserRole[];
  affiliations: Institution[];
}

export interface UserListItem {
  id: number;
  familyName: string;
  givenName: string;
  username: string;
}

export interface LiaisonAstronomer {
  id: number;
  familyName: string;
  givenName: string;
  email: string;
}

export interface NewUserDetails {
  familyName: string;
  givenName: string;
  username: string;
  password: string;
  email: string;
  institutionId: number;
  legalStatus: string;
  gender: string | null;
  race: string | null;
  hasPhd: string | null;
  yearOfPhdCompletion: number | null;
}

export interface StatisticsError {
  legalStatus: string | undefined;
  gender: string | undefined;
  race: string | undefined;
  phd: string | undefined;
}
