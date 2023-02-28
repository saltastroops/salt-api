import { Observable } from "rxjs";

import { Block, BlockRejectionReason } from "../types/block";
import { BlockVisitStatus } from "../types/common";

export abstract class BlockService {
  public abstract getBlock(id: number): Observable<Block>;

  public abstract updateBlockVisitStatus(
    blockVisitId: number,
    blockVisitStatus: BlockVisitStatus,
    rejectionReason: BlockRejectionReason | null,
  ): Observable<void>;
}
