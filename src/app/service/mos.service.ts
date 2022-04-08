import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Injectable } from "@angular/core";

import * as camelcaseKeys from "camelcase-keys";
import { Observable } from "rxjs";
import { map, switchMap } from "rxjs/operators";

import { environment } from "../../environments/environment";
import { MosBlock, MosMaskCutDetails } from "../types/mos";

@Injectable({
  providedIn: "root",
})
export class MosService {
  constructor(private http: HttpClient) {}
  /**
   * Request mos data.
   *
   * @param from_semester The list of semesters
   * @param to_semester The list of semesters
   */
  getMosBlocks(
    from_semester: string,
    to_semester: string,
  ): Observable<MosBlock[]> {
    const uri =
      environment.apiUrl +
      "/rss/mos-mask-metadata?from=" +
      from_semester +
      "&to=" +
      to_semester;
    const headers = new HttpHeaders({
      "Content-type": "application/json",
    });
    return this.http.get<MosBlock[]>(uri, { headers }).pipe(
      switchMap(() => this.http.get<MosBlock[]>(uri)),
      map((mosBlocks: MosBlock[]) =>
        mosBlocks.map((mosBlock: MosBlock) =>
          camelcaseKeys(mosBlock, { deep: true }),
        ),
      ),
    );
  }

  getMosMasksInMagazine(): Observable<string[]> {
    const uri = environment.apiUrl + "/rss/masks-in-magazine?mask_type=MOS";
    return this.http.get<string[]>(uri);
  }
  getObsoleteRssMasks(): Observable<string[]> {
    const uri = environment.apiUrl + "/rss/obsolete-masks-in-magazine";
    return this.http.get<string[]>(uri);
  }

  updateMosMask(mask: MosMaskCutDetails): Observable<MosMaskCutDetails> {
    const uri = environment.apiUrl + "/rss/mos-mask-metadata/" + mask.barcode;
    return this.http
      .patch<MosMaskCutDetails>(uri, {
        cut_by: mask.cutBy,
        cut_date: mask.cutDate,
        mask_comment: mask.maskComment,
      })
      .pipe(map((mosBlock) => camelcaseKeys(mosBlock, { deep: true })));
  }
}
