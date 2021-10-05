import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthenticationService } from '../../service/authentication.service';

@Component({
  selector: 'wm-forgot-password',
  templateUrl: './forgot-password.component.html',
  styleUrls: ['./forgot-password.component.scss'],
})
export class ForgotPasswordComponent implements OnInit {
  forgotPasswordForm!: FormGroup;
  submitted = false;
  loading = false;
  error: string | undefined = undefined;
  switchForm = false;
  constructor(
    private formBuilder: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private authenticationService: AuthenticationService
  ) {}

  ngOnInit(): void {
    this.forgotPasswordForm = this.formBuilder.group({
      usernameEmail: ['', Validators.required],
    });
  }
  forgotPassword(): void {
    // stop here if form is invalid
    if (this.forgotPasswordForm.invalid) {
      return;
    }
    this.loading = true;
    this.authenticationService
      .sendResetPassword(this.f.usernameEmail.value)
      .subscribe(
        () => {
          // Switch form
          this.switchForm = true;
        },
        (error: any) => {
          // The HTTP request for a token is not intercepted, and hence there may be an
          // error response with status code 401.
          if (error.status === 401) {
            this.error = 'Unknown username or email.';
          }
          this.loading = false;
        }
      );

    this.loading = false;
  }

  clearError() {
    this.error = undefined;
  }

  get f() {
    return this.forgotPasswordForm.controls;
  }

  requestAgain() {
    this.switchForm = false;
  }
  toLogin() {
    this.router.navigate(['login']);
  }
}
