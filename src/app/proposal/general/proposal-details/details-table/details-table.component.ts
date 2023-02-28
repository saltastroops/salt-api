import { Component, Input, OnChanges, OnInit } from "@angular/core";

import { AuthenticationService } from "../../../../service/authentication.service";
import { Proposal } from "../../../../types/proposal";
import { User } from "../../../../types/user";
import { AutoUnsubscribe, hasAnyRole } from "../../../../utils";

@Component({
  selector: "wm-details-table",
  templateUrl: "./details-table.component.html",
  styleUrls: ["./details-table.component.scss"],
})
@AutoUnsubscribe()
export class DetailsTableComponent implements OnChanges, OnInit {
  @Input() proposal!: Proposal;
  releaseDate!: Date;
  user!: User;
  showChangeButton = false;

  constructor(private authService: AuthenticationService) {}

  ngOnInit(): void {
    this.authService.getUser().subscribe((user) => {
      this.user = user;
      const isUserPcOrPi = this.proposal.investigators.some(
        (i) => i.id === user.id && (i.isPc || i.isPi),
      );
      this.showChangeButton =
        isUserPcOrPi || hasAnyRole(user, ["Administrator"]);
    });
    this.updateReleaseDate();
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
