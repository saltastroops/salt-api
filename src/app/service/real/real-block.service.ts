import { Injectable } from '@angular/core';
import { BlockService } from '../block.service';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { environment } from '../../../environments/environment';
import { catchError, map } from 'rxjs/operators';
import { Block } from '../../types/block';
import * as camelcaseKeys from 'camelcase-keys';

@Injectable({
  providedIn: 'root',
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
    const uri = environment.apiUrl + '/blocks/' + id;
    return this.http
      .get<Block>(uri)
      .pipe(map((block: Block) => camelcaseKeys(block, { deep: true })));
  }
}
