import { Params } from '@angular/router';
import { Observable } from 'rxjs';
import { AccessToken } from '../types/authentication';

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

  public abstract getAccessToken(): string | null;

  public abstract getRedirection(): Redirection | null;

  public abstract setRedirection(redirection: Redirection | null): void;
}