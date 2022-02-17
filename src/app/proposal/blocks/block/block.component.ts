import { Component, Input } from "@angular/core";

import { Block } from "../../../types/block";

@Component({
  selector: "wm-block",
  templateUrl: "./block.component.html",
  styleUrls: ["./block.component.scss"],
})
export class BlockComponent {
  @Input() block!: Block;
}
