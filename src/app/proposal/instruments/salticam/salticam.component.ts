import { Component, Input } from "@angular/core";

import { PayloadConfiguration } from "../../../types/observation";
import { Salticam } from "../../../types/salticam";

@Component({
  selector: "wm-salticam",
  templateUrl: "./salticam.component.html",
  styleUrls: ["./salticam.component.scss"],
})
export class SalticamComponent {
  @Input() salticam!: Salticam;
  @Input() payloadConfiguration!: PayloadConfiguration;
}
