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
  roles: UserRole[];
}
