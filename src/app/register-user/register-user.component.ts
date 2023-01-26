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

import { Observable, iif, interval, of } from "rxjs";
import {
  catchError,
  map,
  mergeMap,
  switchMap,
  take,
  tap,
} from "rxjs/operators";

import { InstitutionService } from "../service/institution.service";
import { UserService } from "../service/user.service";
import { Partner, PartnerCode } from "../types/common";
import { Institution, NewInstitutionDetails } from "../types/institution";
import { NewUserDetails } from "../types/user";

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
  selectedInstitutionId!: number;
  institutionId$!: Observable<number>;
  DEBOUNCE_TIME = 100;

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
        password: ["", Validators.required, Validators.minLength(6)],
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
      },
      { validators: this.passwordMatchingValidator },
    );
    this.setInstitutionValidators();
  }

  // convenience getter for easy access to form fields
  get f(): { [key: string]: AbstractControl } {
    return this.registerNewUserForm.controls;
  }

  registerNewUser(): void {
    this.registerNewUserForm.markAllAsTouched();

    // stop here if form is invalid
    if (this.registerNewUserForm.invalid) {
      return;
    }

    this.loading = true;

    const newInstitution = {
      institutionName: this.registerNewUserForm.get("institutionName")?.value,
      department: this.registerNewUserForm.get("department")?.value,
      address: this.registerNewUserForm.get("address")?.value,
      url: this.registerNewUserForm.get("url")?.value,
    } as NewInstitutionDetails;

    const newInstitutionId$ = this.institutionService
      .createInstitution(newInstitution)
      .pipe(map((institution) => institution.institutionId));

    const institutionId$ = interval(1000).pipe(
      mergeMap(() =>
        iif(
          () => this.showAddNewInstitutionControls,
          newInstitutionId$,
          of(parseInt(this.registerNewUserForm.get("institutionId")?.value)),
        ),
      ),
    );

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
            institutionId: this.registerNewUserForm.get("institutionId")?.value,
          } as NewUserDetails;

          return this.userService.createUser(user);
        }),
        catchError((err) => {
          this.error = err.message;
          this.loading = false;
          return of(null);
        }),
      )
      .subscribe((user) => {
        if (user) {
          window.alert(
            "You have successfully registered.\nYou may to proceed to log in.",
          );
          this.loading = false;
        }
      });
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

  setInstitutionValidators(): void {
    // Some institution fields are only validated if the user selects "Other" partner,
    // and "ADD NEW INSTITUTION" option from institutions list.
    const institutionNameControl =
      this.registerNewUserForm.get("institutionName");
    const institutionDepartmentControl =
      this.registerNewUserForm.get("department");
    const institutionUrlControl = this.registerNewUserForm.get("url");
    const institutionAddressControl = this.registerNewUserForm.get("address");

    // Use our control and subscribe institutionId value changes
    this.registerNewUserForm
      .get("institutionId")
      ?.valueChanges.subscribe((value) => {
        // If "ADD NEW INSTITUTION" option is selected validate controls
        if (value === "0") {
          institutionNameControl?.setValidators([Validators.required]);
          institutionDepartmentControl?.setValidators([Validators.required]);
          institutionUrlControl?.setValidators([Validators.required]);
          institutionAddressControl?.setValidators([Validators.required]);
        }
        // Update the form validity
        institutionNameControl?.updateValueAndValidity();
        institutionDepartmentControl?.updateValueAndValidity();
        institutionUrlControl?.updateValueAndValidity();
        institutionAddressControl?.updateValueAndValidity();
      });
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
}
