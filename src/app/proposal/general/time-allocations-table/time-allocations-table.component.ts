import { Component, Input } from "@angular/core";

import { TimeAllocation } from "../../../types/proposal";

@Component({
  selector: "wm-time-allocations-table",
  templateUrl: "./time-allocations-table.component.html",
  styleUrls: ["./time-allocations-table.component.scss"],
})
export class TimeAllocationsTableComponent {
  @Input() time_allocations!: TimeAllocation[];
}
