import { Component, Input, OnInit } from '@angular/core';
import {
  addDays,
  subDays,
  differenceInSeconds,
  addHours,
  parseISO,
} from 'date-fns';
import { TimeInterval } from '../../../../types/common';

type ObservingWindow = { start: Date; end: Date };

@Component({
  selector: 'wm-observing-windows',
  templateUrl: './observing-windows.component.html',
  styleUrls: ['./observing-windows.component.scss'],
})
export class ObservingWindowsComponent implements OnInit {
  @Input('observingWindows') stringObservingWindows!: TimeInterval[];

  observingWindows!: ObservingWindow[];
  showObservingWindow = false;
  blocksObservableTonight!: ObservingWindow[];
  remainingNights!: number;
  differenceInSeconds = differenceInSeconds; // It needs to be an attribute of the class to be used in the template.
  constructor() {}

  ngOnInit(): void {
    this.observingWindows = this.stringObservingWindows.map(
      ({ start, end }) => ({ start: parseISO(start), end: parseISO(end) })
    );
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
    let start = this.nightStart(new Date());
    const end = addDays(start, 1);
    return { start, end };
  }

  tonightsObservingWindows(): ObservingWindow[] {
    const night = this.tonight();
    const tonightsWindows = this.observingWindows.filter(
      (o) => o.end >= night.start && o.end < night.end
    );
    return tonightsWindows.sort(this._compareObservingWindows);
  }

  toggleObservingWindows(): void {
    this.showObservingWindow = !this.showObservingWindow;
  }

  numberOfObservableNightsRemaining(): number {
    const tomorrow = addDays(this.tonight().start, 1);
    const remainingWindows = this.observingWindows.filter(
      (o: ObservingWindow) => tomorrow <= o.start
    );
    const remainingNights = new Set(
      remainingWindows.map((w) => this.nightStart(w.start))
    );
    return remainingNights.size;
  }

  sortedObservingWindows(): ObservingWindow[] {
    return [...this.observingWindows].sort(this._compareObservingWindows);
  }

  _compareObservingWindows(a: ObservingWindow, b: ObservingWindow): number {
    return a.start.getTime() - b.start.getTime();
  }
}
