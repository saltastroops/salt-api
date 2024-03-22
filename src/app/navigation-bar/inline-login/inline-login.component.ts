import { Component, OnInit } from "@angular/core";
import {
  AbstractControl,
  UntypedFormBuilder,
  UntypedFormGroup,
  Validators,
} from "@angular/forms";
import { Router } from "@angular/router";

import { AuthenticationService } from "../../service/authentication.service";
import { GENERIC_ERROR_MESSAGE } from "../../utils";

@Component({
  selector: "wm-inline-login",
  templateUrl: "./inline-login.component.html",
  styleUrls: ["./inline-login.component.scss"],
})
export class InlineLoginComponent implements OnInit {
  loginForm!: UntypedFormGroup;
  loading = false;
  error: string | null = null;

  constructor(
    private formBuilder: UntypedFormBuilder,
    private authService: AuthenticationService,
    private router: Router,
  ) {}

  ngOnInit(): void {
    this.loginForm = this.formBuilder.group({
      username: ["", Validators.required],
      password: ["", Validators.required],
    });
  }

  // convenience getter for easy access to form fields
  get f(): { [key: string]: AbstractControl } {
    return this.loginForm.controls;
  }

  login(): void {
    if (this.f.username.errors?.required) {
      this.error = "The username is required.";
      return;
    }
    if (this.f.password.errors?.required) {
      this.error = "The password is required.";
      return;
    }

    this.loading = true;
    this.error = null;

    this.authService
      .login(this.f.username.value, this.f.password.value)
      .subscribe(
        () => {
          const redirection = this.authService.getRedirection();
          const redirectUrlParts =
            redirection && redirection.urlParts.length
              ? redirection.urlParts
              : ["/"];
          const redirectQueryParams = redirection
            ? redirection.queryParams
            : {};
          this.router.navigate(redirectUrlParts, {
            queryParams: redirectQueryParams,
          });
          this.loading = false;
        },
        (error: { status: number; error: string }) => {
          // The HTTP request for logging in is not intercepted, and hence there may be
          // an error response with status code 401.
          if (error.status === 401) {
            this.error = "Username or password is incorrect.";
          } else if (error.status === 403) {
            this.error = "Your account has not been verified.";
          } else {
            this.error = GENERIC_ERROR_MESSAGE;
          }
          this.loading = false;
        },
      );
  }
}
