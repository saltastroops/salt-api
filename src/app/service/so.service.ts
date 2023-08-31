import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";

import * as camelcaseKeys from "camelcase-keys";
import { Observable } from "rxjs";
import { map } from "rxjs/operators";

import { environment } from "../../environments/environment";
import { Block } from "../types/block";

@Injectable({
  providedIn: "root",
})
export class SoService {
  constructor(private http: HttpClient) {}

  getCurrentBlock(): Observable<Block> {
    const uri = environment.apiUrl + "/blocks/current-block";
    return this.http
      .get<Block>(uri)
      .pipe(map((block: Block) => camelcaseKeys(block, { deep: true })));
  }
  getNextScheduledBlock(): Observable<Block> {
    const uri = environment.apiUrl + "/blocks/next-scheduled-block";
    return this.http
      .get<Block>(uri)
      .pipe(map((block) => camelcaseKeys(block, { deep: true })));
  }
}
