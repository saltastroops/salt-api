import { Component, OnInit } from "@angular/core";
import {
  AbstractControl,
  UntypedFormBuilder,
  UntypedFormGroup,
  Validators,
} from "@angular/forms";

import { AuthenticationService } from "../../service/authentication.service";

@Component({
  selector: "wm-request-verification-link",
  templateUrl: "./request-verification-link.component.html",
  styleUrls: ["./request-verification-link.component.scss"],
})
export class RequestVerificationLinkComponent implements OnInit {
  requestLinkForm!: UntypedFormGroup;
  loading = false;
  submitted = false;
  successfull = false;
  error: string | undefined = undefined;

  constructor(
    private formBuilder: UntypedFormBuilder,
    private authenticationService: AuthenticationService,
  ) {}

  ngOnInit(): void {
    this.requestLinkForm = this.formBuilder.group({
      usernameEmail: ["", Validators.required],
    });
  }

  get f(): { [key: string]: AbstractControl } {
    return this.requestLinkForm.controls;
  }

  requestVerificationLink(): void {
    this.submitted = true;
    this.error = undefined;

    // stop here if form is invalid
    if (this.requestLinkForm.invalid) {
      return;
    }

    this.loading = true;
    this.authenticationService
      .requestVerificationLink(this.f.usernameEmail.value)
      .subscribe(
        () => {
          this.loading = false;
          this.successfull = true;
        },
        (error) => {
          this.loading = false;
          this.error = error.message;
        },
      );
  }
}
