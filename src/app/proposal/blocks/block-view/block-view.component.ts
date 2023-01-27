import {
  Component,
  Input,
  OnChanges,
  OnDestroy,
  OnInit,
  SimpleChanges,
} from "@angular/core";

import { Subject, Subscription, merge, of } from "rxjs";
import {
  catchError,
  debounceTime,
  map,
  mapTo,
  switchMap,
} from "rxjs/operators";

import { BlockService } from "../../../service/block.service";
import { Block, BlockSummary } from "../../../types/block";

@Component({
  selector: "wm-block-view",
  templateUrl: "./block-view.component.html",
  styleUrls: ["./block-view.component.scss"],
})
export class BlockViewComponent implements OnInit, OnDestroy, OnChanges {
  @Input() blocks!: BlockSummary[];
  @Input() blockId!: number;

  readonly DEBOUNCE_TIME = 100;

  selectedBlock!: BlockSummary | null;

  selectedBlockId$: Subject<number> = new Subject();

  displayedBlock?: Block;

  error?: string;

  isLoading = false;

  contentSubscription!: Subscription;

  errorSubscription!: Subscription;

  isLoadingSubscription!: Subscription;

  constructor(public blockService: BlockService) {}

  ngOnInit(): void {
    const trigger$ = this.selectedBlockId$.pipe(
      debounceTime(this.DEBOUNCE_TIME),
    );

    const requestResult$ = trigger$.pipe(
      switchMap((id) => {
        return this.blockService.getBlock(id).pipe(
          map((b) => ({ success: true, payload: b })),
          catchError((error) => of({ success: false, payload: error })),
        );
      }),
    );

    const content$ = requestResult$.pipe(
      map((v) => (v.success ? v.payload : null)),
    );

    const error$ = merge(
      this.selectedBlockId$.pipe(mapTo(null)),
      requestResult$.pipe(map((v) => (!v.success ? v.payload : null))),
    );

    const isLoading$ = merge(
      this.selectedBlockId$.pipe(mapTo(true)),
      requestResult$.pipe(mapTo(false)),
    );

    // If we use the async pipe in the template, at this point in time the streams just
    // created have not been subscribed to yet. However, we are about to select a block,
    // and hence events may be missed (most notably the isLoading one). Hence we have to
    // explicitly subscribe ourselves.
    this.contentSubscription = content$.subscribe((block) => {
      this.displayedBlock = block;
    });
    this.errorSubscription = error$.subscribe((error) => {
      this.error = error;
    });
    this.isLoadingSubscription = isLoading$.subscribe((isLoading) => {
      this.isLoading = isLoading;
    });

    // Select the first block
    if (this.blocks.length) {
      this.selectBlock(this.blocks[0]);
    }
  }

  ngOnDestroy(): void {
    this.contentSubscription.unsubscribe();
    this.errorSubscription.unsubscribe();
    this.isLoadingSubscription.unsubscribe();
  }

  selectBlock(block: BlockSummary): void {
    this.selectedBlock = block;
    this.selectedBlockId$.next(block.id);
  }

  ngOnChanges(changes: SimpleChanges): void {
    for (const propName in changes) {
      if (propName === "blockId") {
        const changedProp = changes[propName];
        const selectedBlockId = changedProp.currentValue;
        const index = this.blocks.findIndex(
          (block) => block.id === selectedBlockId,
        );
        if (index === -1) {
          // The index is -1 if a block id selected from the list of executed
          // observations is from another semester.
          this.selectedBlock = null;
          this.selectedBlockId$.next(selectedBlockId);
        } else {
          this.selectBlock(this.blocks[index]);
        }
      }
    }
  }
}
