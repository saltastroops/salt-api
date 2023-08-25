import { Component, Input } from "@angular/core";

import { Block } from "../../../../types/block";

@Component({
  selector: "wm-iterations",
  templateUrl: "./iterations.component.html",
  styleUrls: ["./iterations.component.scss"],
})
export class IterationsComponent {
  @Input() block!: Block;

  acceptedObservations = (): number =>
    this.block.blockVisits.filter((o) => o.status === "Accepted").length;
  rejectedObservations = (): number =>
    this.block.blockVisits.filter((o) => o.status === "Rejected").length;
}
