import { Component, Input, OnInit } from "@angular/core";

import { parseISO } from "date-fns";

import { environment } from "../../../../environments/environment";
import { AuthenticationService } from "../../../service/authentication.service";
import { Block, BlockStatus } from "../../../types/block";
import { FinderChart } from "../../../types/observation";
import { Investigator } from "../../../types/proposal";
import { User } from "../../../types/user";
import { currentJulianDay, finderChartURL } from "../../../util";
import {
  AutoUnsubscribe,
  hasAnyRole,
  isUserPrincipalContact,
  isUserPrincipalInvestigator,
  originalFinderChartURL,
} from "../../../utils";

@Component({
  selector: "wm-block",
  templateUrl: "./block.component.html",
  styleUrls: ["./block.component.scss"],
})
@AutoUnsubscribe()
export class BlockComponent implements OnInit {
  @Input() block!: Block;
  @Input() investigators!: Investigator[];
  originalFinderChartURL = originalFinderChartURL;

  validFrom!: Date;

  validUntil!: Date;

  latestSubmissionDate!: Date;
  user!: User;
  showEditBlockButton = false;

  constructor(private authService: AuthenticationService) {}

  ngOnInit(): void {
    const jd = currentJulianDay();
    this.validFrom = jd.start;
    this.validUntil = jd.end;
    this.authService.getUser().subscribe((user) => {
      this.user = user;
      this.showEditBlockButton =
        isUserPrincipalInvestigator(this.user, this.investigators) ||
        isUserPrincipalContact(this.user, this.investigators) ||
        hasAnyRole(user, ["Administrator", "SALT Astronomer"]);
    });
    this.latestSubmissionDate = parseISO(this.block.latestSubmissionDate);
  }

  blockClass(block: Block): string {
    if (block.status.value === "Completed") {
      return "completed-block";
    } else if (block.status.value === "Active") {
      return "";
    }
    return "inactive-block";
  }

  validSortedFinderCharts(finderCharts: FinderChart[]): FinderChart[] {
    const isValid = (fc: FinderChart) =>
      (fc.validFrom === null || parseISO(fc.validFrom) <= this.validUntil) &&
      (fc.validUntil === null || parseISO(fc.validUntil) >= this.validFrom);
    const millisecondsFromEpoch = (fc: FinderChart) =>
      fc.validFrom ? parseISO(fc.validFrom).getTime() : 0;
    const compare = (fc1: FinderChart, fc2: FinderChart) =>
      millisecondsFromEpoch(fc1) - millisecondsFromEpoch(fc2);
    return [...finderCharts.filter(isValid)].sort(compare);
  }

  thumbnailFinderChartURL(finderChart: FinderChart): string {
    const url = finderChartURL(
      finderChart,
      ["thumbnail", "original"],
      ["png", "jpg"],
      environment.apiUrl,
    );
    return url || "/assets/noun-missing-2181345.png";
  }

  updateBlockStatus(blockStatusUpdate: BlockStatusUpdate): void {
    this.block.status.value = blockStatusUpdate.value;
    this.block.status.reason = blockStatusUpdate.reason;
  }
}

interface BlockStatusUpdate extends BlockStatus {
  blockId: number;
}
