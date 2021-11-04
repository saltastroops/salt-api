import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { BehaviorSubject, Observable, of, Subject } from 'rxjs';
import { environment } from '../../../environments/environment';
import { map, switchMap, tap } from 'rxjs/operators';
import { AccessToken } from '../../types/authentication';
import * as camelcaseKeys from 'camelcase-keys';
import { AuthenticationService, Redirection } from '../authentication.service';
import { parseISO } from 'date-fns';
import { Message } from '../../types/common';
import { User } from '../../types/user';
import { storeAccessToken } from '../../utils';

const user$ = new BehaviorSubject<User | null>(null);

let whoAmITrigger$: Subject<null> | null;

@Injectable({
  providedIn: 'root',
})
export class RealAuthenticationService implements AuthenticationService {
  private redirection: Redirection | null = null;

  constructor(private http: HttpClient) {}

  /**
   * Get an authentication token.
   *
   * @param username Username.
   * @param password Password.
   */
  login(username: string, password: string): Observable<AccessToken> {
    const uri = environment.apiUrl + '/token';
    const headers = new HttpHeaders({
      'Content-type': 'application/x-www-form-urlencoded',
    });

    const body = new HttpParams()
      .set('username', username)
      .set('password', password);
    return this.http.post<any>(uri, body, { headers }).pipe(
      map((accessToken: any) => camelcaseKeys(accessToken, { deep: true })),
      tap((tokenData) => {
        this.setAccessToken(tokenData);
        this.updateUser();
      })
    );
  }

  logout(): void {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('accessTokenExpiresAt');
    sessionStorage.removeItem('user');
    this.updateUser();
  }

  isAuthenticated(): boolean {
    return this.isTokenValid();
  }

  setAccessToken(tokenData: AccessToken): void {
    storeAccessToken(tokenData);
  }

  getAccessToken(): string | null {
    return localStorage.getItem('accessToken');
  }

  _user(): Observable<User> {
    const uri = environment.apiUrl + '/user';
    return this.http
      .get<User>(uri)
      .pipe(
        map((accessToken: any) => camelcaseKeys(accessToken, { deep: true }))
      );
  }

  /**
   * Update the user.
   *
   * If no user is logged in, the current user is set to null; otherwise the
   * user is loaded by calling the /user API endpoint.
   */
  updateUser(): void {
    if (!whoAmITrigger$) {
      whoAmITrigger$ = new Subject<null>();
      whoAmITrigger$
        .pipe(
          switchMap(() => {
            return this.isAuthenticated() ? this._user() : of(null);
          })
        )
        .subscribe((user) => {
          if (user) {
            sessionStorage.setItem('user', JSON.stringify(user));
          } else {
            sessionStorage.removeItem('user');
          }
          user$.next(user);
        });
    }
    whoAmITrigger$.next(null);
  }

  /**
   * An observable emitting the currently logged in user (or null if no user is logged
   * in).
   *
   * The current user (or null) is immediately returned when you subscribe to the
   * stream. The same stream is returned for every instance of the service.
   *
   * Use the updateUser method to update the user.
   */
  user(): Observable<User | null> {
    // Return a read-only stream
    return user$.asObservable();
  }

  getRedirection(): Redirection | null {
    return this.redirection;
  }

  setRedirection(redirection: Redirection | null): void {
    this.redirection = redirection;
  }

  private isTokenValid(): boolean {
    const expiresAt = RealAuthenticationService.getExpiry();
    const accessToken = this.getAccessToken();
    const now = new Date();
    if (!expiresAt || !accessToken) {
      return false;
    }
    return expiresAt >= now;
  }

  private static getExpiry(): Date | null {
    const expiresAt = localStorage.getItem('expiresAt');
    if (expiresAt) {
      return parseISO(expiresAt);
    }
    return null;
  }

  /**
   * Request password reset token to be sent.
   *
   * @param usernameEmail Username or email
   */
  sendResetPassword(usernameEmail: string): Observable<Message> {
    const uri = environment.apiUrl + '/users/send-password-reset-email';
    const headers = new HttpHeaders({
      'Content-type': 'application/json',
    });

    return this.http
      .post<any>(uri, { username_email: usernameEmail }, { headers })
      .pipe(map((message: any) => camelcaseKeys(message, { deep: true })));
  }

  private isTokenValid(): boolean {
    const accessToken = this.getAccessToken();
    const expiresAt = RealAuthenticationService.getExpiry();
    const now = new Date();
    if (!accessToken || !expiresAt) {
      return false;
    }
    return expiresAt >= now;
  }

  private static getExpiry(): Date | null {
    try {
      const expiresAt = localStorage.getItem('accessTokenExpiresAt');
      if (expiresAt) {
        return parseISO(expiresAt);
      }
    } catch (Error) {
      // do nothing
    }
    return null;

  /**
   * Change user password.
   *
   * @param username Username.
   * @param password Password.
   */
  changePassword(password: string, username: string): Observable<any> {
    const uri = environment.apiUrl + '/users/update-user-details';
    return this.http.post<any>(uri, { username }, { })
      .pipe(map((user: any) => camelcaseKeys(user, { deep: true })));
  }

  getUser(): Observable<any> {
    const uri = environment.apiUrl + '/user'
    return this.http.get<any>(uri)
      .pipe(map((user: any) => camelcaseKeys(user, { deep: true })));
  }
}


