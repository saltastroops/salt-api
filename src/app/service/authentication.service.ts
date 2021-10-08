import { Params } from '@angular/router';
import { Observable } from 'rxjs';
import { AccessToken } from '../types/authentication';
import { Message } from '../types/common';

export interface Redirection {
  urlParts: string[];
  queryParams: Params;
}

export abstract class AuthenticationService {
  public abstract login(
    username: string,
    password: string
  ): Observable<AccessToken>;

  public abstract logout(): void;

  public abstract isAuthenticated(): boolean;

  public abstract setAccessToken(tokenData: AccessToken): void;

  public abstract getAccessToken(): string | null;

  public abstract getRedirection(): Redirection | null;

  public abstract setRedirection(redirection: Redirection | null): void;

  public abstract sendResetPassword(usernameEmail: string): Observable<Message>;
}
