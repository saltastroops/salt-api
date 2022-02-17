import { Injectable } from "@angular/core";
import { ActivatedRouteSnapshot, CanActivate, Router } from "@angular/router";

import { AuthenticationService } from "./authentication.service";

@Injectable()
export class AuthGuardService implements CanActivate {
  constructor(private auth: AuthenticationService, private router: Router) {}

  canActivate(route: ActivatedRouteSnapshot): boolean {
    if (!this.auth.isAuthenticated()) {
      const redirectURL = route.url.map((seg) => seg.path);
      const redirectQueryParams = route.queryParams;
      this.auth.setRedirection({
        urlParts: redirectURL,
        queryParams: redirectQueryParams,
      });
      this.router.navigate(["login"]);
      return false;
    }
    this.auth.setRedirection(null);
    return true;
  }
}
