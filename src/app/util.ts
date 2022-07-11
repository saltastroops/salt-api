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

  if (t.getMonth() >= 4 && t.getMonth() < 9) {
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
