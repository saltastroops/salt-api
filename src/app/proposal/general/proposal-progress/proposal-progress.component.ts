import { Component, Input, OnInit } from "@angular/core";

import { of } from "rxjs";
import { catchError, switchMap, tap } from "rxjs/operators";

import { environment } from "../../../../environments/environment";
import { ProposalService } from "../../../service/proposal.service";
import {
  Proposal,
  ProposalProgress,
  ProposalProgressReport,
} from "../../../types/proposal";
import { AutoUnsubscribe, currentSemester } from "../../../utils";

@AutoUnsubscribe()
@Component({
  selector: "wm-proposal-progress",
  templateUrl: "./proposal-progress.component.html",
  styleUrls: ["./proposal-progress.component.scss"],
})
export class ProposalProgressComponent implements OnInit {
  @Input() proposal!: Proposal;
  proposalProgress!: ProposalProgress;
  showForm = false;
  error: string | undefined;
  loading = false;
  apiUrl = environment.apiUrl;
  currentSemester = currentSemester();
  currentProgressReportExists!: boolean;
  progressReports: ProposalProgressReport[] | null = null;
  showReports = false;
  reportsLinksText = "Show progress reports for other semesters";

  constructor(private proposalService: ProposalService) {}

  ngOnInit(): void {
    this.proposalService
      .getProgressReport(this.proposal.proposalCode, currentSemester())
      .pipe(
        tap((data) => {
          this.proposalProgress = { ...data };
          this.loading = false;
        }),
        switchMap(() => {
          return this.proposalService.getProgressReportsUrls(
            this.proposal.proposalCode,
          );
        }),
        catchError((err) => {
          this.error = err.message;
          this.loading = false;
          return of({});
        }),
      )
      .subscribe((p: ProposalProgressReport[]) => {
        const _currentSemester = currentSemester();
        this.progressReports = this.allProgressReports(p);
        this.currentProgressReportExists = p.some(
          (report) => report.semester === _currentSemester,
        );
      });
  }

  showProgressReportForm(): void {
    this.loading = true;
    this.showForm = true;
  }

  closeForm(): void {
    this.showForm = false;

    const element = document.getElementById("proposal-progress");
    element?.scrollIntoView();
  }

  onSuccessfulSubmission(progressReport: ProposalProgress): void {
    if (progressReport.semester === this.currentSemester) {
      this.currentProgressReportExists = true;
    }
  }

  allProgressReports(
    progressReportsUrls: ProposalProgressReport[],
  ): ProposalProgressReport[] {
    let otherProgressReportsUrls: ProposalProgressReport[] =
      progressReportsUrls;
    const _currentSemester = currentSemester();
    if (
      progressReportsUrls !== undefined &&
      progressReportsUrls.some((report) => report.semester === _currentSemester)
    ) {
      otherProgressReportsUrls = progressReportsUrls.filter(
        (report) => report.semester !== _currentSemester,
      );
    }
    return otherProgressReportsUrls;
  }

  progressReportsUrlsMap(
    progressReports: ProposalProgressReport[],
  ): ProposalProgressReport[] {
    return progressReports.map((r) => {
      const url = new URL(r.url);
      const noOriginUrl = url.href.replace(url.origin, "");
      r.url = this.apiUrl + noOriginUrl;

      return r;
    });
  }

  onClick(): void {
    this.showReports = !this.showReports;
    this.reportsLinksText = this.showReports
      ? "Hide progress reports for other semesters"
      : "Show progress reports for other semesters";
  }
}
