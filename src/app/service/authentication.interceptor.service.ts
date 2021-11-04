import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
  HttpErrorResponse,
} from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { AuthenticationService } from './authentication.service';
import { GENERIC_ERROR_MESSAGE } from '../utils';

@Injectable()
export class AuthenticationInterceptor implements HttpInterceptor {
  constructor(private authenticationService: AuthenticationService) {}

  /**
   * Intercept all HTTP requests and responses, unless the request URL ends with
   * "/token".
   *
   * Regarding requests, the access token as an Authorization header.
   *
   * Regarding responses, if the response has the status code 401 (Unauthorized), the
   * user is logged out, as the access token evidently is invalid.
   */
  intercept(
    request: HttpRequest<any>,
    next: HttpHandler
  ): Observable<HttpEvent<any>> {
    if (
      request.url.split('/').slice(-1)[0] === 'token' ||
      request.url.split('/').slice(-1)[0] === 'send-password-reset-email'
    ) {
      return next.handle(request);
    }
    const token = this.authenticationService.getAccessToken();
    if (token) {
      request = request.clone({
        setHeaders: {
          'Content-Type': 'application/json; charset=utf-8',
          Accept: 'application/json',
          Authorization: `Bearer ${token}`,
        },
      });
    }
    return next.handle(request).pipe(
      catchError((err: HttpErrorResponse) => {
        let message = GENERIC_ERROR_MESSAGE;
        if (err.status === 401) {
          message = 'You are not logged in.';
          this.authenticationService.logout();
        } else if (err.status === 500) {
          message = GENERIC_ERROR_MESSAGE;
        } else if (err.error && err.error.detail) {
          message = err.error.detail;
        } else if (err.error && err.error.message) {
          message = err.error.message;
        }
        return throwError(message);
      })
    );
  }
}
