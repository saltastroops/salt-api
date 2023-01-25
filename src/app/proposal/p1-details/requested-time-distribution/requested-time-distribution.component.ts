import { Component, Input } from "@angular/core";

import { RequestedTime } from "../../../types/proposal";

@Component({
  selector: "wm-requested-time-distribution",
  templateUrl: "./requested-time-distribution.component.html",
  styleUrls: ["./requested-time-distribution.component.scss"],
})
export class RequestedTimeDistributionComponent {
  @Input() requestedTime!: RequestedTime;
}
