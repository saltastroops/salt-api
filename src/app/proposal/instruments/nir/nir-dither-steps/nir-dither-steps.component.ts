import { Component, Input } from "@angular/core";

import { NirDitherStep } from "../../../../types/nir";

@Component({
  selector: "wm-nir-dither-steps",
  templateUrl: "./nir-dither-steps.component.html",
  styleUrls: ["./nir-dither-steps.component.scss"],
})
export class NirDitherStepsComponent {
  @Input() nirDitherSteps!: NirDitherStep[];
}
