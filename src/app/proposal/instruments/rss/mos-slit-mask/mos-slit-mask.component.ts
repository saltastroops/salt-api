import { Component, Input, OnInit } from "@angular/core";

import { parseISO } from "date-fns";

import { RssMosMask } from "../../../../types/rss";

@Component({
  selector: "wm-mos-slit-mask",
  templateUrl: "./mos-slit-mask.component.html",
  styleUrls: ["./mos-slit-mask.component.scss"],
})
export class MosSlitMaskComponent implements OnInit {
  @Input() mosSlitMask!: RssMosMask;

  cutDate!: Date | null;

  ngOnInit(): void {
    this.cutDate = this.mosSlitMask.cutDate
      ? parseISO(this.mosSlitMask.cutDate)
      : null;
  }
}
