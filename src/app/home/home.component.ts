import { Component, OnInit } from "@angular/core";

import { Observable } from "rxjs";

import { AuthenticationService } from "../service/authentication.service";
import { User } from "../types/user";

@Component({
  selector: "wm-home",
  templateUrl: "./home.component.html",
  styleUrls: ["./home.component.scss"],
})
export class HomeComponent implements OnInit {
  user$!: Observable<User | null>;
  constructor(private authService: AuthenticationService) {}

  ngOnInit(): void {
    this.user$ = this.authService.user();
  }
}
