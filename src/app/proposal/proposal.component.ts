import { Component, OnInit } from "@angular/core";
import { ActivatedRoute } from "@angular/router";

import { Observable } from "rxjs";
import { delay } from "rxjs/operators";

import { ProposalService } from "../service/proposal.service";
import { Proposal } from "../types/proposal";
import { AutoUnsubcribe } from "../utils";

@Component({
  selector: "wm-proposal",
  templateUrl: "./proposal.component.html",
  styleUrls: ["./proposal.component.scss"],
})
@AutoUnsubcribe()
export class ProposalComponent implements OnInit {
  proposalCode = "";
  blockName = "";
  proposal$!: Observable<Proposal>;
  proposal: Proposal | null = null;
  loading = false;
  loadingFailed = false;

  constructor(
    private route: ActivatedRoute,
    private proposalService: ProposalService,
  ) {}

  ngOnInit(): void {
    const routeParams = this.route.snapshot.paramMap;
    this.proposalCode = routeParams.get("proposal-code") || "";
    this.proposal$ = this.proposalService.getProposal(this.proposalCode);
    this.loading = true;
    this.proposal$.subscribe(
      (proposal) => {
        this.loading = false;
        this.proposal = proposal;
      },
      () => {
        this.loading = false;
        this.loadingFailed = true;
      },
    );
  }

  onClick(block: string): void {
    this.blockName = block;
    const element = document.querySelector(
      '[data-test="block-selection"]',
    ) as HTMLElement;
    element.scrollIntoView({ behavior: "smooth" });
  }
}
