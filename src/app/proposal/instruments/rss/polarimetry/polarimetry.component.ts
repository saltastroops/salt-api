import { Component, Input } from "@angular/core";

import { RssPolarimetryPattern } from "../../../../types/rss";

@Component({
  selector: "wm-polarimetry",
  templateUrl: "./polarimetry.component.html",
  styleUrls: ["./polarimetry.component.scss"],
})
export class PolarimetryComponent {
  @Input() pattern!: RssPolarimetryPattern;
  @Input() beamSplitterOrientation!: string;
}
