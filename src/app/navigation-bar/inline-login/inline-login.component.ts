import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthenticationService } from '../../service/authentication.service';
import { AccessToken } from '../../types/authentication';
import { GENERIC_ERROR_MESSAGE } from '../../utils';

@Component({
  selector: 'wm-inline-login',
  templateUrl: './inline-login.component.html',
  styleUrls: ['./inline-login.component.scss'],
})
export class InlineLoginComponent implements OnInit {
  loginForm!: FormGroup;
  loading: boolean = false;
  error: string | null = null;

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthenticationService
  ) {}

  ngOnInit(): void {
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
    if (this.f.username.errors?.required) {
      this.error = 'The username is required.';
      return;
    }
    if (this.f.password.errors?.required) {
      this.error = 'The password is required.';
      return;
    }

    this.loading = true;
    this.error = null;

    this.authService
      .login(this.f.username.value, this.f.password.value)
      .subscribe(
        () => {
          this.loading = false;
        },
        (error: any) => {
          // The HTTP request for a token is not intercepted, and hence there may be an
          // error response with status code 401.
          if (error.status === 401) {
            this.error = 'Username or password is incorrect.';
          } else {
            this.error = GENERIC_ERROR_MESSAGE;
          }
          this.loading = false;
        }
      );
  }
}
