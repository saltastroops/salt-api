import { Component, OnInit } from "@angular/core";
import { FormBuilder, FormGroup, Validators } from "@angular/forms";
import { ActivatedRoute } from "@angular/router";

import { Observable, Subject, of } from "rxjs";
import { catchError, debounceTime, switchMap, take, tap } from "rxjs/operators";

import { AuthenticationService } from "../service/authentication.service";
import { InstitutionService } from "../service/institution.service";
import { UserService } from "../service/user.service";
import { Partner } from "../types/common";
import { Institution } from "../types/institution";
import { User, UserListItem } from "../types/user";

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
  userProfile!: FormGroup;
  isLoadingForm = false;
  showForm = true;
  error?: string;

  constructor(
    private authService: AuthenticationService,
    private activatedRoute: ActivatedRoute,
    private userService: UserService,
    private institutionService: InstitutionService,
    private formBuilder: FormBuilder,
  ) {}

  ngOnInit(): void {
    this.userProfile = this.formBuilder.group({
      givenName: ["", Validators.required],
      familyName: ["", Validators.required],
      partner: [null, Validators.required],
      institutionName: [null, Validators.required],
      email: ["", [Validators.required, Validators.email]],
      password: [null],
      retypePassword: [null],
    });
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
        catchError((err) => {
          window.alert(err);
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
}
