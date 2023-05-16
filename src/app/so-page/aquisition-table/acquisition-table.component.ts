import { Component, Input } from "@angular/core";

import { Acquisition } from "../../types/observation";
import { originalFinderChartURL } from "../../utils";

@Component({
  selector: "wm-acquisition-table",
  templateUrl: "./acquisition-table.component.html",
  styleUrls: ["./acquisition-table.component.scss"],
})
export class AcquisitionTableComponent {
  @Input() acquisition!: Acquisition;
  originalFinderChartURL = originalFinderChartURL;
}
