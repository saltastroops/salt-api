import { Component, Input, OnInit } from "@angular/core";

import { HrsConfiguration } from "../../../../types/hrs";

@Component({
  selector: "wm-hrs-configuration",
  templateUrl: "./hrs-configuration.component.html",
  styleUrls: ["./hrs-configuration.component.scss"],
})
export class HrsConfigurationComponent implements OnInit {
  @Input() hrsConfig!: HrsConfiguration;
  resolution = "";

  ngOnInit(): void {
    const mode = this.hrsConfig.mode;

    switch (mode) {
      case "Low Resolution":
        this.resolution = "low-resolution";
        break;

      case "Medium Resolution":
        this.resolution = "medium-resolution";
        break;

      case "High Resolution":
        this.resolution = "high-resolution";
        break;

      case "High Stability":
        this.resolution = "high-stability";
        break;

      case "Int Cal Fiber":
        this.resolution = "int-cal-fiber";
        break;
    }
  }
}
