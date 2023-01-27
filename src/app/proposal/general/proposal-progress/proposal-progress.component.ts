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
  progressReportsUrls: ProgressReportsUrls | null = null;
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
        this.progressReportsUrls = p;
        if (this.progressReportsUrls[currentSemester()]) {
          delete this.progressReportsUrls[currentSemester()];
        }

        if (Object.keys(this.progressReportsUrls).length == 0) {
          this.progressReportsUrls = null;
        }
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
