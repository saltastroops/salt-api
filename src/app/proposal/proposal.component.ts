import { Component, OnInit } from "@angular/core";
import { ActivatedRoute } from "@angular/router";

import { Subscription, merge, of } from "rxjs";
import {
  catchError,
  debounceTime,
  map,
  mapTo,
  switchMap,
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

  blockName = "";
  proposal: Proposal | null = null;
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
      .pipe(map((params) => params["proposal-code"]))
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
      this.error = error;
    });
    this.isLoadingSubscription = isLoading$.subscribe((isLoading) => {
      if (isLoading) {
        this.proposal = null;
      }
      this.isLoading = isLoading;
    });
  }

  onClick(block: string): void {
    this.blockName = block;
    const element = document.querySelector(
      '[data-test="block-selection"]',
    ) as HTMLElement;
    element.scrollIntoView({ behavior: "smooth" });
  }
}