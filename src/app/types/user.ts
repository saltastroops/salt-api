export type UserRole =
  | "Administrator"
  | "SALT Astronomer"
  | "SALT Operator"
  | "TAC Chair"
  | "TAC Member";

export interface User {
  username: string;
  givenName: string;
  familyName: string;
  email: string;
  roles: UserRole[];
}
