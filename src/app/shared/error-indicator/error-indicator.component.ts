import { Component, Input } from "@angular/core";

@Component({
  selector: "wm-error-indicator",
  templateUrl: "./error-indicator.component.html",
  styleUrls: ["./error-indicator.component.scss"],
})
export class ErrorIndicatorComponent {
  @Input() message = "Oops. Something is wrong.";
}
