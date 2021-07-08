import { Injectable } from '@angular/core';
import { Block } from '../../types';
import { Observable, of, throwError } from 'rxjs';
import { delay, mergeMap } from 'rxjs/operators';
import {blockGeneralDetails} from '../block-data';

@Injectable({
  providedIn: 'root',
})
export class MockBlockService implements MockBlockService {
  getBlock(id: number): Observable<Block> {
    if (id === 42) {
      return of(1).pipe(
        delay(Math.random() * 1000),
        mergeMap(() => throwError('Block 42 is deliberately inaccessible'))
      );
    }
    return of({
      ...blockGeneralDetails
    }).pipe(delay(Math.random() * 1000));
  }
}
