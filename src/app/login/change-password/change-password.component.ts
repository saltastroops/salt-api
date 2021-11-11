import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Observable } from 'rxjs';
import { AccessToken } from '../../types/authentication';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthenticationService } from '../../service/authentication.service';
import { GENERIC_ERROR_MESSAGE } from '../../utils';

@Component({
  selector: 'wm-change-password',
  templateUrl: './change-password.component.html',
  styleUrls: ['./change-password.component.scss'],
})
export class ChangePasswordComponent implements OnInit {
  changePasswordForm!: FormGroup;
  token!: string;
  user: any;
  loading = false;
  submitted = false;
  error: string | undefined = undefined;

  constructor(
    private formBuilder: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private authenticationService: AuthenticationService
  ) {}

  ngOnInit() {
    this.changePasswordForm = this.formBuilder.group({
      password: ['', Validators.required],
      retypedPassword: ['', Validators.required],
    });
    this.route.params.subscribe((params) => {
      this.token = params.token;
    });
  }

  // convenience getter for easy access to form fields
  get f() {
    return this.changePasswordForm.controls;
  }

  changePassword() {
    this.submitted = true;

    // stop here if form is invalid
    if (this.changePasswordForm.invalid) {
      return;
    }
    if (this.f.password.value !== this.f.retypedPassword.value) {
      this.error = 'Password mismatch.';
      return;
    }

    this.loading = true;
    this.authenticationService
      .changePassword(this.f.password.value, this.token)
      .subscribe(
        () => {
          this.loading = false;
          this.router.navigate(['/login']);
        },
        (error: any) => {
          this.error = error;
          this.loading = false;
        }
      );
  }

  clearError() {
    this.error = undefined;
  }
}
