import { Params } from '@angular/router';
import { Observable } from 'rxjs';
import { AccessToken } from '../types/authentication';
import { Message } from '../types/common';
import { User } from '../types/user';

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

  /**
   * Update the user.
   *
   * If no user is logged in, the current user is set to null; otherwise the
   * user is loaded by calling the /user API endpoint.
   */
  public abstract updateUser(): void;

  /**
   * An observable emitting the currently logged in user (or null if no user is logged
   * in).
   *
   * The current user (or null) is immediately returned when you subscribe to the
   * stream. The same stream is returned for every instance of the service.
   *
   * Use the updateUser method to update the user.
   */
  public abstract user(): Observable<User | null>;

  public abstract getRedirection(): Redirection | null;

  public abstract setRedirection(redirection: Redirection | null): void;

  public abstract sendResetPassword(usernameEmail: string): Observable<Message>;

  public abstract changePassword(
    password: string,
    token: string
  ): Observable<Message>;

  public abstract getUser(): Observable<User>;
}
