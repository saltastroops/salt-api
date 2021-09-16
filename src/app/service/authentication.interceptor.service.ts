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
    if (request.url.split('/').slice(-1)[0] === 'token') {
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
        if (err.status === 401) {
          this.authenticationService.logout();
        }
        return throwError(err.message);
      })
    );
  }
}
