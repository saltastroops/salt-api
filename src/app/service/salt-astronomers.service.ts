import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";

import * as camelcaseKeys from "camelcase-keys";
import { Observable } from "rxjs";
import { map } from "rxjs/operators";

import { environment } from "../../environments/environment";
import { UserListItem } from "../types/user";

@Injectable({
  providedIn: "root",
})
export class SaltAstronomersService {
  constructor(private http: HttpClient) {}
  /**
   * Get the list of all SALT Astronomers
   */
  getSaltAstronomers(): Observable<UserListItem[]> {
    const uri = environment.apiUrl + "/salt-astronomers/";
    return this.http
      .get<UserListItem[]>(uri)
      .pipe(
        map((saltAstronomers: UserListItem[]) =>
          saltAstronomers.map((saltAstronomer: UserListItem) =>
            camelcaseKeys(saltAstronomer, { deep: true }),
          ),
        ),
      );
  }
}
