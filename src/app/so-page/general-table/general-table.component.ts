import { Component, Input, OnInit } from "@angular/core";

import { Block } from "../../types/block";
import { Investigator, Proposal } from "../../types/proposal";

@Component({
  selector: "wm-general-table",
  templateUrl: "./general-table.component.html",
  styleUrls: ["./general-table.component.scss"],
})
export class GeneralTableComponent implements OnInit {
  @Input() proposal!: Proposal;
  @Input() block!: Block;
  principalInvestigator!: Investigator;
  principalContact!: Investigator;
  isShowSummary = false;

  ngOnInit(): void {
    this.principalInvestigator = this.proposal.investigators.find(
      (i) => i.isPi,
    ) as Investigator;
    this.principalContact = this.proposal.investigators.find(
      (i) => i.isPc,
    ) as Investigator;
  }
  toggleSummary(): void {
    this.isShowSummary = !this.isShowSummary;
  }
}
