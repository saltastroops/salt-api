import { Component, Input, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { GeneralProposalInfo, Semester } from '../../types';
import { parseISO } from 'date-fns';

@Component({
  selector: 'wm-general-proposal-info',
  templateUrl: './general-proposal-info.component.html',
  styleUrls: ['./general-proposal-info.component.scss'],
})
export class GeneralProposalInfoComponent implements OnInit {
  @Input() generalProposalInfo!: GeneralProposalInfo;
  @Input() currentSemester!: string;
  @Input() phase!: number;
  @Input() proposalCode!: string;
  semesterControl = new FormControl();
  currentSubmission!: Date;
  firstSubmission!: Date;
  constructor() {}

  ngOnInit(): void {
    this.currentSubmission = parseISO(
      this.generalProposalInfo.currentSubmission
    );
    this.firstSubmission = parseISO(this.generalProposalInfo.firstSubmission);
    this.semesterControl.setValue(this.currentSemester);
  }
}
