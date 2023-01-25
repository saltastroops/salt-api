import { Component, OnInit } from "@angular/core";
import { FormControl, FormGroup } from "@angular/forms";
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
  gotoProposalForm!: FormGroup;

  constructor(
    private authService: AuthenticationService,
    private router: Router,
  ) {}

  ngOnInit(): void {
    // Ensure that the proposal goto button works if you are on the proposal page.
    this.selectedUri = sessionStorage.getItem("selectedUri") || "";
    this.user$ = this.authService.user();
    this.gotoProposalForm = new FormGroup({
      proposalCode: new FormControl(""),
    });
  }

  get isLoggedIn(): boolean {
    return this.authService.isAuthenticated();
  }

  logout(): void {
    this.authService.logout().subscribe(() => {
      /* do nothing */
    });
    this.router.navigate(["/"]);
  }

  gotoProposal(): void {
    const proposalCode = this.gotoProposalForm.value.proposalCode;
    this.gotoProposalForm.patchValue({ proposalCode: "" });
    this.router.navigate(["/proposal", proposalCode]);
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
