import { Component, Input } from "@angular/core";

import { Nir } from "../../../types/nir";
import { PayloadConfiguration } from "../../../types/observation";

@Component({
  selector: "wm-nir",
  templateUrl: "./nir.component.html",
  styleUrls: ["./nir.component.scss"],
})
export class NirComponent {
  @Input() nir!: Nir;
  @Input() payloadConfiguration!: PayloadConfiguration;
}
