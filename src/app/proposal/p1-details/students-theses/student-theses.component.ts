import { Component, Input, OnInit } from "@angular/core";

import { GeneralProposalInfo, Investigator } from "../../../types/proposal";

@Component({
  selector: "wm-student-theses",
  templateUrl: "./student-theses.component.html",
  styleUrls: ["./student-theses.component.scss"],
})
export class StudentThesesComponent implements OnInit {
  @Input() investigators: Investigator[] = [];
  @Input() generalInfo!: GeneralProposalInfo;
  thesisStudents: Investigator[] = [];
  isThesisProposal = false;

  ngOnInit(): void {
    this.thesisStudents = this.investigators.filter((i) => i.thesis);
    this.isThesisProposal = this.investigators.some((i) => i.thesis);
  }
}
