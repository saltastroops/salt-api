import { Component, Input, OnInit } from "@angular/core";

import { parseISO } from "date-fns";

import { environment } from "../../../../../environments/environment";
import { FinderChart, Observation } from "../../../../types/observation";
import { finderChartURL } from "../../../../util";

@Component({
  selector: "wm-observation",
  templateUrl: "./observation.component.html",
  styleUrls: ["./observation.component.scss"],
})
export class ObservationComponent implements OnInit {
  @Input() observation!: Observation;

  positionAngles!: Array<number | null>;
  firstValidFrom: Date | undefined;
  lastValidUntil: Date | undefined;

  ngOnInit(): void {
    // TODO: Must be fixed
    this.positionAngles = this.observation.telescopeConfigurations.map(
      (tc) => tc.positionAngle,
    );
    this.firstValidFrom = parseISO("1970-01-01T00:00:00Z");
    this.lastValidUntil = parseISO("2100-01-01T00:00:00Z");
  }

  thumbnailFinderChartURL(finderChart: FinderChart): string {
    const url = finderChartURL(
      finderChart,
      ["thumbnail", "original"],
      ["png", "jpg"],
      environment.apiUrl,
    );
    return url || "/assets/noun-missing-2181345.png";
  }

  originalFinderChartURL(finderChart: FinderChart): string {
    const url = finderChartURL(
      finderChart,
      ["original"],
      ["pdf", "png", "jpg"],
      environment.apiUrl,
    );
    return url || "/assets/noun-missing-2181345.png";
  }
}
