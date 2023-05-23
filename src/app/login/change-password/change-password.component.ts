import { Component, OnInit } from "@angular/core";
import {
  AbstractControl,
  UntypedFormBuilder,
  UntypedFormGroup,
  Validators,
} from "@angular/forms";
import { ActivatedRoute, Router } from "@angular/router";

import { AuthenticationService } from "../../service/authentication.service";

@Component({
  selector: "wm-change-password",
  templateUrl: "./change-password.component.html",
  styleUrls: ["./change-password.component.scss"],
})
export class ChangePasswordComponent implements OnInit {
  changePasswordForm!: UntypedFormGroup;
  token!: string;
  loading = false;
  submitted = false;
  error: string | undefined = undefined;

  constructor(
    private formBuilder: UntypedFormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private authenticationService: AuthenticationService,
  ) {}

  ngOnInit(): void {
    this.changePasswordForm = this.formBuilder.group({
      password: ["", Validators.required],
      retypedPassword: ["", Validators.required],
    });
    this.route.params.subscribe((params) => {
      this.token = params.token;
    });
  }

  // convenience getter for easy access to form fields
  get f(): { [key: string]: AbstractControl } {
    return this.changePasswordForm.controls;
  }

  changePassword(): void {
    this.submitted = true;

    // stop here if form is invalid
    if (this.changePasswordForm.invalid) {
      return;
    }
    if (this.f.password.value !== this.f.retypedPassword.value) {
      this.error = "Password mismatch.";
      return;
    }

    this.loading = true;
    this.authenticationService
      .changePassword(this.f.password.value, this.token)
      .subscribe(
        () => {
          this.loading = false;
          this.router.navigate(["/login"]);
        },
        (error) => {
          this.error = error.message;
          this.loading = false;
        },
      );
  }

  clearError(): void {
    this.error = undefined;
  }
}
