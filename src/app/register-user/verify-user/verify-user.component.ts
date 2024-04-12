import { Component, OnInit } from "@angular/core";
import { ActivatedRoute } from "@angular/router";

import { AuthenticationService } from "../../service/authentication.service";

@Component({
  selector: "wm-activate-user",
  templateUrl: "./verify-user.component.html",
  styleUrls: ["./verify-user.component.scss"],
})
export class VerifyUserComponent implements OnInit {
  error: string | undefined = undefined;
  user_id!: number;
  token!: string;

  constructor(
    private route: ActivatedRoute,
    private authenticationService: AuthenticationService,
  ) {}

  ngOnInit(): void {
    this.route.params.subscribe((params) => {
      this.user_id = params.user_id;
      this.token = params.token;
    });
    this.verifyUser();
  }

  verifyUser(): void {
    this.authenticationService.verifyUser(this.user_id, this.token).subscribe(
      () => {
        // Do nothing
      },
      (error) => {
        this.error = error.message;
      },
    );
  }

  requestLink(email: string): void {
    this.authenticationService.requestVerificationLink(email).subscribe(
      () => {
        // Do nothing
      },
      (error) => {
        this.error = error.message;
      },
    );
  }
}
