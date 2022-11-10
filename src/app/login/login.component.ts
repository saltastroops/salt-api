import { Component, OnInit } from "@angular/core";
import {
  AbstractControl,
  UntypedFormBuilder,
  UntypedFormGroup,
  Validators,
} from "@angular/forms";
import { ActivatedRoute, Router } from "@angular/router";

import { AuthenticationService } from "../service/authentication.service";
import { GENERIC_ERROR_MESSAGE } from "../utils";

@Component({ templateUrl: "login.component.html" })
export class LoginComponent implements OnInit {
  loginForm!: UntypedFormGroup;
  loading = false;
  submitted = false;
  error: string | undefined = undefined;

  constructor(
    private formBuilder: UntypedFormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private authenticationService: AuthenticationService,
  ) {
    // redirect to home if already logged in
    if (this.authenticationService.isAuthenticated()) {
      window.alert("You are logged in already.");
      this.router.navigate(["/"]);
    }
  }

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
    this.submitted = true;

    // stop here if form is invalid
    if (this.loginForm.invalid) {
      return;
    }

    this.loading = true;
    this.authenticationService
      .login(this.f.username.value, this.f.password.value)
      .subscribe(
        () => {
          const redirection = this.authenticationService.getRedirection();
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
        },
        (error: { status: number }) => {
          // The HTTP request for a token is not intercepted, and hence there may be an
          // error response with status code 401.
          if (error.status === 401) {
            this.error = "Username or password is incorrect.";
          } else {
            this.error = GENERIC_ERROR_MESSAGE;
          }
          this.loading = false;
        },
      );
  }

  clearError(): void {
    this.error = undefined;
  }

  toForgotPassword(): void {
    this.router.navigate(["forgot-password"]);
  }
}
