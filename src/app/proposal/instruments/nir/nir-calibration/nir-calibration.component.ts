import { Component, Input } from "@angular/core";

@Component({
  selector: "wm-nir-calibration",
  templateUrl: "./nir-calibration.component.html",
  styleUrls: ["./nir-calibration.component.scss"],
})
export class NirCalibrationComponent {
  @Input() lamp!: string | null;
  @Input() filter!: string | null;
}
