import { Component, Input } from "@angular/core";

@Component({
  selector: "wm-loading-indicator",
  templateUrl: "./loading-indicator.component.html",
  styleUrls: ["./loading-indicator.component.scss"],
})
export class LoadingIndicatorComponent {
  @Input() message = "Loading...";
}
