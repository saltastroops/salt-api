import { Component, Input, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { GeneralProposalInfo, Semester } from '../../types';

@Component({
  selector: 'wm-general-proposal-info',
  templateUrl: './general-proposal-info.component.html',
  styleUrls: ['./general-proposal-info.component.scss'],
})
export class GeneralProposalInfoComponent implements OnInit {
  @Input() general_proposal_info!: GeneralProposalInfo;
  @Input() currentSemester!: Semester;
  semesterControl = new FormControl();
  constructor() {}

  ngOnInit(): void {
    // Select the current semester.
    // It is not possible to just pass this.currentSemester, as (while it may share the
    // year and semester with an item) it is not equal to any of the items in the
    // semesters array.
    this.semesterControl.setValue(
      this.general_proposal_info.semesters.find(
        (s) =>
          this.currentSemester.year === s.year &&
          this.currentSemester.semester === s.semester
      )
    );
  }
}
