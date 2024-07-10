import { Component, OnInit } from "@angular/core";

import { AuthenticationService } from "../../service/authentication.service";
import { UserService } from "../../service/user.service";
import { User, UserListItem, UserRole } from "../../types/user";
import { hasAnyRole } from "../../utils";

@Component({
  selector: "wm-edit-roles",
  templateUrl: "./edit-roles.component.html",
  styleUrls: ["./edit-roles.component.scss"],
})
export class EditRolesComponent implements OnInit {
  users!: UserListItem[];
  error: string | undefined = undefined;
  selectedUserId!: number;
  loading = false;
  selectedUser!: User;
  user!: User;
  constructor(
    private userService: UserService,
    private authService: AuthenticationService,
  ) {}

  ngOnInit(): void {
    this.authService.getUser().subscribe((user) => {
      this.selectedUser = user;
      this.user = user;
      this.selectedUserId = user.id;
    });
    this.userService.getUsers().subscribe(
      (users) => {
        this.users = users;
      },
      () => {
        this.error = "Failed to fetch users.";
      },
    );
  }

  onSelectUser(event: Event): void {
    this.loading = true;
    this.selectedUserId = parseInt(
      (event.target as HTMLSelectElement).value,
      10,
    );
    this.userService.getUserById(this.selectedUserId).subscribe(
      (user) => {
        this.selectedUser = user;
        this.loading = false;
      },
      () => {
        this.error = `Failed to fetch selected user.`;
        this.loading = false;
      },
    );
  }
  updateRoles(role: UserRole): void {
    this.error = undefined;

    // Convert roles array to a Set for efficient operations
    const rolesSet = new Set(this.selectedUser.roles);

    if (rolesSet.has(role)) {
      // If the role is in the set, remove it
      rolesSet.delete(role);
    } else {
      // If the role is not in the set, add it
      rolesSet.add(role);
    }

    // Convert the Set back to an array
    this.selectedUser.roles = Array.from(rolesSet);
  }
  submitRoles(): void {
    this.error = undefined;
    this.loading = true;
    this.userService.updateRoles(this.selectedUser).subscribe(
      (user) => {
        this.selectedUser = user;
        this.loading = false;
      },
      () => {
        this.error = "Failed to update user roles.";
        this.loading = false;
      },
    );
  }

  protected readonly hasAnyRole = hasAnyRole;
}
