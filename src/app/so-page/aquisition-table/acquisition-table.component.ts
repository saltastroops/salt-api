import { Component, Input } from "@angular/core";

import { Acquisition } from "../../types/so";
import { originalFinderChartURL, thumbnailFinderChartURL } from "../../utils";

@Component({
  selector: "wm-acquisition-table",
  templateUrl: "./acquisition-table.component.html",
  styleUrls: ["./acquisition-table.component.scss"],
})
export class AcquisitionTableComponent {
  @Input() acquisition!: Acquisition;
  @Input() positionAngle: number | null = null;
  originalFinderChartURL = originalFinderChartURL;
  thumbnailFinderChartURL = thumbnailFinderChartURL;
}
