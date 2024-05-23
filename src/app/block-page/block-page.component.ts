import { Component, OnInit } from '@angular/core';
import { BlockService } from "../service/block.service";
import { Block } from "../types/block";
import { ActivatedRoute } from "@angular/router";
import { ProposalService } from "../service/proposal.service";
import { Proposal } from "../types/proposal";

@Component({
  selector: 'wm-block-page',
  templateUrl: './block-page.component.html',
  styleUrls: ['./block-page.component.scss']
})
export class BlockPageComponent implements OnInit {
  block!: Block;
  proposal!: Proposal;
  blockId!: number;
  loading = false;
  error: undefined | string = undefined;

  constructor( private blockService: BlockService,private proposalService: ProposalService,private route: ActivatedRoute,) { }

  ngOnInit(): void {
    this.loading = true;
    this.route.params.subscribe((params) => {
      this.blockId = params.blockId;
      this.fetchBlockDetails();
    });
  }

  private fetchBlockDetails(): void {
    this.error = undefined
    this.blockService.getBlock(this.blockId).subscribe(
      (blockData) => {
        this.block = blockData;
        const proposalCode = blockData.proposalCode;

        this.fetchProposalDetails(proposalCode);
      },
      () => {
        this.loading = false
        this.error = `Failed to fetch block ${this.blockId}.`;
      }
    );
  }

  private fetchProposalDetails(proposalCode: string): void {
    this.proposalService.getProposal(proposalCode).subscribe(
      (proposalData) => {
        this.loading = false
        this.proposal = proposalData;
      },
      () => {
        this.loading = false
        this.error = `Failed to fetch proposal details for the block ${this.blockId}.`;
      }
    );
  }

}
