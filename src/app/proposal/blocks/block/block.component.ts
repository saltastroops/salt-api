import { Component, Input, OnInit } from "@angular/core";

import { parseISO } from "date-fns";

import { environment } from "../../../../environments/environment";
import { Block } from "../../../types/block";
import { FinderChart } from "../../../types/observation";
import { finderChartURL } from "../../../util";

@Component({
  selector: "wm-block",
  templateUrl: "./block.component.html",
  styleUrls: ["./block.component.scss"],
})
export class BlockComponent implements OnInit {
  @Input() block!: Block;
  firstValidFrom: Date | undefined;
  lastValidUntil: Date | undefined;

  ngOnInit(): void {
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
