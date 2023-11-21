import { Component, Input, OnInit } from "@angular/core";

import { AuthenticationService } from "../../../../service/authentication.service";
import { Proposal } from "../../../../types/proposal";
import { UserRole } from "../../../../types/user";
import {
  AutoUnsubscribe,
  hasAnyRole,
  isUserPrincipalContact,
  isUserPrincipalInvestigator,
} from "../../../../utils";

@Component({
  selector: "wm-liaison-astronomer",
  templateUrl: "./liaison-astronomer.component.html",
  styleUrls: ["./liaison-astronomer.component.scss"],
})
@AutoUnsubscribe()
export class LiaisonAstronomerComponent implements OnInit {
  @Input() proposal!: Proposal;
  isAdminOrSa = false;

  constructor(private authService: AuthenticationService) {}

  ngOnInit(): void {
    this.authService.user().subscribe(
      (user) => {
        if (user) {
          this.isAdminOrSa = hasAnyRole(user, [
            "SALT Astronomer",
            "Administrator",
          ] as UserRole[]);
        }
      },
      () => {
        this.isAdminOrSa = false;
      },
    );
  }
}
