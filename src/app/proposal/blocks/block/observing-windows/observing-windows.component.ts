import { Component, Input, OnChanges } from "@angular/core";

import {
  addDays,
  addHours,
  differenceInSeconds,
  parseISO,
  subDays,
} from "date-fns";

import { TimeInterval } from "../../../../types/common";

type ObservingWindow = { start: Date; end: Date };

@Component({
  selector: "wm-observing-windows",
  templateUrl: "./observing-windows.component.html",
  styleUrls: ["./observing-windows.component.scss"],
})
export class ObservingWindowsComponent implements OnChanges {
  @Input() observingWindows!: TimeInterval[];

  observingWindowList!: ObservingWindow[];
  showObservingWindow = false;
  blocksObservableTonight!: ObservingWindow[];
  remainingNights!: number;
  differenceInSeconds = differenceInSeconds; // It needs to be an attribute of the class to be used in the template.

  ngOnChanges(): void {
    this.observingWindowList = this.observingWindows.map(({ start, end }) => ({
      start: parseISO(start),
      end: parseISO(end),
    }));
    this.blocksObservableTonight = this.tonightsObservingWindows();
    this.remainingNights = this.numberOfObservableNightsRemaining();
  }

  nightStart(t: Date): Date {
    const millisecondsSinceMidnightUTC = t.getTime() % 86400000; // 86400 == 1 day
    const midnightUTC = new Date(t.getTime() - millisecondsSinceMidnightUTC);
    let noonUTC = addHours(midnightUTC, 12);
    if (millisecondsSinceMidnightUTC < 43200000) {
      // 43200000 == 12 hours
      // The time is between 0:00 and 12:00 UTC, and hence the night starts on the
      // previous day.
      noonUTC = subDays(noonUTC, 1);
    }
    return new Date(noonUTC);
  }

  tonight(): { start: Date; end: Date } {
    const start = this.nightStart(new Date());
    const end = addDays(start, 1);
    return { start, end };
  }

  tonightsObservingWindows(): ObservingWindow[] {
    const night = this.tonight();
    const tonightsWindows = this.observingWindowList.filter(
      (o) => o.end >= night.start && o.end < night.end,
    );
    return tonightsWindows.sort(this._compareObservingWindows);
  }

  toggleObservingWindows(): void {
    this.showObservingWindow = !this.showObservingWindow;
    const element = document.getElementById("observing-windows");
    if (!this.showObservingWindow) {
      element?.scrollIntoView();
    }
  }

  numberOfObservableNightsRemaining(): number {
    const tomorrow = addDays(this.tonight().start, 1);
    const remainingWindows = this.observingWindowList.filter(
      (o: ObservingWindow) => tomorrow <= o.start,
    );
    const remainingNights = new Set(
      remainingWindows.map((w) => this.nightStart(w.start)),
    );
    return remainingNights.size;
  }

  sortedObservingWindows(): ObservingWindow[] {
    return [...this.observingWindowList].sort(this._compareObservingWindows);
  }

  _compareObservingWindows(a: ObservingWindow, b: ObservingWindow): number {
    return a.start.getTime() - b.start.getTime();
  }
}
