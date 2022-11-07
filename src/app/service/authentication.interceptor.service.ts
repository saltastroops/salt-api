import {
  HttpErrorResponse,
  HttpEvent,
  HttpHandler,
  HttpInterceptor,
  HttpRequest,
} from "@angular/common/http";
import { Injectable } from "@angular/core";

import { Observable, throwError } from "rxjs";
import { catchError } from "rxjs/operators";

import {
  FORBIDDEN_MESSAGE,
  GENERIC_ERROR_MESSAGE,
  NOT_LOGGED_IN_MESSAGE,
} from "../utils";
import { AuthenticationService } from "./authentication.service";

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
    request: HttpRequest<unknown>,
    next: HttpHandler,
  ): Observable<HttpEvent<unknown>> {
    if (
      request.url.split("/").slice(-1)[0] === "token" ||
      request.url.split("/").slice(-1)[0] === "send-password-reset-email"
    ) {
      return next.handle(request);
    }
    return next.handle(request).pipe(
      catchError((err: HttpErrorResponse) => {
        if (err.status === 401) {
          this.authenticationService.logout().subscribe(() => {
            /* do nothing */
          });
        }
        return httpErrorObservable(err);
      }),
    );
  }
}

function httpErrorObservable(err: HttpErrorResponse): Observable<never> {
  let message = GENERIC_ERROR_MESSAGE;
  if (err.status === 401) {
    message = NOT_LOGGED_IN_MESSAGE;
  } else if (err.status === 403) {
    message = FORBIDDEN_MESSAGE;
  } else if (err.status === 500) {
    message = GENERIC_ERROR_MESSAGE;
  } else if (err.error && err.error.detail) {
    message = err.error.detail;
  } else if (err.error && err.error.message) {
    message = err.error.message;
  } else if (err.error && typeof err.error === "string") {
    message = err.error;
  }
  return throwError(message);
}
