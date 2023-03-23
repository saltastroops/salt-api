import { Observable } from "rxjs";

import {
  Block,
  BlockRejectionReason,
  BlockStatus,
  BlockStatusValue,
} from "../types/block";
import { BlockVisitStatus } from "../types/common";

export abstract class BlockService {
  public abstract getBlock(id: number): Observable<Block>;

  public abstract updateBlockStatus(
    id: number,
    blockStatus: BlockStatusValue,
    statusReason: string | number,
  ): Observable<BlockStatus>;

  public abstract updateBlockVisitStatus(
    blockVisitId: number,
    blockVisitStatus: BlockVisitStatus,
    rejectionReason: BlockRejectionReason | null,
  ): Observable<void>;
}
