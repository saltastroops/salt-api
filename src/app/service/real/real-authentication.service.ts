import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { map } from 'rxjs/operators';
import { AccessToken } from '../../types/authentication';
import * as camelcaseKeys from 'camelcase-keys';
import { AuthenticationService, Redirection } from '../authentication.service';
import { parseISO } from 'date-fns';
import { storeAccessToken } from '../../utils';
import { Message } from '../../types/common';

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
    return this.http
      .post<any>(uri, body, { headers })
      .pipe(
        map((accessToken: any) => camelcaseKeys(accessToken, { deep: true }))
      );
  }

  logout(): void {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('expiresAt');
  }

  isAuthenticated(): boolean {
    const accessToken = localStorage.getItem('accessToken');
    if (!accessToken) {
      return false;
    }
    return this.isTokenValid();
  }

  setAccessToken(tokenData: AccessToken): void {
    storeAccessToken(tokenData);
  }

  getAccessToken(): string | null {
    return localStorage.getItem('accessToken');
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
      Authorization: 'Bearer x',
      'Content-type': 'application/json',
    });

    return this.http
      .post<any>(uri, { username_email: usernameEmail }, { headers })
      .pipe(map((message: any) => camelcaseKeys(message, { deep: true })));
  }

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


