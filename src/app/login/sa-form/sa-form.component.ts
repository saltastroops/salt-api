import { Component, Input, OnInit } from "@angular/core";
import {
  FormGroup,
  UntypedFormBuilder,
  UntypedFormControl,
} from "@angular/forms";

import { StatisticsError } from "../../types/user";

@Component({
  selector: "wm-sa-form",
  templateUrl: "./sa-form.component.html",
  styleUrls: ["./sa-form.component.scss"],
})
export class SaFormComponent implements OnInit {
  @Input() userDetailsForm!: FormGroup;
  @Input() error!: StatisticsError;
  phdYearControl = new UntypedFormControl();
  collect = false;
  isSelfDefinedGender: boolean | undefined = undefined;
  isTypePhdYear = false;
  years = [...Array(101).keys()].map((i) => new Date().getFullYear() - 100 + i);

  constructor(private formBuilder: UntypedFormBuilder) {}
  ngOnInit(): void {
    console.log(this.userDetailsForm);
  }

  collectMoreDetails(collect: boolean, legalStatus: string): void {
    this.collect = collect;
    this.setLegalStatus(legalStatus);
    if (legalStatus === "Other") {
      this.setGender("");
      this.setRace("");
      this.setPhdYear("");
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
    this.userDetailsForm.patchValue({ phdYear });
  }

  hasPhd(isPhd: boolean): void {
    this.isTypePhdYear = isPhd;
    this.phdYearControl.setValue(null);
    this.userDetailsForm.patchValue({ hasPhd: isPhd });
  }

  typeDefinedGender(isSelfDefined: boolean): void {
    this.isSelfDefinedGender = isSelfDefined;
  }
}
