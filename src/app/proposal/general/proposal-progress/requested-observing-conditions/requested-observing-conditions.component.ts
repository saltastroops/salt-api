import { Component, Input } from "@angular/core";

@Component({
  selector: "wm-requested-observing-conditions",
  templateUrl: "./requested-observing-conditions.component.html",
  styleUrls: ["./requested-observing-conditions.component.scss"],
})
export class RequestedObservingConditionsComponent {
  @Input() lastObservingConstraints!: {
    seeing: number;
    transparency: string;
    description: string;
  };
}
