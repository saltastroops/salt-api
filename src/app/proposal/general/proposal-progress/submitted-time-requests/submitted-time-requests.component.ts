import { Component, Input } from "@angular/core";

import { TimeStatistics } from "../../../../types/proposal";

@Component({
  selector: "wm-submitted-time-requests",
  templateUrl: "./submitted-time-requests.component.html",
  styleUrls: ["./submitted-time-requests.component.scss"],
})
export class SubmittedTimeRequestsComponent {
  @Input() submittedTimeRequests!: TimeStatistics[];
}
