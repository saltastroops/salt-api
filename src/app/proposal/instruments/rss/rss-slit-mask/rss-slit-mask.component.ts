import { Component, Input } from "@angular/core";

import { RssMask } from "../../../../types/rss";

@Component({
  selector: "wm-rss-slit-mask",
  templateUrl: "./rss-slit-mask.component.html",
  styleUrls: ["./rss-slit-mask.component.scss"],
})
export class RssSlitMaskComponent {
  @Input() slitMask!: RssMask;
}
