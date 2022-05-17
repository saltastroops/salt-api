import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";

import * as camelcaseKeys from "camelcase-keys";
import { Observable } from "rxjs";
import { map } from "rxjs/operators";

import { environment } from "../../environments/environment";
import { Institution } from "../types/institution";

@Injectable({
  providedIn: "root",
})
export class InstitutionService {
  constructor(private http: HttpClient) {}

  /**
   * Get the list of institutions
   */
  getInstitutions(): Observable<Institution[]> {
    const uri = environment.apiUrl + "/institutions/";
    return this.http
      .get<Institution[]>(uri)
      .pipe(
        map((institutions: Institution[]) =>
          institutions.map((institution: Institution) =>
            camelcaseKeys(institution, { deep: true }),
          ),
        ),
      );
  }
}
