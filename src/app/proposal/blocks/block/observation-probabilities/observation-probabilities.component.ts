import { Component, Input, OnInit } from "@angular/core";

import { Block } from "../../../../types/block";
import { ObservationProbabilities } from "../../../../types/common";

@Component({
  selector: "wm-observation-probabilities",
  templateUrl: "./observation-probabilities.component.html",
  styleUrls: ["./observation-probabilities.component.scss"],
})
export class ObservationProbabilitiesComponent implements  OnInit{
  @Input() block!: Block;
  probabilities!: ObservationProbabilities;

  ngOnInit(): void {
    this.probabilities = this.block.observationProbabilities;
  }
}
