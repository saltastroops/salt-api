import { Component, Input, OnInit } from "@angular/core";

import { Block } from "../../../../types/block";

@Component({
  selector: "wm-iterations",
  templateUrl: "./iterations.component.html",
  styleUrls: ["./iterations.component.scss"],
})
export class IterationsComponent implements OnInit {
  @Input() block!: Block;

  acceptedObservations!: number;

  rejectedObservations!: number;

  ngOnInit(): void {
    this.acceptedObservations = this.block.blockVisits.filter(
      (o) => o.status === "Accepted",
    ).length;
    this.rejectedObservations = this.block.blockVisits.filter(
      (o) => o.status === "Rejected",
    ).length;
  }
}
