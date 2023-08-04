import { Component, Input } from "@angular/core";
import { AbstractControl, FormGroup, UntypedFormControl } from "@angular/forms";

import { StatisticsError } from "../../types/user";

@Component({
  selector: "wm-sa-form",
  templateUrl: "./sa-form.component.html",
  styleUrls: ["./sa-form.component.scss"],
})
export class SaFormComponent {
  @Input() userDetailsForm!: FormGroup;
  @Input() error!: StatisticsError;
  phdYearControl = new UntypedFormControl();
  collect = false;
  isSelfDefinedGender: boolean | undefined = undefined;
  isTypePhdYear = false;
  years = [...Array(101).keys()].map((i) => new Date().getFullYear() - 100 + i);

  get f(): { [key: string]: AbstractControl } {
    return this.userDetailsForm.controls;
  }

  collectMoreDetails(collect: boolean, legalStatus: string): void {
    this.collect = collect;
    this.setLegalStatus(legalStatus);
    if (legalStatus === "Other") {
      this.setGender(null);
      this.setRace(null);
      this.setPhdYear(null);
    }
  }

  setLegalStatus(legalStatus: string): void {
    this.userDetailsForm.patchValue({ legalStatus });
  }

  setGender(gender: string | null): void {
    this.userDetailsForm.patchValue({ gender });
  }

  setRace(race: string | null): void {
    this.userDetailsForm.patchValue({ race });
  }

  setPhdYear(phdYear: string | null): void {
    this.error.phd = undefined;
    this.userDetailsForm.patchValue({ phdYear });
  }

  hasPhd(isPhd: boolean): void {
    this.error.phd = undefined;
    this.isTypePhdYear = isPhd;
    this.phdYearControl.setValue(null);
    this.userDetailsForm.patchValue({ hasPhd: isPhd });
  }

  typeDefinedGender(isSelfDefined: boolean): void {
    this.isSelfDefinedGender = isSelfDefined;
  }

  clearError(name: "phd" | "race" | "gender" | "legalStatus"): void {
    this.error[name] = undefined;
  }
}
