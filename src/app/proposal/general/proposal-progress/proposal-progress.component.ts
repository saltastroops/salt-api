import { Component, Input, OnInit } from "@angular/core";

import { of } from "rxjs";
import { catchError, switchMap, tap } from "rxjs/operators";

import { environment } from "../../../../environments/environment";
import { ProposalService } from "../../../service/proposal.service";
import {
  ProgressReportsUrls,
  Proposal,
  ProposalProgress,
} from "../../../types/proposal";
import { AutoUnsubcribe, currentSemester } from "../../../utils";

@AutoUnsubcribe()
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
  otherProgressReportsUrls: ProgressReportsUrls | null = null;
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
      .subscribe((p: ProgressReportsUrls) => {
        const _currentSemester = currentSemester();
        this.otherProgressReportsUrls = this.otherProgressReports(p);
        this.currentProgressReportExists = p[_currentSemester] !== undefined;
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

  otherProgressReports(
    progressReportsUrls: ProgressReportsUrls,
  ): ProgressReportsUrls | null {
    let otherProgressReportsUrls: ProgressReportsUrls | null = {
      ...progressReportsUrls,
    };
    const _currentSemester = currentSemester();
    if (progressReportsUrls[_currentSemester]) {
      delete otherProgressReportsUrls[currentSemester()];
    }

    if (Object.keys(otherProgressReportsUrls).length == 0) {
      otherProgressReportsUrls = null;
    }

    return otherProgressReportsUrls;
  }

  progressReportsUrlsMap(
    progressReports: ProgressReportsUrls,
  ): Map<string, { [key: string]: string }> {
    const reportUrlsMap = new Map(Object.entries(progressReports));
    for (const [key, value] of reportUrlsMap) {
      const url = new URL(value["proposalProgressPdf"]);
      const noOriginUrl = url.href.replace(url.origin, "");
      reportUrlsMap.set(key, {
        proposalProgressPdf: this.apiUrl + noOriginUrl,
      });
    }
    return reportUrlsMap;
  }

  onClick(): void {
    this.showReports = !this.showReports;
    this.reportsLinksText = this.showReports
      ? "Hide progress reports for other semesters"
      : "Show progress reports for other semesters";
  }
}
