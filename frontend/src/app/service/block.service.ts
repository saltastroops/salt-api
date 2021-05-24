import { Observable } from 'rxjs';
import { Block } from '../types';

export abstract class BlockService {
  public abstract getBlock(id: number): Observable<Block>;
}
