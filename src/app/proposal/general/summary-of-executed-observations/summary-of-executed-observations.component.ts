import { Component, EventEmitter, Input, OnInit, Output } from "@angular/core";

import { parseISO } from "date-fns";
import { take } from "rxjs/operators";

import { AuthenticationService } from "../../../service/authentication.service";
import { BlockVisit } from "../../../types/common";
import { User } from "../../../types/user";
import { byPropertiesOf, hasAnyRole, sortArg } from "../../../utils";

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

  observationDate(dateString: string): Date {
    return parseISO(dateString);
  }

  onClick(blockName: string): void {
    this.selectBlock.emit(blockName);
  }

  onColumnClick(event: Event, columnName: sortArg<Observation>): void {
    this.columnsSortDirections[columnName] =
      this.columnsSortDirections[columnName] === "asc" ? "desc" : "asc";

    this.sortedColumn = columnName;
  }

  sortableColumnClass(columnName: sortArg<Observation>): {
    [key: string]: unknown;
  } {
    return {
      pointer: true,
      active: this.sortedColumn == columnName,
      asc: this.columnsSortDirections[columnName] === "asc",
      desc: this.columnsSortDirections[columnName] === "desc",
      sortable: true,
    };
  }
}

interface Observation extends BlockVisit {
  downloadObservation: boolean;
}
