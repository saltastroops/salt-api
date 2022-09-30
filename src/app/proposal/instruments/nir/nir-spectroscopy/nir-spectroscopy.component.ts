import { Component, Input } from "@angular/core";

import { NirSpectroscopy } from "../../../../types/nir";

@Component({
  selector: "wm-nir-spectroscopy",
  templateUrl: "./nir-spectroscopy.component.html",
  styleUrls: ["./nir-spectroscopy.component.scss"],
})
export class NirSpectroscopyComponent {
  @Input() nirSpectroscopy!: NirSpectroscopy | null;
  @Input() filter!: string;
}
