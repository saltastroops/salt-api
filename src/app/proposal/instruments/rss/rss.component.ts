import { Component, Input } from "@angular/core";

import { PayloadConfiguration } from "../../../types/observation";
import { Rss } from "../../../types/rss";

@Component({
  selector: "wm-rss",
  templateUrl: "./rss.component.html",
  styleUrls: ["./rss.component.scss"],
})
export class RssComponent {
  @Input() rss!: Rss;
  @Input() payloadConfiguration!: PayloadConfiguration;
  headerLine: string | null = null;
}
