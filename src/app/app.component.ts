import { Component, OnInit } from "@angular/core";
import { FormBuilder } from "@angular/forms";

import { AuthenticationService } from "./service/authentication.service";

@Component({
  selector: "wm-root",
  templateUrl: "./app.component.html",
  styleUrls: ["./app.component.scss"],
})
export class AppComponent implements OnInit {
  title = "Web Manager";

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthenticationService,
  ) {}

  ngOnInit(): void {
    // Make sure that invalid tokens are removed
    if (!this.authService.isAuthenticated()) {
      this.authService.logout();
    }

    // Load the user details
    this.authService.updateUser();
  }
}