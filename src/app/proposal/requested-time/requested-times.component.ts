import { Component, Input, OnInit } from "@angular/core";

import { RequestedTime } from "../../types/proposal";

@Component({
  selector: "wm-requested-times",
  templateUrl: "./requested-times.component.html",
  styleUrls: ["./requested-times.component.scss"],
})
export class RequestedTimesComponent implements OnInit {
  @Input() requestedTimes!: RequestedTime[];
  semesterRequestedTimes: { [key: string]: RequestedTime } = {};
  selectedSemester: string | undefined = undefined;
  Object = Object; //Object is used in the template

  ngOnInit(): void {
    this.requestedTimes.forEach(() => {
      this.semesterRequestedTimes = this.requestedTimes.reduce(
        (o, r) => ({ ...o, [r.semester]: r }),
        {},
      );
    });
  }

  selectSemester(semester: string): void {
    if (this.selectedSemester === semester) {
      this.selectedSemester = undefined;
    } else {
      this.selectedSemester = semester;
    }
  }
}
