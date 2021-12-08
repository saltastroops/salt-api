import { Component, OnInit } from '@angular/core';
import {
  AbstractControl,
  FormBuilder,
  FormGroup,
  Validators,
} from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthenticationService } from '../../service/authentication.service';
import { GENERIC_ERROR_MESSAGE } from '../../utils';

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
  showSuccessMessage = false;
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
    this.submitted = true;
    if (this.forgotPasswordForm.invalid) {
      return;
    }
    this.loading = true;
    this.authenticationService
      .sendResetPassword(this.f.usernameEmail.value)
      .subscribe(
        () => {
          // Switch form
          this.showSuccessMessage = true;
        },
        (error: { status: number; error: string }) => {
          if (error.status === 404) {
            this.error = 'Unknown username or email.';
          } else {
            this.error = GENERIC_ERROR_MESSAGE;
          }
          this.loading = false;
        }
      );

    this.loading = false;
  }

  clearError(): void {
    this.error = undefined;
  }

  get f(): { [key: string]: AbstractControl } {
    return this.forgotPasswordForm.controls;
  }

  requestAgain(): void {
    this.showSuccessMessage = false;
  }
}
