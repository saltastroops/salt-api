import { Component, EventEmitter, Input, OnInit, Output } from "@angular/core";
import {
  AbstractControl,
  UntypedFormArray,
  UntypedFormBuilder,
  UntypedFormGroup,
  Validators,
} from "@angular/forms";

import { ProposalService } from "../../../../service/proposal.service";
import { Proposal, ProposalProgress } from "../../../../types/proposal";
import { getNextSemester } from "../../../../util";
import { GENERIC_ERROR_MESSAGE, currentSemester } from "../../../../utils";

@Component({
  selector: "wm-progress-request-form",
  templateUrl: "./progress-request-form.component.html",
  styleUrls: ["./progress-request-form.component.scss"],
})
export class ProgressRequestFormComponent implements OnInit {
  @Input() progressReport!: ProposalProgress;
  @Input() proposal!: Proposal;
  @Output() successfulSubmission: EventEmitter<ProposalProgress> =
    new EventEmitter();

  proposalProgressForm!: UntypedFormGroup;
  loading = false;
  submitted = false;
  error?: string = undefined;
  success?: string = undefined;
  currentSemester = currentSemester();
  nextSemester = getNextSemester();
  changeReasonError = false;
  file: File | null = null;
  wrongFileType = false;

  constructor(
    private formBuilder: UntypedFormBuilder,
    private proposalService: ProposalService,
  ) {}

  ngOnInit(): void {
    const requestedPercentageGroups: UntypedFormGroup[] =
      this.progressReport.partnerRequestedPercentages.map((p) =>
        this.createPartnerRequestedPercentages(
          p.partnerCode,
          p.requestedPercentage,
        ),
      );
    this.proposalProgressForm = this.formBuilder.group({
      additionalPdf: [""],
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
    this.loading = true;
    this.submitted = true;
    this.success = undefined;
    this.validatePartnerRequestedPercentagesControls();

    // stop here if form is invalid
    if (this.proposalProgressForm.invalid) {
      this.error =
        "Please make sure that all required fields are filled correctly.";
      this.loading = false;
      return;
    }
    this.error = undefined;
    // We use getRawValue() rather than just the value property, as the input field for
    // the percentage requested from partner OTH (if there is one) is disabled, but we
    // still need its value.
    const proposalProgressFormValues = this.proposalProgressForm.getRawValue();
    const partnerRequestedPercentages =
      proposalProgressFormValues.partnerRequestedPercentages
        .map(
          (rp: { requestedPercentage: string; partnerCode: string }) =>
            rp.partnerCode + ":" + rp.requestedPercentage,
        )
        .join(";");

    const formData: FormData = new FormData();

    formData.append("requested_time", proposalProgressFormValues.requestedTime);
    formData.append("maximum_seeing", proposalProgressFormValues.maximumSeeing);
    formData.append("transparency", proposalProgressFormValues.transparency);
    formData.append(
      "description_of_observing_constraints",
      proposalProgressFormValues.descriptionOfObservingConstraints,
    );
    formData.append("change_reason", proposalProgressFormValues.changeReason);
    formData.append(
      "summary_of_proposal_status",
      proposalProgressFormValues.summaryOfProposalStatus,
    );
    formData.append(
      "strategy_changes",
      proposalProgressFormValues.strategyChanges,
    );
    formData.append(
      "partner_requested_percentages",
      partnerRequestedPercentages,
    );

    this.proposalService
      .putProgressReport(
        this.proposal.proposalCode,
        this.currentSemester,
        formData,
        this.file,
      )
      .subscribe(
        (data) => {
          this.progressReport = { ...data };
          this.loading = false;
          this.success = "The progress report has been submitted.";
          this.successfulSubmission.emit(data);

          setTimeout(() => {
            this.success = undefined;
          }, 3000);
        },
        () => {
          this.error = GENERIC_ERROR_MESSAGE;
          this.loading = false;
        },
      );

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
    this.validateAttachedFile(files);
    if (files) {
      this.file = files.item(0);
      this.proposalProgressForm.patchValue({
        additionalPdf: files.item(0),
      });
    }
  }

  removeFile(): void {
    this.file = null;
    this.proposalProgressForm.patchValue({
      additionalPdf: null,
    });
    this.f.additionalPdf.setErrors(null);
  }

  validatePartnerRequestedPercentagesControls(): void {
    let totalRequestedPercentage = 0;
    this.partnerRequestedPercentages?.controls.forEach((p) => {
      totalRequestedPercentage += Number(p.value.requestedPercentage) || 0;
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
        ?.get("requestedPercentage")
        ?.setErrors({
          message: `The requested percentage for the partner ${partnerCode} should be between 0 and 100`,
        });
    }
  }

  validateAttachedFile(files: FileList | null): void {
    if (files?.item(0)?.type != "application/pdf") {
      this.f.additionalPdf.setErrors({
        message: "The additional PDF can only be of type PDF.",
      });
    }
  }

  createPartnerRequestedPercentages(
    partnerCode: string,
    requestedPercentage: number,
  ): UntypedFormGroup {
    return this.formBuilder.group({
      partnerCode: [partnerCode, Validators.required],
      requestedPercentage: [
        // "readonly" would be more appropriate than "disabled", but this property is
        // not supported by Angular Forms.
        { value: `${requestedPercentage}`, disabled: partnerCode === "OTH" },
        Validators.required,
      ],
    });
  }

  get partnerRequestedPercentages(): UntypedFormArray {
    return <UntypedFormArray>(
      this.proposalProgressForm.get("partnerRequestedPercentages")
    );
  }
}
