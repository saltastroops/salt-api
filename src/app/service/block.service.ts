import { Observable } from "rxjs";

import { Block } from "../types/block";

export abstract class BlockService {
  public abstract getBlock(id: number): Observable<Block>;
}
