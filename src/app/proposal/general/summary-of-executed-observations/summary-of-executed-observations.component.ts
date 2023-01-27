import { Component, EventEmitter, Input, OnInit, Output } from "@angular/core";

import { parseISO } from "date-fns";
import { take } from "rxjs/operators";

import { AuthenticationService } from "../../../service/authentication.service";
import { Sort } from "../../../sort";
import { SortDirection } from "../../../sort.directive";
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
  @Output() selectBlock = new EventEmitter<number>();
  observations!: Observation[];
  user!: User;
  showEditBlockButton = false;
  columnsSortDirections: { [columnName: string]: string } = {};
  sortedColumn = "";

  constructor(private authService: AuthenticationService) {}

  ngOnInit(): void {
    this.authService
      .getUser()
      .pipe(take(1))
      .subscribe((user) => {
        this.user = user;
        this.showEditBlockButton = !hasAnyRole(user, [
          "Administrator",
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

  sort = (key: string, direction: SortDirection): void => {
    const sort = new Sort();
    const isString = ["blockName", "status", "targets"].includes(key);
    let sortFunc;
    if (key !== "targets") {
      sortFunc = sort.startSort(key, direction, isString);
    } else {
      sortFunc = sort.startSort(
        (o: Observation) => o.targets.join(" "),
        direction,
        isString,
      );
    }
    this.observations.sort(sortFunc);
  };

  observationDate(dateString: string): Date {
    return parseISO(dateString);
  }

  onClick(blockId: number): void {
    this.selectBlock.emit(blockId);
  }
}

interface Observation extends BlockVisit {
  downloadObservation: boolean;
}
