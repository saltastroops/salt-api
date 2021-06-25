import { Component, Input, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { GeneralProposalInfo, Semester } from '../../types';

@Component({
  selector: 'wm-general-proposal-info',
  templateUrl: './general-proposal-info.component.html',
  styleUrls: ['./general-proposal-info.component.scss'],
})
export class GeneralProposalInfoComponent implements OnInit {
  @Input() generalProposalInfo!: GeneralProposalInfo;
  @Input() currentSemester!: Semester;
  semesterControl = new FormControl();
  constructor() {}

  ngOnInit(): void {
    this.semesterControl.setValue(
    // Select the current semester.
    // It is not possible to just pass this.currentSemester, as (while it may share the
    // year and semester with an item) it is not equal to any of the items in the
    // semesters array.
      this.generalProposalInfo.semesters.find(
        (s) =>
          this.currentSemester.year === s.year &&
          this.currentSemester.semester === s.semester
      )
    );
  }
}
