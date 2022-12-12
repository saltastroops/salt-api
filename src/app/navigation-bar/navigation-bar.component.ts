import { Component, OnInit } from "@angular/core";
import { Router } from "@angular/router";

import { Observable } from "rxjs";

import { AuthenticationService } from "../service/authentication.service";
import { User } from "../types/user";
import { hasAnyRole } from "../utils";

@Component({
  selector: "wm-navigation-bar",
  templateUrl: "./navigation-bar.component.html",
  styleUrls: ["./navigation-bar.component.scss"],
})
export class NavigationBarComponent implements OnInit {
  user$!: Observable<User | null>;
  selectedUri!: string;
  hasAnyRole = hasAnyRole;

  constructor(
    private authService: AuthenticationService,
    private router: Router,
  ) {}

  ngOnInit(): void {
    this.selectedUri = sessionStorage.getItem("selectedUri") || "";
    this.user$ = this.authService.user();
  }

  logout(): void {
    this.authService.logout().subscribe(() => {
      /* do nothing */
    });
    this.router.navigate(["/"]);
  }

  selectUri(uri: string): void {
    this.selectedUri = uri;
    sessionStorage.setItem("selectedUri", uri);
  }

  toggleDropdownMenu(e: Event): void {
    const dropdown = e.target as HTMLElement;
    if (dropdown.parentElement?.classList.contains("navbar-dropdown")) {
      dropdown.blur();
    }
  }
}
