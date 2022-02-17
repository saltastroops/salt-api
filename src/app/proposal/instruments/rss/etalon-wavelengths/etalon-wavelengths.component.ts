import { Component, Input } from "@angular/core";

@Component({
  selector: "wm-etalon-wvelengths",
  templateUrl: "./etalon-wavelengths.component.html",
  styleUrls: ["./etalon-wavelengths.component.scss"],
})
export class EtalonWavelengthsComponent {
  @Input() etalonConfiguration!: number[];
}
