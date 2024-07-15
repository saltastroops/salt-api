import { Component, OnInit } from "@angular/core";
import {
  AbstractControl,
  FormBuilder,
  FormGroup,
  ValidationErrors,
  ValidatorFn,
  Validators,
} from "@angular/forms";
import { ActivatedRoute, Router } from "@angular/router";

import { of } from "rxjs";
import { catchError, map, switchMap, take, tap } from "rxjs/operators";

import { InstitutionService } from "../service/institution.service";
import { UserService } from "../service/user.service";
import { Partner, PartnerCode } from "../types/common";
import { Institution, NewInstitutionDetails } from "../types/institution";
import { NewUserDetails, StatisticsError } from "../types/user";
import { GENERIC_ERROR_MESSAGE } from "../utils";

@Component({
  selector: "wm-register-user",
  templateUrl: "./register-user.component.html",
  styleUrls: ["./register-user.component.scss"],
})
export class RegisterUserComponent implements OnInit {
  registerNewUserForm!: FormGroup;
  loading = false;
  submitted = false;
  error: string | undefined = undefined;
  institutionsMapping = new Map();
  partners!: Partner[];
  partnerInstitutions!: Institution[];
  showAddNewInstitutionControls = false;
  statisticsError: StatisticsError = {
    legalStatus: undefined,
    race: undefined,
    gender: undefined,
    phd: undefined,
  };
  isRegistered = false;

  // cross-validation to ensure that password
  // and confirm password values match
  passwordMatchingValidator: ValidatorFn = (
    control: AbstractControl,
  ): ValidationErrors | null => {
    const password = control.get("password");
    const confirmPassword = control.get("confirmPassword");

    return password?.value === confirmPassword?.value
      ? null
      : { notMatched: true };
  };

  institutionValidator: ValidatorFn = (
    control: AbstractControl,
  ): ValidationErrors | null => {
    // Some institution fields are only validated if the user selects "Other" partner,
    // and "ADD NEW INSTITUTION" option from institutions list.
    const institutionIdControl = control.get("institutionId");
    const institutionNameControl = control.get("institutionName");
    const institutionDepartmentControl = control.get("department");
    const institutionAddressControl = control.get("address");
    const institutionURLControl = control.get("url");

    const errors: { [key: string]: boolean } = {};
    if (institutionIdControl?.value === "0") {
      if (
        institutionNameControl?.value === null ||
        institutionNameControl?.value.trim() === ""
      ) {
        errors.institutionNameRequired = true;
      }

      if (
        institutionDepartmentControl?.value === null ||
        institutionDepartmentControl?.value.trim() === ""
      ) {
        errors.institutionDepartmentRequired = true;
      }

      if (
        institutionAddressControl?.value === null ||
        institutionAddressControl?.value.trim() === ""
      ) {
        errors.institutionAddressRequired = true;
      }

      if (
        institutionURLControl?.value === null ||
        institutionURLControl?.value.trim() === ""
      ) {
        errors.institutionURLRequired = true;
      }
    }

    return Object.keys(errors).length > 0 ? errors : null;
  };

  constructor(
    private formBuilder: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private userService: UserService,
    private institutionService: InstitutionService,
  ) {}

  ngOnInit(): void {
    this.institutionService
      .getInstitutions()
      .pipe(take(1))
      .subscribe((institutions) => {
        this.partners = this.institutionsForPartners(institutions);
      });

    this.registerNewUserForm = this.formBuilder.group(
      {
        username: ["", Validators.required],
        password: ["", [Validators.required, Validators.minLength(6)]],
        confirmPassword: ["", Validators.required],
        givenName: ["", Validators.required],
        familyName: ["", Validators.required],
        email: ["", [Validators.required, Validators.email]],
        institutionId: [null, Validators.required],
        partner: [null, Validators.required],
        institutionName: [null],
        department: [null],
        url: [null],
        address: [null],
        legalStatus: [null, Validators.required],
        gender: [""],
        race: [""],
        phdYear: [""],
        hasPhd: [""],
      },
      {
        validators: [this.passwordMatchingValidator, this.institutionValidator],
      },
    );
  }

  // convenience getter for easy access to form fields
  get f(): { [key: string]: AbstractControl } {
    return this.registerNewUserForm.controls;
  }

  registerNewUser(): void {
    this.registerNewUserForm.markAllAsTouched();

    this.validateStatistics();

    // stop here if form is invalid
    if (this.registerNewUserForm.valid) {
      this.loading = true;

      const newInstitution = {
        institutionName: this.registerNewUserForm.get("institutionName")?.value,
        department: this.registerNewUserForm.get("department")?.value,
        address: this.registerNewUserForm.get("address")?.value,
        url: this.registerNewUserForm.get("url")?.value,
      } as NewInstitutionDetails;

      const institutionId$ =
        this.registerNewUserForm.get("institutionId")?.value != "0"
          ? of(parseInt(this.registerNewUserForm.get("institutionId")?.value))
          : this.institutionService
              .createInstitution(newInstitution)
              .pipe(map((institution) => institution.institutionId));

      institutionId$
        .pipe(
          tap((institutionId) =>
            this.registerNewUserForm.patchValue({
              institutionId: institutionId,
            }),
          ),
          switchMap(() => {
            const user = {
              username: this.registerNewUserForm.get("username")?.value,
              password: this.registerNewUserForm.get("password")?.value,
              email: this.registerNewUserForm.get("email")?.value,
              givenName: this.registerNewUserForm.get("givenName")?.value,
              familyName: this.registerNewUserForm.get("familyName")?.value,
              institutionId:
                this.registerNewUserForm.get("institutionId")?.value,
              legalStatus: this.registerNewUserForm.get("legalStatus")?.value,
              gender:
                this.registerNewUserForm.get("legalStatus")?.value === "Other"
                  ? null
                  : this.registerNewUserForm.get("gender")?.value,
              race:
                this.registerNewUserForm.get("legalStatus")?.value === "Other"
                  ? null
                  : this.registerNewUserForm.get("race")?.value,
              hasPhd:
                this.registerNewUserForm.get("legalStatus")?.value === "Other"
                  ? null
                  : this.registerNewUserForm.get("hasPhd")?.value,
              yearOfPhdCompletion:
                this.registerNewUserForm.get("legalStatus")?.value === "Other"
                  ? null
                  : this.registerNewUserForm.get("phdYear")?.value,
            } as NewUserDetails;
            return this.userService.createUser(user);
          }),
          catchError((err) => {
            this.error = err.message;
            this.loading = false;
            return of(null);
          }),
        )
        .subscribe(
          (user) => {
            if (user) {
              // If the server call fails with an error, the catchError above returns a stream with
              // a null user. In this case loading has stopped but no success message must be shown.
              this.isRegistered = true;
            }
            this.loading = false;
          },
          () => {
            this.loading = false;
            this.error = GENERIC_ERROR_MESSAGE;
          },
        );
    }
  }

  clearError(): void {
    this.error = undefined;
  }

  get selectedOtherPartner(): boolean {
    return this.showAddNewInstitutionControls;
  }

  onSelectPartner(partner: string): void {
    const selectedPartner = partner as Partner;
    // Show add new institution option if partner is "OTHER"
    this.showAddNewInstitutionControls = selectedPartner === Partner.OTH;
    const partnerCode =
      Object.keys(Partner)[Object.values(Partner).indexOf(selectedPartner)];
    this.partnerInstitutions = this.institutionsMapping.get(partnerCode);
  }

  institutionString(institution: Institution): string {
    if (institution.department && institution.department !== " ") {
      return institution.name + " (" + institution.department + ")";
    }
    return institution.name;
  }

  institutionsForPartners(institutions: Institution[]): Partner[] {
    this.institutionsMapping = new Map<PartnerCode, Institution[]>();
    for (const institution of institutions) {
      const partnerCode = institution.partnerCode;
      if (this.institutionsMapping.has(partnerCode)) {
        this.institutionsMapping.get(partnerCode).push(institution);
      } else {
        this.institutionsMapping.set(partnerCode, [institution]);
      }
    }
    const partners = Array.from(this.institutionsMapping.keys()).map(
      (partnerCode: PartnerCode) => Partner[partnerCode],
    );

    // move "Other" partner to the end of an array
    partners.sort();
    partners.push(partners.splice(partners.indexOf("Other" as Partner), 1)[0]);

    return partners;
  }
  validateStatistics(): void {
    if (this.registerNewUserForm.value.legalStatus === "") {
      return;
    }
    if (!this.registerNewUserForm.value.legalStatus) {
      this.statisticsError.legalStatus =
        "Your legal status in South Africa is required";
      this.registerNewUserForm.controls["legalStatus"].setErrors({
        incorrect: true,
      });
    }
    if (
      this.registerNewUserForm.value.legalStatus === "South African citizen" ||
      this.registerNewUserForm.value.legalStatus ===
        "Permanent resident of South Africa"
    ) {
      if (this.registerNewUserForm.value.gender === "") {
        this.statisticsError.gender = "Gender is required.";
        this.registerNewUserForm.controls["gender"].setErrors({
          incorrect: true,
        });
      }
      if (this.registerNewUserForm.value.race === "") {
        this.statisticsError.race = "Race is required.";
        this.registerNewUserForm.controls["race"].setErrors({
          incorrect: true,
        });
      }
      if (this.registerNewUserForm.value.hasPhd === "") {
        this.statisticsError.phd = "PhD status is required.";
        this.registerNewUserForm.controls["hasPhd"].setErrors({
          incorrect: true,
        });
      }

      if (
        this.registerNewUserForm.value.hasPhd &&
        !this.registerNewUserForm.value.phdYear
      ) {
        this.registerNewUserForm.controls["phdYear"].setErrors({
          incorrect: true,
        });
        this.statisticsError.phd = "Year of PhD completion is required.";
      }
    }
  }
}
