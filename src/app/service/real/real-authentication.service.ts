import { HttpClient, HttpHeaders, HttpParams } from "@angular/common/http";
import { Injectable } from "@angular/core";

import * as camelcaseKeys from "camelcase-keys";
import { parseISO } from "date-fns";
import { BehaviorSubject, Observable, Subject, of } from "rxjs";
import { map, switchMap, tap } from "rxjs/operators";

import { environment } from "../../../environments/environment";
import { AccessToken } from "../../types/authentication";
import { Message } from "../../types/common";
import { User } from "../../types/user";
import { storeAccessToken } from "../../utils";
import { AuthenticationService, Redirection } from "../authentication.service";

const user$ = new BehaviorSubject<User | null>(null);

let whoAmITrigger$: Subject<null> | null;

@Injectable({
  providedIn: "root",
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
    const uri = environment.apiUrl + "/token";
    const headers = new HttpHeaders({
      "Content-type": "application/x-www-form-urlencoded",
    });

    const body = new HttpParams()
      .set("username", username)
      .set("password", password);
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    return this.http.post<any>(uri, body, { headers }).pipe(
      map((accessToken) => camelcaseKeys(accessToken, { deep: true })),
      tap((tokenData) => {
        this.setAccessToken(tokenData);
        this.updateUser();
      }),
    );
  }

  logout(): void {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("accessTokenExpiresAt");
    sessionStorage.removeItem("user");
    this.updateUser();
  }

  isAuthenticated(): boolean {
    return this.isTokenValid();
  }

  setAccessToken(tokenData: AccessToken): void {
    storeAccessToken(tokenData);
  }

  getAccessToken(): string | null {
    return localStorage.getItem("accessToken");
  }

  _user(): Observable<User> {
    const uri = environment.apiUrl + "/user";
    return (
      this.http
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        .get<any>(uri)
        .pipe(map((user) => camelcaseKeys(user, { deep: true })))
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
          }),
        )
        .subscribe((user) => {
          if (user) {
            sessionStorage.setItem("user", JSON.stringify(user));
          } else {
            sessionStorage.removeItem("user");
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
    const expiresAt = localStorage.getItem("accessTokenExpiresAt");
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
    const uri = environment.apiUrl + "/users/send-password-reset-email";
    const headers = new HttpHeaders({
      "Content-type": "application/json",
    });

    return this.http
      .post<Message>(uri, { username_email: usernameEmail }, { headers })
      .pipe(map((message: Message) => camelcaseKeys(message, { deep: true })));
  }

  /**
   * Change user password.
   *
   * @param token Authentication token.
   * @param password Password.
   */
  changePassword(password: string, token: string): Observable<Message> {
    // Make sure that we don't use another token for changing the password
    this.logout();

    const options = {
      headers: {
        "Content-Type": "application/json; charset=utf-8",
        Accept: "application/json",
        Authorization: `Bearer ${token}`,
      },
    };
    return (
      this.http
        // get the user for the token...
        .get<User>(environment.apiUrl + "/user/", options)
        .pipe(
          // ... and update their password
          switchMap((user) => {
            return this.http.patch<Message>(
              `${environment.apiUrl}/users/${user.username}`,
              { password },
              options,
            );
          }),
        )
    );
  }

  getUser(): Observable<User> {
    const uri = environment.apiUrl + "/user";
    return this.http
      .get<User>(uri)
      .pipe(map((user) => camelcaseKeys(user, { deep: true })));
  }
}
