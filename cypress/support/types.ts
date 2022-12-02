export interface User {
  givenName: string;
  familyName: string;
  email: string;
}

export interface Email {
  to: string;
  body: string;
  html: string;
}
