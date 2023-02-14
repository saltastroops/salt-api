import { Component, Input, OnInit } from "@angular/core";
import { UntypedFormControl } from "@angular/forms";

import { parseISO } from "date-fns";

import { Investigator, Proposal } from "../../../types/proposal";

@Component({
  selector: "wm-general-proposal-info",
  templateUrl: "./general-proposal-info.component.html",
  styleUrls: ["./general-proposal-info.component.scss"],
})
export class GeneralProposalInfoComponent implements OnInit {
  @Input() proposal!: Proposal;
  semesterControl = new UntypedFormControl();
  currentSubmission!: Date;
  firstSubmission!: Date;
  statusDescription = "";
  backgroundColor = "";
  principalInvestigator: Investigator | undefined;
  principalContact: Investigator | undefined;

  ngOnInit(): void {
    this.currentSubmission = parseISO(
      this.proposal.generalInfo.currentSubmission,
    );
    this.firstSubmission = parseISO(this.proposal.generalInfo.firstSubmission);

    const investigators = this.proposal.investigators;
    this.semesterControl.setValue(this.proposal.semester);

    this.principalContact = investigators.find(
      (investigator) => investigator.isPc,
    );
    this.principalInvestigator = investigators.find(
      (investigator) => investigator.isPi,
    );

    const status = this.proposal.generalInfo.status.value;

    switch (status) {
      case "Active":
        this.statusDescription =
          "This proposal has been added to the queue to be observed.";
        this.backgroundColor = "has-background-success";
        break;

      case "Accepted":
        this.statusDescription = "This proposal has been accepted.";
        this.backgroundColor = "has-background-success";
        break;

      case "Completed":
        this.statusDescription = "This proposal has been completed.";
        this.backgroundColor = "has-background-success";
        break;

      case "Deleted":
        this.statusDescription = "This proposal has been deleted.";
        this.backgroundColor = "has-background-danger";
        break;

      case "Expired":
        this.statusDescription = "This proposal has expired.";
        this.backgroundColor = "has-background-danger";
        break;

      case "Inactive":
        this.statusDescription = "This proposal is inactive.";
        this.backgroundColor = "has-background-danger";
        break;

      case "Superseded":
        this.statusDescription = "This proposal has been superseded.";
        this.backgroundColor = "has-background-danger";
        break;

      case "Under technical review":
        this.statusDescription = "This proposal is under technical review.";
        this.backgroundColor = "has-background-danger";
        break;

      case "Under scientific review":
        this.statusDescription = "This proposal is under scientific review.";
        this.backgroundColor = "has-background-danger";
        break;
    }
  }
}
