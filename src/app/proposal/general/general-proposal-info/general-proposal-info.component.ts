import { Component, EventEmitter, Input, OnInit, Output } from "@angular/core";
import { UntypedFormControl } from "@angular/forms";

import { parseISO } from "date-fns";

import {
  Investigator,
  Proposal,
  ProposalStatusValue,
} from "../../../types/proposal";

@Component({
  selector: "wm-general-proposal-info",
  templateUrl: "./general-proposal-info.component.html",
  styleUrls: ["./general-proposal-info.component.scss"],
})
export class GeneralProposalInfoComponent implements OnInit {
  @Input() proposal!: Proposal;
  @Input() isLoading!: boolean;
  @Output() selectSemester = new EventEmitter<string>();
  semesterControl = new UntypedFormControl();

  ngOnInit(): void {
    this.semesterControl.setValue(this.proposal.semester);
  }
  onSemesterChange(): void {
    this.isLoading = true;
    this.selectSemester.emit(this.semesterControl.value);
  }

  backgroundColor(status: ProposalStatusValue): string {
    switch (status) {
      case "Active":
        return "has-background-success";

      case "Accepted":
        return "has-background-success";

      case "Completed":
        return "has-background-success";

      case "Deleted":
        return "has-background-danger";

      case "Expired":
        return "has-background-danger";

      case "Inactive":
        return "has-background-danger";

      case "Superseded":
        return "has-background-danger";

      case "Under technical review":
        return "has-background-danger";

      case "Under scientific review":
        return "has-background-danger";
    }
    return "";
  }
  statusDescription(status: ProposalStatusValue): string {
    switch (status) {
      case "Active":
        return "This proposal has been added to the queue to be observed.";

      case "Accepted":
        return "This proposal has been accepted.";

      case "Completed":
        return "This proposal has been completed.";

      case "Deleted":
        return "This proposal has been deleted.";

      case "Expired":
        return "This proposal has expired.";

      case "Inactive":
        return "This proposal is inactive.";

      case "Superseded":
        return "This proposal has been superseded.";

      case "Under technical review":
        return "This proposal is under technical review.";

      case "Under scientific review":
        return "This proposal is under scientific review.";
    }
    return "";
  }

  firstSubmission(): Date {
    return parseISO(this.proposal.generalInfo.firstSubmission);
  }

  currentSubmission(): Date {
    return parseISO(this.proposal.generalInfo.currentSubmission);
  }

  principalInvestigator(): Investigator | undefined {
    const investigators = this.proposal.investigators;
    return investigators.find((investigator) => investigator.isPi);
  }

  principalContact(): Investigator | undefined {
    const investigators = this.proposal.investigators;
    return investigators.find((investigator) => investigator.isPc);
  }
}
