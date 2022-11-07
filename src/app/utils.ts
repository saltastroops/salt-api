import { User, UserRole } from "./types/user";

export const GENERIC_ERROR_MESSAGE =
  "Sorry, something has gone wrong. Please try again later.";

export const NOT_LOGGED_IN_MESSAGE = "You are not logged in.";

export const FORBIDDEN_MESSAGE = "You are not allowed to perform this action.";

export function currentSemester(): string {
  const now = new Date();
  const year = now.getFullYear();
  const month = now.getMonth();
  if (month < 4) {
    return `${year - 1}-2`;
  } else if (month < 10) {
    return `${year}-1`;
  } else {
    return `${year}-2`;
  }
}

/* eslint-disable  @typescript-eslint/no-explicit-any */
// @ts-ignore
type NestedKeyOf<T extends Record<string, any>> = {
  [Key in keyof T & (string | number)]: T[Key] extends Record<string, any>
    ? // @ts-ignore
      `${Key}` | `${Key}.${NestedKeyOf<T[Key]>}`
    : `${Key}`;
}[keyof T & (string | number)];

export type sortArg<T> =
  | keyof T
  | NestedKeyOf<T>
  | `-${string & keyof T}`
  | `+${string & keyof T}`
  | `-${string & NestedKeyOf<T>}`
  | `+${string & NestedKeyOf<T>}`;
/**
 * Returns a comparator for objects of type T that can be used by sort
 * functions, where T objects are compared by the specified T properties.
 *
 * @param sortBy - the names of the properties to sort by, in precedence order.
 *                 Prefix any name with `-` to sort it in descending order or
 *                 with '+' to sort in ascending order.
 *
 * referece: https://stackoverflow.com/a/68279093/8910547
 */
export function byPropertiesOf<T>(
  sortBy: Array<sortArg<T>>,
): (a: T, b: T) => number {
  function compareByProperty(arg: sortArg<T>) {
    let key: keyof T;
    let sortOrder = 1;
    if (typeof arg === "string" && arg.startsWith("-")) {
      sortOrder = -1;
      // Typescript is not yet smart enough to infer that substring is keyof T
      key = arg.substr(1) as keyof T;
    } else if (typeof arg === "string" && arg.startsWith("+")) {
      // Typescript is not yet smart enough to infer that substring is keyof T
      key = arg.substr(1) as keyof T;
    } else {
      // Likewise it is not yet smart enough to infer that arg is not keyof T
      key = arg as keyof T;
    }
    return function (a: T, b: T) {
      let result;
      if (typeof a[key] === "string") {
        if (
          (a[key] as unknown as string).toLocaleUpperCase() <
          (b[key] as unknown as string).toLocaleUpperCase()
        ) {
          result = -1;
        } else if (
          (a[key] as unknown as string).toLocaleUpperCase() >
          (b[key] as unknown as string).toLocaleUpperCase()
        ) {
          result = 1;
        } else {
          result = 0;
        }
      } else {
        const key_split = key.toString().split(".");
        if (key_split.length > 1) {
          key = key_split[0] as keyof T;
          const subkey = key_split[1] as keyof T[keyof T];
          if (a[key][subkey] < b[key][subkey]) {
            result = -1;
          } else if (a[key][subkey] > b[key][subkey]) {
            result = 1;
          } else {
            result = 0;
          }
        } else {
          if (a[key] < b[key]) {
            result = -1;
          } else if (a[key] > b[key]) {
            result = 1;
          } else {
            result = 0;
          }
        }
      }
      return result * sortOrder;
    };
  }

  return function (obj1: T, obj2: T) {
    let i = 0;
    let result = 0;
    const numberOfProperties = sortBy.length;
    while (result === 0 && i < numberOfProperties) {
      result = compareByProperty(sortBy[i])(obj1, obj2);
      i++;
    }

    return result;
  };
}

// @ input {deg}     Numeric; degrees number to convert
// @ input {decimal_places} Decimal places to use for output seconds
//                   Default 2 places
// @ return {HMS} string hours : minutes : seconds
//
// reference https://stackoverflow.com/a/61961361
export function degreesToHms(deg: number, decimal_places = 2): string {
  if (deg < 0) {
    throw new Error("The degrees must be non-negative");
  }

  let hours = Math.floor(deg / 15);
  let minutes = Math.floor((deg / 15 - hours) * 60);
  let seconds =
    Math.round(
      (deg / 15 - hours - minutes / 60) * 3600 * Math.pow(10, decimal_places),
    ) / Math.pow(10, decimal_places);

  seconds >= 60 && (minutes++, (seconds = 0)); //if seconds rounds to 60 then increment minutes, reset seconds
  minutes == 60 && (hours++, (minutes = 0)); //if minutes rounds to 60 then increment hours, reset minutes

  const ra_h = hours < 10 ? "0" + String(hours) : String(hours);
  const ra_m = minutes < 10 ? "0" + String(minutes) : String(minutes);
  const ra_s =
    seconds < 10
      ? "0" + seconds.toFixed(decimal_places)
      : seconds.toFixed(decimal_places);

  return ra_h + ":" + ra_m + ":" + ra_s;
}

// @ input {deg}     Numeric; degrees number to convert
// @ input {decimal_places} Decimal places to use for output seconds
//                   Default 2 places
// @ return {DMS} string degrees : minutes : seconds
//
// reference https://stackoverflow.com/a/61961361
export function degreesToDms(deg: number, decimal_places = 2): string {
  const sign = deg < 0 ? -1 : 1;
  deg = Math.abs(deg);

  let degrees = Math.floor(deg);
  let arcminutes = Math.floor((deg - degrees) * 60);
  let arcseconds =
    Math.round(
      (deg - degrees - arcminutes / 60) * 3600 * Math.pow(10, decimal_places),
    ) / Math.pow(10, decimal_places);

  arcseconds >= 60 && (arcminutes++, (arcseconds = 0)); //if arcseconds rounds to 60 then increment minutes, reset seconds
  arcminutes == 60 && (degrees++, (arcminutes = 0)); //if arcminutes rounds to 60 then increment degrees, reset minutes

  const dec_degrees = degrees < 10 ? "0" + String(degrees) : String(degrees);
  const dec_arcminutes =
    arcminutes < 10 ? "0" + String(arcminutes) : String(arcminutes);
  const dec_arcseconds =
    arcseconds < 10
      ? "0" + arcseconds.toFixed(decimal_places)
      : arcseconds.toFixed(decimal_places);

  const dms_string = dec_degrees + ":" + dec_arcminutes + ":" + dec_arcseconds;

  return sign < 0 ? "-" + dms_string : "+" + dms_string;
}

export function availableSemesters(): string[] {
  const startYear = 2006;
  const endYear = new Date().getFullYear() + 5;
  const semesters: string[] = [];
  for (let year = startYear; year <= endYear; year++) {
    semesters.push(`${year}-1`, `${year}-2`);
  }
  return semesters;
}

export function nextSemesterOf(semester: string): string {
  const semester_regex = new RegExp("^20d{2}-[12]");

  if (semester_regex.test(semester)) {
    throw new Error("incorrect semester format");
  }
  const year_sem = semester.split("-");
  let year = Number(year_sem[0]);
  let sem = Number(year_sem[1]);
  if (sem === 2) {
    year += 1;
    sem = 1;
  } else {
    sem = 2;
  }
  return `${year}-${sem}`;
}

// @ input {input}  String; the right ascension.
//
// @ return {Degrees} Number;
export function convertRightAscensionHMSToDegrees(input: string): number {
  if (!input) {
    throw Error("Right ascension should not be an empty string.");
  }

  if (!/^[+-]?\d{1,2}(([:; "']\d{1,2})?[:; "']\d{1,2}(\.\d*)?)?$/.test(input)) {
    throw Error("Right ascension is invalid.");
  }

  const parts = input.split(/[:; "']/);
  const hours = Number(parts[0]);
  const minutes = parts[1] === undefined ? 0 : Number(parts[1]);
  const seconds = parts[2] === undefined ? 0 : Number(parts[2]);

  if (hours < 0) {
    throw new Error("Hours cannot be less than 0");
  }

  if (hours >= 24) {
    throw new Error("Hours should be a value between 0 and 23.");
  }
  if (minutes >= 60) {
    throw new Error("Minutes cannot be greater than or equal to 60.");
  }
  if (seconds >= 60) {
    throw new Error("Seconds cannot be greater than or equal to 60.");
  }
  return (hours + minutes / 60 + seconds / (60 * 60)) * 15;
}

export function previousSemesterOf(semester: string): string {
  const semester_regex = new RegExp("^20d{2}-[12]");

  if (semester_regex.test(semester)) {
    throw new Error("incorrect semester format");
  }
  const year_sem = semester.split("-");
  let year = Number(year_sem[0]);
  let sem = Number(year_sem[1]);
  if (sem === 1) {
    year -= 1;
    sem = 2;
  } else {
    sem = 1;
  }

  return `${year}-${sem}`;
}

// reference https://blog.bitsrc.io/6-ways-to-unsubscribe-from-observables-in-angular-ab912819a78f
// 5. Use Decorator to automate Unsubscription
// This decorator can only work when there is a subscription property.
export function AutoUnsubcribe() {
  return function (constructor: any): void {
    // eslint-disable-line
    const orig = constructor.prototype.ngOnDestroy;
    constructor.prototype.ngOnDestroy = function () {
      for (const prop in this) {
        const property = this[prop];
        if (typeof property?.unsubscribe === "function") {
          property.unsubscribe();
        }
      }
      orig?.apply();
    };
  };
}

export function hasAnyRole(user: User, roles: UserRole[]): boolean {
  if (user.roles.includes("Administrator")) {
    return true;
  }
  return user.roles.some((role) => roles.includes(role));
}
