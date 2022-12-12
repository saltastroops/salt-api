import { Component, OnInit } from "@angular/core";

import { Subject, of } from "rxjs";
import { catchError, debounceTime, switchMap } from "rxjs/operators";

import { AuthenticationService } from "../../service/authentication.service";
import { ProposalService } from "../../service/proposal.service";
import { ProposalListItem } from "../../types/proposal";
import { User } from "../../types/user";
import { availableSemesters, currentSemester } from "../../utils";

@Component({
  selector: "wm-home-user",
  templateUrl: "./home-user.component.html",
  styleUrls: ["./home-user.component.scss"],
})
export class HomeUserComponent implements OnInit {
  user!: User;
  proposals?: ProposalListItem[];
  filteredProposals?: ProposalListItem[];

  semesterRange$ = new Subject<[string, string]>();

  selectedSemester: string = currentSemester();
  startSemester = "";
  endSemester = "";
  startSemesterValue: string | null = "";
  endSemesterValue = "";
  nextSemester!: string;
  semesterFilter = "";
  availableSemesters = availableSemesters();
  otherFilterByProperties: { [elementId: string]: string | boolean } = {};
  // eslint-disable-next-line  @typescript-eslint/no-explicit-any
  filterProposalsBy: { [elementId: string]: any } = {};
  // eslint-disable-next-line  @typescript-eslint/no-explicit-any
  filterFunctions: { [elementId: string]: any } = {};
  loading = false;
  defaultStartSemester = "2000-1";
  defaultEndSemester = "2099-1";

  isValidSemester!: boolean;
  semesterErrorMessage = "";

  DEBOUNCE_TIME = 100;

  constructor(
    private authService: AuthenticationService,
    private proposalService: ProposalService,
  ) {}

  ngOnInit(): void {
    this.loadFilters();

    this.semesterRange$
      .pipe(
        debounceTime(this.DEBOUNCE_TIME),
        switchMap((data) => {
          return this.proposalService.getProposals(data[0], data[1]);
        }),
        catchError((err) => {
          window.alert(err);
          this.loading = false;
          return of([]);
        }),
      )
      .subscribe((p) => {
        this.proposals = p;
        this.filteredProposals = [...this.proposals];
        this.applyOtherFilters();
        if (this.filteredProposals.length == 1000) {
          alert(
            "1000 or more proposals satisfy the filter criteria. Only the latest 1000 proposals are shown.",
          );
        }
      });

    this.authService.getUser().subscribe((user: User) => {
      this.user = user;
      this.getFilteredProposals();
      if (!this.isValidSemester || this.semesterErrorMessage != "") {
        window.alert(this.semesterErrorMessage);
        this.loading = false;
        this.proposals = [];
      }
    });

    this.filterFunctions["unassigned"] = this.filterUnassignedProposals;
    this.filterFunctions["my_proposals"] = this.filterMyProposals;
    this.filterFunctions["requiring_attention"] = this.filterAttentionProposals;
    this.filterFunctions["unchecked"] = this.filterUncheckedProposals;
    this.filterFunctions["commissioning"] = this.filterCommissioningProposals;
    this.filterFunctions["completed"] = this.filterCompletedProposals;
    this.filterFunctions["active"] = this.filterActiveProposals;
    this.filterFunctions["science"] = this.filterScienceProposals;
    this.filterFunctions["ddt"] = this.filterDDTProposals;
    this.filterFunctions["phase1"] = this.filterPhase12Proposals;
    this.filterFunctions["phase2"] = this.filterPhase12Proposals;
    this.filterFunctions["rejected_completed_expired"] =
      this.filterRejectedCompletedExpiredProposals;

    const index = this.availableSemesters.findIndex(
      (semester) => semester == currentSemester(),
    );
    this.nextSemester = this.availableSemesters[index + 1];
  }

  loadFilters(): void {
    this.filterProposalsBy = JSON.parse(
      localStorage.getItem("filter_proposals_by") || "{}",
    );
    this.selectedSemester =
      this.filterProposalsBy["selected_semester"] || currentSemester();
    this.startSemester = this.filterProposalsBy["start_semester"] || null;
    this.endSemester = this.filterProposalsBy["end_semester"] || null;
    this.semesterFilter = this.filterProposalsBy["semester_filter"] || "";

    this.otherFilterByProperties =
      this.filterProposalsBy["other_filter_by_properties"] || {};
  }

  storeFilters(): void {
    this.filterProposalsBy["semester_filter"] = this.semesterFilter;
    this.filterProposalsBy["other_filter_by_properties"] =
      this.otherFilterByProperties;
    localStorage.setItem(
      "filter_proposals_by",
      JSON.stringify(this.filterProposalsBy),
    );
  }

  onSemesterFilterClick(filterName: string): void {
    this.semesterFilter = filterName;
    if (this.semesterFilter != "semester_range") {
      this.getFilteredProposals();
    }
  }

  applySemesterRangeFilter(): void {
    this.filterProposalsBy["start_semester"] = this.startSemesterValue;
    this.filterProposalsBy["end_semester"] = this.endSemesterValue;
    this.storeFilters();
    const start_semester = this.startSemesterValue
      ? this.startSemesterValue
      : "";
    const end_semester = this.endSemesterValue ? this.endSemesterValue : "";
    this.filterProposalsBySemesters(start_semester, end_semester);
  }

  applyOtherFilters(): void {
    let proposals = this.proposals ? [...this.proposals] : [];
    const properties = Object.keys(this.otherFilterByProperties);
    properties.forEach((property: string) => {
      if (this.otherFilterByProperties[property] === "true") {
        (document.getElementById(property) as HTMLInputElement).checked = true;
        if (property == "phase1") {
          proposals = this.filterFunctions[property](proposals, 1);
        } else if (property == "phase2") {
          proposals = this.filterFunctions[property](proposals, 2);
        } else {
          proposals = this.filterFunctions[property](proposals);
        }
      }
    });
    this.filteredProposals = proposals;
  }

  getFilteredProposals(): void {
    if (this.semesterFilter != "") {
      if (this.semesterFilter == "current_and_next_semester") {
        return this.filterByCurrentAndNextSemester();
      } else if (this.semesterFilter == "semester_range") {
        this.startSemesterValue = this.startSemester;
        this.endSemesterValue = this.endSemester;
        return this.filterBySemesterRangeInputs();
      } else {
        return this.filterBySingleSemester();
      }
    } else {
      this.filterProposalsBySemesters(
        this.defaultStartSemester,
        this.defaultEndSemester,
      );
    }
  }

  parseSemester(semester: string, defaultValue: string): string {
    const semester_regex = /\d{4}-[1-2]/;
    const s = semester != "" ? semester : defaultValue;
    if (!s.match(semester_regex)) {
      throw new Error(
        `The semester ${s} must be of the form yyyy-n, where yyyy is the year and n is 1 or 2.`,
      );
    }
    return s;
  }

  parseSemesterRange(start_semester: string, end_semester: string): string[] {
    if (start_semester === "" && end_semester === "") {
      throw new Error(
        "Please provide a start and/or end semester in the format yyyy-n, where yyyy is the year and n is 1 or 2",
      );
    }
    const start_s = this.parseSemester(
      start_semester,
      this.defaultStartSemester,
    );
    const end_s = this.parseSemester(end_semester, this.defaultEndSemester);
    if (start_s > end_s) {
      throw new Error(
        "The start semester must be less than or equal to the end semester.",
      );
    }
    return [start_s, end_s];
  }

  filterProposalsBySemesters(
    start_semester: string,

    end_semester: string,
  ): void {
    this.semesterErrorMessage = "";

    try {
      const [start_s, end_s] = this.parseSemesterRange(
        start_semester,
        end_semester,
      );
      this.startSemester = start_s;
      this.endSemester = end_s;
      this.isValidSemester = true;
      this.semesterRange$.next([start_s, end_s]);
    } catch (e) {
      this.semesterErrorMessage = e.message;
      this.isValidSemester = false;
    }
  }

  filterByCurrentSemester(): void {
    this.filterProposalsBy["semester_filter"] = this.semesterFilter;
    this.storeFilters();
    const current_semester = currentSemester();
    this.filterProposalsBySemesters(current_semester, current_semester);
  }

  filterByCurrentAndNextSemester(): void {
    this.filterProposalsBy["semester_filter"] = this.semesterFilter;
    this.storeFilters();
    this.filterProposalsBySemesters(currentSemester(), this.nextSemester);
  }

  filterBySingleSemester(): void {
    this.filterProposalsBy["semester_filter"] = this.semesterFilter;
    this.storeFilters();
    if (this.semesterFilter == "current_semester") {
      const current_semester = currentSemester();
      this.filterProposalsBySemesters(current_semester, current_semester);
    } else {
      this.filterProposalsBy["selected_semester"] = this.selectedSemester;
      this.filterProposalsBySemesters(
        this.selectedSemester,
        this.selectedSemester,
      );
    }
  }

  filterBySemesterRangeInputs(): void {
    this.filterProposalsBy["semester_filter"] = this.semesterFilter;
    const start_semester = this.startSemesterValue
      ? this.startSemesterValue
      : "";
    const end_semester = this.endSemesterValue ? this.endSemesterValue : "";
    this.filterProposalsBySemesters(start_semester, end_semester);
  }

  onSemesterSelect(event: Event): void {
    const index = parseInt((event.target as HTMLSelectElement).value, 10);
    this.selectedSemester = this.availableSemesters[index];
    this.filterProposalsBy["selected_semester"] = this.selectedSemester;
    this.storeFilters();
    this.filterBySingleSemester();
  }

  filterAttentionProposals = (
    proposals: ProposalListItem[],
  ): ProposalListItem[] => {
    return proposals.filter(
      (proposal) =>
        proposal.liaisonAstronomer?.givenName === this.user.givenName &&
        proposal.liaisonAstronomer.familyName === this.user.familyName &&
        (proposal.status.value === "Under technical review" ||
          proposal.status.value === "Under scientific review"),
    );
  };

  filterMyProposals = (proposals: ProposalListItem[]): ProposalListItem[] => {
    return proposals.filter(
      (proposal) =>
        (proposal.principalInvestigator.givenName === this.user.givenName &&
          proposal.principalInvestigator.familyName === this.user.familyName) ||
        (proposal.liaisonAstronomer?.givenName === this.user.givenName &&
          proposal.liaisonAstronomer.familyName === this.user.familyName),
    );
  };

  filterUnassignedProposals = (
    proposals: ProposalListItem[],
  ): ProposalListItem[] => {
    return proposals.filter((proposal) => proposal.liaisonAstronomer == null);
  };

  filterUncheckedProposals = (
    proposals: ProposalListItem[],
  ): ProposalListItem[] => {
    return proposals.filter(
      (proposal) =>
        proposal.status.value === "Under technical review" ||
        proposal.status.value === "Under scientific review",
    );
  };

  filterActiveProposals = (
    proposals: ProposalListItem[],
  ): ProposalListItem[] => {
    return proposals.filter((proposal) => proposal.status.value === "Active");
  };

  filterCompletedProposals = (
    proposals: ProposalListItem[],
  ): ProposalListItem[] => {
    return proposals.filter(
      (proposal) => proposal.status.value === "Completed",
    );
  };

  filterCommissioningProposals = (
    proposals: ProposalListItem[],
  ): ProposalListItem[] => {
    return proposals.filter(
      (proposal) => proposal.proposalType === "Commissioning",
    );
  };

  filterScienceProposals = (
    proposals: ProposalListItem[],
  ): ProposalListItem[] => {
    return proposals.filter((proposal) => proposal.proposalType === "Science");
  };

  filterDDTProposals = (proposals: ProposalListItem[]): ProposalListItem[] => {
    return proposals.filter(
      (proposal) => proposal.proposalType === "Director's Discretionary Time",
    );
  };

  filterRejectedCompletedExpiredProposals = (
    proposals: ProposalListItem[],
  ): ProposalListItem[] => {
    return proposals.filter(
      (proposal) =>
        proposal.status.value === "Rejected" ||
        proposal.status.value === "Completed" ||
        proposal.status.value === "Expired",
    );
  };

  filterPhase12Proposals = (
    proposals: ProposalListItem[],
    phase: number,
  ): ProposalListItem[] => {
    return proposals.filter((proposal) => proposal.phase == phase);
  };

  filterProposals(filter: string): void {
    let proposals = this.proposals ? [...this.proposals] : [];
    this.otherFilterByProperties[filter] =
      this.otherFilterByProperties[filter] == "true" ? "false" : "true";
    this.storeFilters();
    const properties = Object.keys(this.otherFilterByProperties);
    properties.forEach((property: string) => {
      if (this.otherFilterByProperties[property] === "true") {
        if (property == "phase1") {
          proposals = this.filterFunctions[property](proposals, 1);
        } else if (property == "phase2") {
          proposals = this.filterFunctions[property](proposals, 2);
        } else {
          proposals = this.filterFunctions[property](proposals);
        }
      }
    });
    this.filteredProposals = proposals;
  }

  isSA(proposal: ProposalListItem): boolean {
    return (
      proposal.liaisonAstronomer?.givenName === this.user.givenName &&
      proposal.liaisonAstronomer.familyName === this.user.familyName
    );
  }

  isPI(proposal: ProposalListItem): boolean {
    return (
      proposal.principalInvestigator.givenName === this.user.givenName &&
      proposal.principalInvestigator.familyName === this.user.familyName
    );
  }

  isPC(proposal: ProposalListItem): boolean {
    return (
      proposal.principalContact.givenName === this.user.givenName &&
      proposal.principalContact.familyName === this.user.familyName
    );
  }

  proposalRowClass(proposal: ProposalListItem): string {
    if (this.isPI(proposal)) {
      return "pi";
    } else if (this.isPC(proposal)) {
      return "pc";
    } else if (this.isSA(proposal)) {
      return "sa";
    }
    return "";
  }
}
