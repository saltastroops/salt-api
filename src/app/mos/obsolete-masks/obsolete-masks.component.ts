import { Component, OnInit } from "@angular/core";

import { Observable } from "rxjs";

import { MosService } from "../../service/mos.service";
import { currentSemester } from "../../utils";

@Component({
  selector: "wm-obsolete-masks",
  templateUrl: "./obsolete-masks.component.html",
  styleUrls: ["./obsolete-masks.component.scss"],
})
export class ObsoleteMasksComponent implements OnInit {
  obsoleteMasks!: Observable<string[]>;
  selectedSemester: string =
    sessionStorage.getItem("mosSelectedSemester") || currentSemester();

  constructor(private mosService: MosService) {}

  ngOnInit(): void {
    this.obsoleteMasks = this.mosService.getObsoleteRssMasks();
  }
}
