import { Component, Input, OnChanges, OnInit } from "@angular/core";

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
  selector: "wm-details-table",
  templateUrl: "./details-table.component.html",
  styleUrls: ["./details-table.component.scss"],
})
@AutoUnsubscribe()
export class DetailsTableComponent implements OnChanges, OnInit {
  @Input() proposal!: Proposal;
  releaseDate!: Date;
  isAdminOrSa = false;
  isPiOrPc = false;
  isSelfActivatable!: boolean;
  loading = false;

  constructor(private authService: AuthenticationService) {}
  ngOnInit(): void {
    this.updateReleaseDate();
    this.isSelfActivatable = this.proposal.generalInfo.isSelfActivatable;
    this.authService.user().subscribe(
      (user) => {
        if (user) {
          this.isAdminOrSa = hasAnyRole(user, [
            "SALT Astronomer",
            "Administrator",
          ] as UserRole[]);

          this.isPiOrPc =
            isUserPrincipalInvestigator(user, this.proposal.investigators) ||
            isUserPrincipalContact(user, this.proposal.investigators);
        }
      },
      () => {
        this.isAdminOrSa = false;
        this.isPiOrPc = false;
      },
    );
  }

  ngOnChanges(): void {
    this.updateReleaseDate();
  }

  updateReleaseDate(): void {
    const tmpDate = new Date(
      this.proposal.generalInfo.proprietaryPeriod.startDate,
    );
    this.releaseDate = new Date(
      tmpDate.setMonth(
        tmpDate.getMonth() + this.proposal.generalInfo.proprietaryPeriod.period,
      ),
    );
  }

  onProprietaryPeriodUpdate(proprietaryPeriod: number): void {
    this.proposal.generalInfo.proprietaryPeriod.period = proprietaryPeriod;
    this.updateReleaseDate();
  }
}
