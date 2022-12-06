import { Component, Input, OnInit } from "@angular/core";

@Component({
  selector: "wm-loading-indicator",
  templateUrl: "./loading-indicator.component.html",
  styleUrls: ["./loading-indicator.component.scss"],
})
export class LoadingIndicatorComponent implements OnInit {
  @Input() message = "Loading...";

  constructor() {}

  ngOnInit(): void {}
}
