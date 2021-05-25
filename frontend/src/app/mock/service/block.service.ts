import { Injectable } from '@angular/core';
import { Block } from '../../types';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class BlockService implements BlockService {
  getBlock(id: number): Observable<Block> {
    return of({
      id,
      name: `Block-${id}`,
    });
  }
}
