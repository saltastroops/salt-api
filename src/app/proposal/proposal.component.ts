import { Component, OnInit } from "@angular/core";
import { ActivatedRoute } from "@angular/router";

import { Subscription, merge, of } from "rxjs";
import {
  catchError,
  debounceTime,
  map,
  mapTo,
  switchMap,
  tap,
} from "rxjs/operators";

import { ProposalService } from "../service/proposal.service";
import { Proposal } from "../types/proposal";

@Component({
  selector: "wm-proposal",
  templateUrl: "./proposal.component.html",
  styleUrls: ["./proposal.component.scss"],
})
export class ProposalComponent implements OnInit {
  readonly DEBOUNCE_TIME = 100;

  blockId!: number;
  proposal: Proposal | null = null;
  proposalCode!: string;
  isLoading = false;
  error?: string;
  contentSubscription!: Subscription;
  isLoadingSubscription!: Subscription;
  errorSubscription!: Subscription;

  constructor(
    private route: ActivatedRoute,
    private proposalService: ProposalService,
  ) {}

  ngOnInit(): void {
    const trigger$ = this.route.params.pipe(debounceTime(this.DEBOUNCE_TIME));

    const requestResult$ = trigger$
      .pipe(
        map((params) => params["proposal-code"]),
        tap((proposalCode) => {
          this.proposalCode = proposalCode;
        }),
      )
      .pipe(
        switchMap((proposalCode) => {
          return this.proposalService.getProposal(proposalCode).pipe(
            map((b) => ({ success: true, payload: b })),
            catchError((error) => of({ success: false, payload: error })),
          );
        }),
      );

    const content$ = requestResult$.pipe(
      map((v) => (v.success ? v.payload : null)),
    );

    const error$ = merge(
      this.route.params.pipe(mapTo(null)),
      requestResult$.pipe(map((v) => (!v.success ? v.payload : null))),
    );

    const isLoading$ = merge(
      this.route.params.pipe(mapTo(true)),
      requestResult$.pipe(mapTo(false)),
    );

    // If we use the async pipe in the template, at this point in time the streams just
    // created have not been subscribed to yet. However, we are about to select a block,
    // and hence events may be missed (most notably the isLoading one). Hence we have to
    // explicitly subscribe ourselves.
    this.contentSubscription = content$.subscribe((proposal) => {
      this.proposal = proposal;
    });
    this.errorSubscription = error$.subscribe((error) => {
      if (error) {
        if (error.status === 404 || error.status === 422) {
          this.error = `Proposal code ${this.proposalCode} not found.`;
        } else {
          this.error = `Failed to fetch proposal '${this.proposalCode}'.`;
        }
      } else {
        // The error stream emits null if there is no error.
        this.error = undefined;
      }
    });
    this.isLoadingSubscription = isLoading$.subscribe((isLoading) => {
      // For some reason in some browsers the loading event is fired only a second or
      // two after the content one. For that reason, in the template the loading
      // indicator should only be displayed if the loading flag is true and the proposal
      // is defined. Otherwise, the loading indicator and the proposal content might be
      // displayed at the same time for a short while.
      if (isLoading) {
        this.proposal = null;
        this.error = undefined;
      }
      this.isLoading = isLoading;
    });
  }

  onClick(blockId: number): void {
    this.blockId = blockId;
    const element = document.querySelector(
      '[data-test="block-selection"]',
    ) as HTMLElement;
    element.scrollIntoView({ behavior: "smooth" });
  }

  changeSemester(semester: string): void {
    this.isLoading = true;
    if (this.proposal) {
      this.proposalService
        .getProposal(this.proposal.proposalCode, semester, this.proposal.phase)
        .subscribe((p) => {
          this.proposal = p;
          this.isLoading = false;
        });
    }
  }
}
