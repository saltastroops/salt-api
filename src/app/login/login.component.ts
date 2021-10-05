import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Observable } from 'rxjs';
import { AccessToken } from '../types/authentication';
import { AuthenticationService } from '../service/authentication.service';

@Component({ templateUrl: 'login.component.html' })
export class LoginComponent implements OnInit {
  loginForm!: FormGroup;
  accessToken!: Observable<AccessToken>;
  loading = false;
  submitted = false;
  error: string | undefined = undefined;

  constructor(
    private formBuilder: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private authenticationService: AuthenticationService
  ) {
    // redirect to home if already logged in
    if (this.authenticationService.isAuthenticated()) {
      window.alert('You are logged in already.');
      this.router.navigate(['/']);
    }
  }

  ngOnInit() {
    this.loginForm = this.formBuilder.group({
      username: ['', Validators.required],
      password: ['', Validators.required],
    });
  }

  // convenience getter for easy access to form fields
  get f() {
    return this.loginForm.controls;
  }

  login() {
    this.submitted = true;

    // stop here if form is invalid
    if (this.loginForm.invalid) {
      return;
    }

    this.loading = true;
    this.authenticationService
      .login(this.f.username.value, this.f.password.value)
      .subscribe(
        (data: AccessToken) => {
          this.authenticationService.setAccessToken(data);
          const redirection = this.authenticationService.getRedirection();
          const redirectUrlParts =
            redirection && redirection.urlParts.length
              ? redirection.urlParts
              : ['/'];
          const redirectQueryParams = redirection
            ? redirection.queryParams
            : {};
          this.router.navigate(redirectUrlParts, {
            queryParams: redirectQueryParams,
          });
        },
        (error: any) => {
          // The HTTP request for a token is not intercepted, and hence there may be an
          // error response with status code 401.
          if (error.status === 401) {
            this.error = 'Username or password is incorrect.';
          } else {
            this.error =
              'Sorry, something has gone wrong. Please try again later.';
          }
          this.loading = false;
        }
      );
  }

  clearError() {
    this.error = undefined;
  }

  toForgotPassword() {
    this.router.navigate(['forgot-password']);
  }
}
