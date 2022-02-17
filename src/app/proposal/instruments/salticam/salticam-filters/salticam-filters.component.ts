import { Component, Input } from "@angular/core";

import { SalticamExposure } from "../../../../types/salticam";

@Component({
  selector: "wm-salticam-filters",
  templateUrl: "./salticam-filters.component.html",
  styleUrls: ["./salticam-filters.component.scss"],
})
export class SalticamFiltersComponent {
  @Input() salticamExposures!: SalticamExposure[];
}
