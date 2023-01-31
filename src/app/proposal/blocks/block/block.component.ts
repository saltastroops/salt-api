import { Component, Input, OnInit } from "@angular/core";

import { parseISO } from "date-fns";

import { environment } from "../../../../environments/environment";
import { Block } from "../../../types/block";
import { FinderChart } from "../../../types/observation";
import { currentJulianDay, finderChartURL } from "../../../util";

@Component({
  selector: "wm-block",
  templateUrl: "./block.component.html",
  styleUrls: ["./block.component.scss"],
})
export class BlockComponent implements OnInit {
  @Input() block!: Block;

  validFrom!: Date;

  validUntil!: Date;

  ngOnInit(): void {
    const jd = currentJulianDay();
    this.validFrom = jd.start;
    this.validUntil = jd.end;
  }

  validSortedFinderCharts(finderCharts: FinderChart[]): FinderChart[] {
    const isValid = (fc: FinderChart) =>
      (fc.validFrom === null || parseISO(fc.validFrom) <= this.validUntil) &&
      (fc.validUntil === null || parseISO(fc.validUntil) >= this.validFrom);
    const millisecondsFromEpoch = (fc: FinderChart) =>
      fc.validFrom ? parseISO(fc.validFrom).getTime() : 0;
    const compare = (fc1: FinderChart, fc2: FinderChart) =>
      millisecondsFromEpoch(fc1) - millisecondsFromEpoch(fc2);
    return [...finderCharts.filter(isValid)].sort(compare);
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
