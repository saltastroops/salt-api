import { Component, Input } from "@angular/core";

import { RssFabryPerotMode } from "../../../../types/rss";

@Component({
  selector: "wm-fabry-perot",
  templateUrl: "./fabry-perot.component.html",
  styleUrls: ["./fabry-perot.component.scss"],
})
export class FabryPerotComponent {
  @Input() filter!: string;
  @Input() mode!: RssFabryPerotMode;
}
