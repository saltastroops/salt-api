import { Component, EventEmitter, Input, OnInit, Output } from "@angular/core";

import { parseISO } from "date-fns";

import { AuthenticationService } from "../../../service/authentication.service";
import { Sort } from "../../../sort";
import { SortDirection } from "../../../sort.directive";
import { BlockRejectionReason } from "../../../types/block";
import { BlockVisit, BlockVisitStatus } from "../../../types/common";
import { User } from "../../../types/user";
import { AutoUnsubscribe, hasAnyRole } from "../../../utils";

@Component({
  selector: "wm-summary-of-executed-observations",
  templateUrl: "./summary-of-executed-observations.component.html",
  styleUrls: ["./summary-of-executed-observations.component.scss"],
})
@AutoUnsubscribe()
export class SummaryOfExecutedObservationsComponent implements OnInit {
  @Input() blockVisits!: BlockVisit[];
  @Output() selectBlock = new EventEmitter<number>();
  observations!: Observation[];
  groupedObservations: { [key: string]: Observation[] } = {};
  user!: User;
  showEditBlockButton = false;
  showObservationsList = false;
  displayedSemesters = new Set<string>();
  selectedSemesters = new Set<string>();

  Object = Object; //Object is used in the template

  constructor(private authService: AuthenticationService) {}

  ngOnInit(): void {
    this.authService.getUser().subscribe((user) => {
      this.user = user;
      this.showEditBlockButton = hasAnyRole(user, [
        "Administrator",
        "SALT Astronomer",
      ]);
    });
    this.observations = this.blockVisits.map((o) => ({
      ...o,
      downloadObservation: false,
    }));
    this.groupObservations();
  }

  selectAllData(selected: boolean): void {
    this.observations.forEach((o) => {
      o.downloadObservation = selected;
    });
    if (selected) {
      this.selectedSemesters = this.allSemesters();
    } else {
      this.selectedSemesters = new Set<string>();
    }
  }

  toggleRequestData(selected: boolean, observationId: number): void {
    // Assume that all data is selected.
    this.selectedSemesters = this.allSemesters();

    this.observations.forEach((o) => {
      if (o.id === observationId) {
        o.downloadObservation = selected;
      }
      if (!o.downloadObservation) {
        // Revoke assumption that any data is not requested for that semester.
        this.selectedSemesters.delete(o.semester);
      }
    });
  }

  sort = (key: string, direction: SortDirection): void => {
    const sort = new Sort();
    const isString = ["blockName", "status", "targets"].includes(key);
    let sortFunc: any;
    if (key !== "targets") {
      sortFunc = sort.startSort(key, direction, isString);
    } else {
      sortFunc = sort.startSort(
        (o: Observation) => o.targets.join(" "),
        direction,
        isString,
      );
    }
    this.allSemesters().forEach((semester) => {
      this.groupedObservations[semester].sort(sortFunc);
    });
  };

  observationDate(dateString: string): Date {
    return parseISO(dateString);
  }

  onClick(blockId: number): void {
    this.selectBlock.emit(blockId);
  }

  toggleObservationsList(scrollToSection: boolean): void {
    this.showObservationsList = !this.showObservationsList;
    if (scrollToSection) {
      const element = document.getElementById("executed-observations");
      element?.scrollIntoView();
    }
  }

  updateBlockVisitStatus(blockVisitStatusUpdate: BlockVisitStatusUpdate): void {
    const blockVisit = this.observations.find(
      (o) => o.id === blockVisitStatusUpdate.blockVisitId,
    );
    if (blockVisit !== undefined) {
      blockVisit.status = blockVisitStatusUpdate.blockVisitStatus;
      blockVisit.rejectionReason = blockVisitStatusUpdate.rejectionReason;
    }
  }

  addOrRemoveDisplayedSemester(semester: string): void {
    if (this.displayedSemesters.has(semester)) {
      this.displayedSemesters.delete(semester);
    } else {
      this.displayedSemesters.add(semester);
    }
  }

  groupObservations(): void {
    this.observations.forEach((o) => {
      // eslint-disable-next-line no-prototype-builtins
      if (!this.groupedObservations.hasOwnProperty(o.semester)) {
        this.groupedObservations[o.semester] = [];
      }
      this.groupedObservations[o.semester].push(o);
    });
  }

  selectAllSemesterData(selected: boolean, semester: string): void {
    this.observations.forEach((o) => {
      if (o.semester === semester) {
        o.downloadObservation = selected;
      }
    });
    selected
      ? this.selectedSemesters.add(semester)
      : this.selectedSemesters.delete(semester);
  }

  isAllDataSelected(): boolean {
    return (
      this.selectedSemesters.size === this.allSemesters().size &&
      [...this.allSemesters()].every((value) =>
        this.selectedSemesters.has(value),
      )
    );
  }

  isAllSemesterDataChecked(semester: string): boolean {
    return this.selectedSemesters.has(semester);
  }

  isObservationSelected(observationId: number): boolean {
    let isChecked: boolean | null = null;
    this.observations.forEach((o) => {
      if (o.id === observationId) {
        isChecked = o.downloadObservation;
      }
    });
    if (isChecked === null) {
      throw new Error(`Observation Id ${observationId} is not found.`);
    } else {
      return isChecked;
    }
  }

  allSemesters(): Set<string> {
    return new Set<string>(Object.keys(this.groupedObservations));
  }
}

interface Observation extends BlockVisit {
  downloadObservation: boolean;
}

interface BlockVisitStatusUpdate {
  blockVisitId: number;
  blockVisitStatus: BlockVisitStatus;
  rejectionReason: BlockRejectionReason | null;
}
