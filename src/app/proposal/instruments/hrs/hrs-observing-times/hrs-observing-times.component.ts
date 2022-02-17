import { Component, Input } from "@angular/core";

import { Hrs } from "../../../../types/hrs";

@Component({
  selector: "wm-hrs-observing-times",
  templateUrl: "./hrs-observing-times.component.html",
  styleUrls: ["./hrs-observing-times.component.scss"],
})
export class HrsObservingTimesComponent {
  @Input() hrs!: Hrs;
}
