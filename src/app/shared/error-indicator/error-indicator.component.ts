import { Component, Input, OnInit } from "@angular/core";

@Component({
  selector: "wm-error-indicator",
  templateUrl: "./error-indicator.component.html",
  styleUrls: ["./error-indicator.component.scss"],
})
export class ErrorIndicatorComponent implements OnInit {
  @Input() message = "Oops. Something is wrong.";

  constructor() {}

  ngOnInit(): void {}
}
