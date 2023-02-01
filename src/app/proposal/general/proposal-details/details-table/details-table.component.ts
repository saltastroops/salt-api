import { Component, Input, OnChanges, OnInit } from "@angular/core";

import { Proposal } from "../../../../types/proposal";

@Component({
  selector: "wm-details-table",
  templateUrl: "./details-table.component.html",
  styleUrls: ["./details-table.component.scss"],
})
export class DetailsTableComponent implements OnChanges, OnInit {
  @Input() proposal!: Proposal;
  releaseDate!: Date;
  ngOnInit(): void {
    this.updateReleaseDate();
  }

  ngOnChanges(): void {
    this.updateReleaseDate();
  }

  updateReleaseDate(): void {
    console.log("##: ", this.proposal.generalInfo.proprietaryPeriod.startDate);
    const tmpDate = new Date(
      this.proposal.generalInfo.proprietaryPeriod.startDate,
    );
    this.releaseDate = new Date(
      tmpDate.setMonth(
        tmpDate.getMonth() + this.proposal.generalInfo.proprietaryPeriod.period,
      ),
    );
  }

  onProprietaryPeriodUpdate(proprietaryPeriod: number): void {
    this.proposal.generalInfo.proprietaryPeriod.period = proprietaryPeriod;
    this.updateReleaseDate();
  }
}
