import { Component, EventEmitter, Input, OnInit, Output } from "@angular/core";

import { parseISO } from "date-fns";
import { take } from "rxjs/operators";

import { AuthenticationService } from "../../../service/authentication.service";
import { BlockVisit } from "../../../types/common";
import { User } from "../../../types/user";
import { hasAnyRole } from "../../../utils";

@Component({
  selector: "wm-summary-of-executed-observations",
  templateUrl: "./summary-of-executed-observations.component.html",
  styleUrls: ["./summary-of-executed-observations.component.scss"],
})
export class SummaryOfExecutedObservationsComponent implements OnInit {
  selectAll = false;
  @Input() blockVisits!: BlockVisit[];
  @Output() selectBlock = new EventEmitter<string>();
  observations!: Observation[];
  user!: User;
  showEditBlockButton = false;

  constructor(private authService: AuthenticationService) {}

  ngOnInit(): void {
    this.authService
      .getUser()
      .pipe(take(1))
      .subscribe((user) => {
        this.user = user;
        this.showEditBlockButton = !hasAnyRole(user, [
          "SALT Astronomer",
          "SALT Operator",
        ]);
      });
    this.observations = this.blockVisits.map((o) => ({
      ...o,
      downloadObservation: this.selectAll,
    }));
  }

  selectDeselectAll(selectAll: boolean): void {
    this.selectAll = selectAll;
    this.observations.forEach((e) => {
      e.downloadObservation = this.selectAll;
    });
  }

  toggleRequestData(observation_id: number): void {
    this.selectAll = true;
    this.observations.forEach((o) => {
      if (o.blockId === observation_id) {
        o.downloadObservation = !o.downloadObservation;
      }
      if (!o.downloadObservation) {
        this.selectAll = false;
      }
    });
  }

  observationDate(dateString: string): Date {
    return parseISO(dateString);
  }

  onClick(blockName: string): void {
    this.selectBlock.emit(blockName);
  }
}

interface Observation extends BlockVisit {
  downloadObservation: boolean;
}
