import { Component, OnInit } from "@angular/core";
import {
  AbstractControl,
  UntypedFormBuilder,
  UntypedFormGroup,
  ValidationErrors,
  ValidatorFn,
  Validators,
} from "@angular/forms";

import { Observable, Subject, of } from "rxjs";
import { catchError, debounceTime, switchMap, take, tap } from "rxjs/operators";

import { AuthenticationService } from "../service/authentication.service";
import { InstitutionService } from "../service/institution.service";
import { UserService } from "../service/user.service";
import { Partner } from "../types/common";
import { Institution } from "../types/institution";
import { StatisticsError, User, UserListItem, UserUpdate } from "../types/user";
import { AutoUnsubscribe } from "../utils";

@AutoUnsubscribe()
@Component({
  selector: "wm-manage-user-profile",
  templateUrl: "./manage-user-profile.component.html",
  styleUrls: ["./manage-user-profile.component.scss"],
})
export class ManageUserProfileComponent implements OnInit {
  public Partner = Partner;
  user$!: Observable<User>;
  selectedUser!: User;
  selectedUserId$: Subject<number> = new Subject<number>();
  users!: UserListItem[];
  partners!: Array<keyof typeof Partner>;
  partnerInstitutions!: Institution[];
  institutionsMapping = new Map();
  userProfile!: UntypedFormGroup;
  isLoadingForm = false;
  showForm = true;
  error?: string;
  statisticsError: StatisticsError = {
    legalStatus: undefined,
    race: undefined,
    gender: undefined,
    phd: undefined,
  };

  loading = false;

  // cross-validation to ensure that password has the required
  // character length, and matches the confirm password value
  passwordValidators: ValidatorFn = (
    control: AbstractControl,
  ): ValidationErrors | null => {
    const password = control.get("password");
    const confirmPassword = control.get("confirmPassword");

    const errors: { [key: string]: boolean } = {};
    if (
      password?.value !== null &&
      password?.value !== "" &&
      password?.value?.length < 6
    ) {
      errors.minLength = true;
    }

    if (password?.value !== confirmPassword?.value) {
      errors.notMatched = true;
    }

    return Object.keys(errors).length > 0 ? errors : null;
  };

  constructor(
    private authService: AuthenticationService,
    private userService: UserService,
    private institutionService: InstitutionService,
    private formBuilder: UntypedFormBuilder,
  ) {}

  ngOnInit(): void {
    this.userProfile = this.formBuilder.group(
      {
        givenName: ["", Validators.required],
        familyName: ["", Validators.required],
        partner: [null],
        institutionName: [null],
        email: ["", [Validators.required, Validators.email]],
        password: [null],
        confirmPassword: [null],
        legalStatus: ["", Validators.required],
        gender: [null],
        race: [null],
        phdYear: [null],
        hasPhd: [null],
      },
      {
        validators: [this.passwordValidators],
      },
    );

    this.userProfile.get("partner")?.disable();
    this.userProfile.get("institutionName")?.disable();

    this.user$ = this.authService.getUser().pipe(
      tap((user) => {
        this.selectedUserId$.next(user.id);
      }),
    );
    this.user$
      .pipe(
        tap((user) => user),
        switchMap((user) => {
          if (user.roles.includes("Administrator")) {
            return this.userService.getUsers().pipe(take(1));
          }
          return of([]);
        }),
      )
      .subscribe((users) => {
        this.users = users;
      });
    this.selectedUserId$
      .pipe(
        debounceTime(100),
        switchMap((user_id) => {
          return this.userService.getUserById(user_id);
        }),
        catchError(() => {
          window.alert("Failed to fetch user.");
          this.isLoadingForm = false;
          return of(null);
        }),
      )
      .subscribe((user) => {
        if (user) {
          this.selectedUser = user;
          this.userProfile.patchValue(user);
          this.userProfile.patchValue({
            partner:
              Partner[user.affiliations[0].partnerCode as keyof typeof Partner],
            institutionName: user.affiliations[0].name,
          });
          this.isLoadingForm = false;
          this.partnerInstitutions = this.filterInstitutions();
        } else {
          this.showForm = false;
          this.error = "Not logged in.";
        }
      });
    this.institutionService
      .getInstitutions()
      .pipe(take(1))
      .subscribe((institutions) => {
        this.institutionsMapping = new Map<string, Institution[]>();
        for (const institution of institutions) {
          const partnerCode = institution.partnerCode;
          if (this.institutionsMapping.has(partnerCode)) {
            this.institutionsMapping.get(partnerCode).push(institution);
          } else {
            this.institutionsMapping.set(partnerCode, [institution]);
          }
        }
        const partners = Array.from(this.institutionsMapping.keys()).map(
          (partnerCode: keyof typeof Partner) => Partner[partnerCode],
        );

        // move "Other" partner to the end of an array
        partners.sort();
        partners.push(
          partners.splice(partners.indexOf("Other" as Partner), 1)[0],
        );
        this.partners = partners.map(
          (partner) =>
            Object.keys(Partner)[
              Object.values(Partner).indexOf(partner)
            ] as keyof typeof Partner,
        );
      });
  }

  get f(): { [key: string]: AbstractControl } {
    return this.userProfile.controls;
  }

  filterInstitutions(): Institution[] {
    const partnerCode = this.selectedPartnerCode;
    if (partnerCode) {
      return this.institutionsMapping.get(partnerCode);
    }
    return [];
  }

  get selectedUserId(): number | null {
    return this.selectedUser ? this.selectedUser.id : null;
  }

  onSelectUser(event: Event): void {
    const userId = parseInt((event.target as HTMLSelectElement).value, 10);
    this.isLoadingForm = true;
    this.selectUser(userId);
  }

  onSelectPartner(event: Event): void {
    const partner = (event.target as HTMLSelectElement).value as Partner;
    const partnerCode =
      Object.keys(Partner)[Object.values(Partner).indexOf(partner)];
    this.partnerInstitutions = this.institutionsMapping.get(partnerCode);
    this.userProfile.patchValue({
      partner: partner,
      institutionName: this.partnerInstitutions[0].name,
    });
  }

  selectUser(user_id: number): void {
    this.selectedUserId$.next(user_id);
  }

  get selectedPartnerCode(): string | null {
    if (this.selectedUser) {
      return this.selectedUser.affiliations[0]
        .partnerCode as keyof typeof Partner;
    } else {
      return null;
    }
  }

  get selectedInstitution(): string | null {
    return this.selectedUser ? this.selectedUser.affiliations[0].name : null;
  }

  institutionString(institution: Institution): string {
    if (institution.department && institution.department !== " ") {
      return institution.name + " (" + institution.department + ")";
    }
    return institution.name;
  }

  validateStatistics(): void {
    if (this.userProfile.value.legalStatus === null) {
      return;
    }
    if (!this.userProfile.value.legalStatus) {
      this.statisticsError.legalStatus =
        "Your legal status in South Africa is required";
    }
    if (
      this.userProfile.value.legalStatus === "South African citizen" ||
      this.userProfile.value.legalStatus ===
        "Permanent resident of South Africa"
    ) {
      if (this.userProfile.value.gender === null) {
        this.statisticsError.gender = "Gender is required.";
      }
      if (this.userProfile.value.race === null) {
        this.statisticsError.race = "Race is required.";
      }
      if (this.userProfile.value.hasPhd === null) {
        this.statisticsError.phd = "PhD status is required.";
      }

      if (this.userProfile.value.hasPhd && !this.userProfile.value.phdYear) {
        this.statisticsError.phd = "PhD year of completion is required.";
      }
    }
  }

  submit(): void {
    this.validateStatistics();

    if (this.userProfile.valid) {
      this.loading = true;

      const userUpdate = {
        givenName: this.userProfile.get("givenName")?.value,
        familyName: this.userProfile.get("familyName")?.value,
        password: this.userProfile.get("password")?.value,
        email: this.userProfile.get("email")?.value,
        legalStatus: this.userProfile.get("legalStatus")?.value,
        gender: this.userProfile.get("gender")?.value,
        race: this.userProfile.get("race")?.value,
        hasPhd: this.userProfile.get("hasPhd")?.value,
        yearOfPhdCompletion: this.userProfile.get("phdYear")?.value,
      } as UserUpdate;

      this.userService
        .updateUser(this.selectedUser.id, userUpdate)
        .pipe(
          catchError((err) => {
            this.error = err.message;
            this.loading = false;
            return of(null);
          }),
        )
        .subscribe((user) => {
          if (user) {
            window.alert("User details successfully updated.");
            const updatedUser = this.users.find((u) => u.givenName === user.givenName && u.familyName === user.familyName);
            if (updatedUser) {
              this.selectedUserId$.next(updatedUser.id);
            }
            this.loading = false;
          }
        });
    }
  }

  onGivenNameChange(name: string): void {
    this.userProfile.get("givenName")?.patchValue(name);
  }

  onFamilyNameChange(surname: string): void {
    this.userProfile.get("familyName")?.patchValue(surname);
  }

  onEmailChange(email: string): void {
    this.userProfile.get("email")?.patchValue(email);
  }
}
