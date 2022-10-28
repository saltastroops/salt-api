import { Component, Input, OnInit } from "@angular/core";
import { UntypedFormControl } from "@angular/forms";

import { parseISO } from "date-fns";

import { GeneralProposalInfo } from "../../../types/proposal";

@Component({
  selector: "wm-general-proposal-info",
  templateUrl: "./general-proposal-info.component.html",
  styleUrls: ["./general-proposal-info.component.scss"],
})
export class GeneralProposalInfoComponent implements OnInit {
  @Input() generalProposalInfo!: GeneralProposalInfo;
  @Input() currentSemester!: string;
  @Input() phase!: number;
  @Input() proposalCode!: string;
  semesterControl = new UntypedFormControl();
  currentSubmission!: Date;
  firstSubmission!: Date;
  statusDescription = "";
  backgroundColor = "";

  ngOnInit(): void {
    this.currentSubmission = parseISO(
      this.generalProposalInfo.currentSubmission,
    );
    this.firstSubmission = parseISO(this.generalProposalInfo.firstSubmission);
    this.semesterControl.setValue(this.currentSemester);

    const status = this.generalProposalInfo.status.value;

    switch (status) {
      case "Active":
        this.statusDescription =
          "This proposal has been added to the queue to be observed.";
        this.backgroundColor = "is-green-background";
        break;

      case "Accepted":
        this.statusDescription = "This proposal has been accepted.";
        this.backgroundColor = "is-green-background";
        break;

      case "Completed":
        this.statusDescription = "This proposal has been completed.";
        this.backgroundColor = "is-green-background";
        break;

      case "Deleted":
        this.statusDescription = "This proposal has been deleted.";
        this.backgroundColor = "is-red-background";
        break;

      case "Expired":
        this.statusDescription = "This proposal has expired.";
        this.backgroundColor = "is-red-background";
        break;

      case "Inactive":
        this.statusDescription = "This proposal is inactive.";
        this.backgroundColor = "is-red-background";
        break;

      case "Superseded":
        this.statusDescription = "This proposal has been superseded.";
        this.backgroundColor = "is-red-background";
        break;

      case "Under technical review":
        this.statusDescription = "This proposal is under technical review.";
        this.backgroundColor = "is-red-background";
        break;

      case "Under scientific review":
        this.statusDescription = "This proposal is under scientific review.";
        this.backgroundColor = "is-red-background";
        break;
    }
  }
}
