import { Component, OnInit } from "@angular/core";
import { Router } from "@angular/router";

import { AuthenticationService } from "../../service/authentication.service";
import { UserService } from "../../service/user.service";
import { UserListItem } from "../../types/user";

@Component({
  selector: "wm-switch-user",
  templateUrl: "./switch-user.component.html",
  styleUrls: ["./switch-user.component.scss"],
})
export class SwitchUserComponent implements OnInit {
  switchToUser: UserListItem | null = null;
  displayedUsers: DisplayedUser[] = [];
  submitError: string | null = null;
  loadError: string | null = null;
  loading = false;
  isFetchingUsers = false;

  constructor(
    private authService: AuthenticationService,
    private userService: UserService,
    private router: Router,
  ) {}

  ngOnInit(): void {
    this.isFetchingUsers = true;
    this.userService.getUsers().subscribe(
      (users) => {
        this.displayedUsers = this.initDisplayedUsers(users).filter(
          (name) => name.givenName !== "-",
        );
        this.isFetchingUsers = false;
      },
      () => {
        this.loadError = "Failed to fetch users.";
        this.isFetchingUsers = false;
      },
    );
  }

  sortFunction(
    a: UserListItem | DisplayedUser,
    b: UserListItem | DisplayedUser,
  ): number {
    if (a.familyName + a.givenName > b.familyName + b.givenName) {
      return 1;
    }
    if (a.familyName + a.givenName < b.familyName + b.givenName) {
      return -1;
    }
    return 0;
  }

  initDisplayedUsers(users: UserListItem[]): DisplayedUser[] {
    const sortedUsers = users.sort(this.sortFunction);
    const initUsers: DisplayedUser[] = [];

    for (let i = 0; i < sortedUsers.length - 1; i++) {
      initUsers.push({
        ...users[i],
        displayUsername:
          this.haveSameName(users[i], users[i + 1]) ||
          this.haveSameName(users[i], users[i - 1]),
      });
    }
    return initUsers.sort(this.sortFunction);
  }

  haveSameName(
    user1: UserListItem | undefined,
    user2: UserListItem | undefined,
  ): boolean {
    if (!user1 || !user2) {
      return false;
    }
    return (
      user1.familyName === user2.familyName &&
      user1.givenName === user2.givenName
    );
  }

  switch(value: string): void {
    this.loading = true;
    this.submitError = null;
    this.loadError = null;
    const user = this.displayedUsers.filter(
      (user) => user.id === parseInt(value),
    )[0];
    if (user) {
      this.authService.switchUser(user.username).subscribe(
        () => {
          this.loading = false;
          this.router.navigate(["/"]);
        },
        () => {
          this.loading = false;
          this.submitError = "Failed to switch user.";
        },
      );
    } else {
      this.loading = false;
      this.submitError = "No user selected.";
    }
  }
}

interface DisplayedUser extends UserListItem {
  displayUsername: boolean;
}
