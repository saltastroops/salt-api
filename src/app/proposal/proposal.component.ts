import { Component, OnInit } from "@angular/core";
import { ActivatedRoute } from "@angular/router";

import { Observable } from "rxjs";

import { ProposalService } from "../service/proposal.service";
import { Proposal } from "../types/proposal";

@Component({
  selector: "wm-proposal",
  templateUrl: "./proposal.component.html",
  styleUrls: ["./proposal.component.scss"],
})
export class ProposalComponent implements OnInit {
  proposalCode = "";
  blockName = "";
  proposal!: Observable<Proposal>;

  constructor(
    private route: ActivatedRoute,
    private proposalService: ProposalService,
  ) {}

  ngOnInit(): void {
    const routeParams = this.route.snapshot.paramMap;
    this.proposalCode = routeParams.get("proposal-code") || "";
    this.proposal = this.proposalService.getProposal(this.proposalCode);
  }

  onClick(block: string): void {
    this.blockName = block;
    const element = document.querySelector(
      '[data-test="block-selection"]',
    ) as HTMLElement;
    element.scrollIntoView({ behavior: "smooth" });
  }
}
