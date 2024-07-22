import { Component, Input } from "@angular/core";

import { Block } from "../../../../types/block";

@Component({
  selector: "wm-observing-conditions",
  templateUrl: "./observing-conditions.component.html",
  styleUrls: ["./observing-conditions.component.scss"],
})
export class ObservingConditionsComponent {
  @Input() block!: Block;
  @Input() observationTime!: number;

  acceptedObservations = (): number =>
    this.block.blockVisits.filter((o) => o.status === "Accepted").length;
  rejectedObservations = (): number =>
    this.block.blockVisits.filter((o) => o.status === "Rejected").length;
}
