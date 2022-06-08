import { Component, Input, OnInit } from "@angular/core";

import { ChargedTime, TimeAllocation } from "../../../types/proposal";

@Component({
  selector: "wm-charged-time",
  templateUrl: "./charged-time.component.html",
  styleUrls: ["./charged-time.component.scss"],
})
export class ChargedTimeComponent implements OnInit {
  @Input() chargedTime!: ChargedTime;
  @Input() timeAllocations!: TimeAllocation[];
  allocatedP0ToP3Time = 0;
  chargedTimeP0ToP3 = 0;

  ngOnInit(): void {
    this.allocatedP0ToP3Time = this.timeAllocations
      ? this.timeAllocations
          .map(
            (timeAllocation) =>
              timeAllocation.priority0 +
              timeAllocation.priority1 +
              timeAllocation.priority2 +
              timeAllocation.priority3,
          )
          .reduce((a, b) => a + b, 0)
      : 0;
    this.chargedTimeP0ToP3 =
      this.chargedTime.priority0 +
      this.chargedTime.priority1 +
      this.chargedTime.priority2 +
      this.chargedTime.priority3;
  }
}
