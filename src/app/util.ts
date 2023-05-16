import add from "date-fns/add";
import sub from "date-fns/sub";

import {
  FinderChart,
  FinderChartFileType,
  FinderChartSize,
} from "./types/observation";

export function semesterOfDatetime(t: Date): string {
  /**
   Return the semester in which a datetime lies.

   The semester is returned as a string of the form "year-semester", such as "2020-2"
   or "2021-1". Semester 1 of a year starts on 1 May noon UTC, semester 2 starts on
   1 November noon UTC.

   The given datetime must be timezone-aware.
   */
  let semester = 2;
  let year = t.getUTCFullYear();

  if (t.getMonth() >= 4 && t.getMonth() < 10) {
    semester = 1;
  }
  if (t.getMonth() < 4) {
    year -= 1;
  }
  return `${year}-${semester}`;
}

export function getNextSemester(): string {
  const currentSemester = semesterOfDatetime(new Date()).split("-");
  let year = currentSemester[0];
  let semester = currentSemester[1];
  if (parseInt(semester) === 1) {
    semester = "2";
  } else {
    semester = "1";
    year = `${parseInt(year) + 1}`;
  }
  return `${year}-${semester}`;
}

export function finderChartURL(
  finderChart: FinderChart,
  acceptableSizes: FinderChartSize[],
  acceptableFileTypes: FinderChartFileType[],
  baseURL: string,
): string | null {
  /*
  Return the URL for a finder chart.

  The lists of acceptable file types must be ordered hy preference, the most preferred
  option being the first list item.
   */
  for (const size of acceptableSizes) {
    for (const fileType of acceptableFileTypes) {
      const file = finderChart.files.find(
        (f) => f.size === size && f.url.endsWith("." + fileType),
      );
      if (file) {
        return baseURL + file.url;
      }
    }
  }

  return null;
}

/**
 * Return the start and end time of the current Julian day.
 *
 * The Julian days starts and ends at noon UTC.
 */
export function currentJulianDay(): { start: Date; end: Date } {
  const now = new Date();
  const nowHours = now.getUTCHours();
  let start = new Date(
    Date.UTC(
      now.getUTCFullYear(),
      now.getUTCMonth(),
      now.getUTCDate(),
      12,
      0,
      0,
      0,
    ),
  );
  if (nowHours < 12) {
    start = sub(start, { days: 1 });
  }
  const end = add(start, { days: 1 });

  return { start, end };
}

export function secondsToHhMmSs(time: number): string {
  if (time < 0) {
    throw Error(`Can't convert negative seconds: ${time}.`);
  }
  return (
    Math.floor(time / 3600).toLocaleString("en-US", {
      minimumIntegerDigits: 2,
      useGrouping: false,
    }) +
    ":" +
    Math.floor((time % 3600) / 60).toLocaleString("en-US", {
      minimumIntegerDigits: 2,
      useGrouping: false,
    }) +
    ":" +
    ((time % 3600) % 60).toLocaleString("en-US", {
      minimumIntegerDigits: 2,
      useGrouping: false,
    })
  );
}
