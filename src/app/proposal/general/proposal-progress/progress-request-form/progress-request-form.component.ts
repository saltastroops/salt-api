import { Component, Input, OnInit } from "@angular/core";
import {
  AbstractControl,
  FormArray,
  FormBuilder,
  FormGroup,
  Validators,
} from "@angular/forms";

import { ProposalProgress } from "../../../../types/proposal";
import { getNextSemester } from "../../../../util";

@Component({
  selector: "wm-progress-request-form",
  templateUrl: "./progress-request-form.component.html",
  styleUrls: ["./progress-request-form.component.scss"],
})
export class ProgressRequestFormComponent implements OnInit {
  @Input() progressReport!: ProposalProgress;

  proposalProgressForm!: FormGroup;
  loading = false;
  submitted = false;
  error: string | undefined = undefined;
  nextSemester = getNextSemester();
  changeReasonError = false;
  file: File | null = null;
  wrongFileType = false;

  constructor(private formBuilder: FormBuilder) {}

  ngOnInit(): void {
    const requestedPercentageGroups: FormGroup[] =
      this.progressReport.partnerRequestedPercentages.map((p) =>
        this.createPartnerRequestedPercentages(
          p.partnerCode,
          p.requestedPercentage,
        ),
      );
    this.proposalProgressForm = this.formBuilder.group({
      requestedTime: ["", Validators.required],
      maximumSeeing: ["", Validators.required],
      transparency: ["", Validators.required],
      descriptionOfObservingConstraints: ["", Validators.required],
      changeReason: ["", Validators.required],
      summaryOfProposalStatus: ["", Validators.required],
      strategyChanges: ["", Validators.required],
      partnerRequestedPercentages: this.formBuilder.array(
        requestedPercentageGroups,
        Validators.required,
      ),
    });

    this.f.transparency.setValue(this.progressReport.transparency || "");
    if (this.progressReport) {
      this.f.requestedTime.setValue(this.progressReport.requestedTime);
      this.f.maximumSeeing.setValue(this.progressReport.maximumSeeing);
      this.f.descriptionOfObservingConstraints.setValue(
        this.progressReport.descriptionOfObservingConstraints,
      );
      this.f.changeReason.setValue(this.progressReport.changeReason);
      this.f.summaryOfProposalStatus.setValue(
        this.progressReport.summaryOfProposalStatus,
      );
      this.f.strategyChanges.setValue(this.progressReport.strategyChanges);
    }
  }

  // convenience getter for easy access to form fields
  get f(): { [key: string]: AbstractControl } {
    return this.proposalProgressForm.controls;
  }

  submit(): void {
    this.submitted = true;
    this.validatePartnerRequestedPercentagesControls();

    // stop here if form is invalid
    if (this.proposalProgressForm.invalid) {
      this.error = "Please make sure that all required fields are filled.";
      return;
    }
    this.error = undefined;

    this.loading = false;
    //TODO under development do not submit the form. Error for network will be added
    return;
  }

  clearError(): void {
    this.error = undefined;
  }

  changeTransparency(e: Event): void {
    this.f.transparency.setValue((e.target as HTMLSelectElement).value, {
      onlySelf: true,
    });
  }

  onFileInput(files: FileList | null): void {
    if (files) {
      this.file = files.item(0);
    }
    this.wrongFileType = this.file?.type !== "application/pdf";
  }

  removeFile(): void {
    this.file = null;
    this.wrongFileType = false;
  }

  validatePartnerRequestedPercentagesControls(): void {
    let totalRequestedPercentage = 0;
    this.partnerRequestedPercentages?.controls.forEach((p) => {
      totalRequestedPercentage += Number(p.value.requestedPercentages) || 0;
    });
    if (
      totalRequestedPercentage > 100.0001 ||
      totalRequestedPercentage < 99.9999
    ) {
      this.partnerRequestedPercentages?.setErrors({
        message: "The percentages for the partners have to add up to 100.",
      });
    }
  }

  validateRequestedTimeValue(value: string): void {
    if (isNaN(Number(value)) || Number(value) < 0) {
      this.f.maximumSeeing.setErrors({
        message: "The requested amount should be a non-negative number.",
      });
    }
  }

  validateMaximumSeeingValue(value: string): void {
    if (isNaN(Number(value)) || Number(value) < 0 || Number(value) > 9) {
      this.f.maximumSeeing.setErrors({
        message: "This maximum seeing value should a number between 0 and 9.",
      });
    }
  }

  validatePercentageValue(value: string, partnerCode: string, i: number): void {
    if (isNaN(Number(value)) || Number(value) < 0 || Number(value) > 100) {
      this.partnerRequestedPercentages?.controls[i]
        ?.get("requestedPercentages")
        ?.setErrors({
          message: `The requested percentage for the partner ${partnerCode} should be between 0 and 100`,
        });
    }
  }

  createPartnerRequestedPercentages(
    partnerCode: string,
    requestedPercentage: number,
  ): FormGroup {
    return this.formBuilder.group({
      partnerCode: [partnerCode, Validators.required],
      requestedPercentages: [
        { value: `${requestedPercentage}`, disabled: partnerCode === "OTH" },
        Validators.required,
      ],
    });
  }

  get partnerRequestedPercentages(): FormArray {
    return <FormArray>(
      this.proposalProgressForm.get("partnerRequestedPercentages")
    );
  }
}
