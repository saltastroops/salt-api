import { Component, Input } from "@angular/core";

import { Block } from "../../../types/block";
import {parseISO} from "date-fns";
import {FinderChart} from "../../../types/observation";
import {finderChartURL} from "../../../util";
import {environment} from "../../../../environments/environment";

@Component({
  selector: "wm-block",
  templateUrl: "./block.component.html",
  styleUrls: ["./block.component.scss"],
})
export class BlockComponent {
  @Input() block!: Block;
  firstValidFrom: Date = parseISO("1970-01-01T00:00:00Z");
  lastValidUntil: Date = parseISO("2100-01-01T00:00:00Z");

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
