import { Component, Input } from "@angular/core";

import { Proposal } from "../../types/proposal";

@Component({
  selector: "wm-p1-details",
  templateUrl: "./p1-details.component.html",
  styleUrls: ["./p1-details.component.scss"],
})
export class P1DetailsComponent {
  @Input() proposal!: Proposal;
}
