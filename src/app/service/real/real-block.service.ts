import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Injectable } from "@angular/core";

import * as camelcaseKeys from "camelcase-keys";
import { Observable } from "rxjs";
import { map } from "rxjs/operators";

import { environment } from "../../../environments/environment";
import { Block, BlockRejectionReason } from "../../types/block";
import { BlockVisit, BlockVisitStatus } from "../../types/common";
import { BlockService } from "../block.service";

@Injectable({
  providedIn: "root",
})
export class RealBlockService implements BlockService {
  constructor(private http: HttpClient) {}

  /**
   * Get a block from the API server.
   *
   * If the request fails the stream terminates with a generic error message as error.
   *
   * @param id Block id.
   */
  getBlock(id: number): Observable<Block> {
    const uri = environment.apiUrl + "/blocks/" + id;
    return this.http
      .get<Block>(uri)
      .pipe(map((block: Block) => camelcaseKeys(block, { deep: true })));
  }

  /**
   * Update a block visit status from the API server.
   *
   * @param blockVisitId Block visit id.
   * @param blockVisitStatus Block visit status.
   * @param rejectionReason Block rejection reason.
   */
  updateBlockVisitStatus(
    blockVisitId: number,
    blockVisitStatus: BlockVisitStatus,
    rejectionReason: BlockRejectionReason | null,
  ): Observable<void> {
    const uri =
      environment.apiUrl + "/block-visits/" + blockVisitId + "/status";
    const headers = new HttpHeaders({
      "Content-type": "application/json",
    });
    const data = {
      status: blockVisitStatus,
      reason: rejectionReason,
    };
    return this.http.patch<void>(uri, data, { headers });
  }
}
