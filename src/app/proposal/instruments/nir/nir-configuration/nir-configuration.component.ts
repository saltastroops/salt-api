import { Component, Input } from "@angular/core";

import { NirConfiguration } from "../../../../types/nir";

@Component({
  selector: "wm-nir-configuration",
  templateUrl: "./nir-configuration.component.html",
  styleUrls: ["./nir-configuration.component.scss"],
})
export class NirConfigurationComponent {
  @Input() nirConfiguration!: NirConfiguration | null;
}
