import { AccessToken } from './types/authentication';

export const GENERIC_ERROR_MESSAGE =
  'Sorry, something has gone wrong. Please try again later.';

export const NOT_LOGGED_IN_MESSAGE = 'You are not logged in.';

export const FORBIDDEN_MESSAGE = 'You are not allowed to perform this action.';

export function storeAccessToken(tokenData: AccessToken) {
  localStorage.setItem('accessToken', tokenData.accessToken);
  localStorage.setItem('accessTokenExpiresAt', tokenData.expiresAt);
}

export function currentSemester() {
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

export type sortArg<T> =
  | keyof T
  | `-${string & keyof T}`
  | `+${string & keyof T}`;
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
export function byPropertiesOf<T extends object>(sortBy: Array<sortArg<T>>) {
  function compareByProperty(arg: sortArg<T>) {
    let key: keyof T;
    let sortOrder = 1;
    if (typeof arg === 'string' && arg.startsWith('-')) {
      sortOrder = -1;
      // Typescript is not yet smart enough to infer that substring is keyof T
      key = arg.substr(1) as keyof T;
    } else if (typeof arg === 'string' && arg.startsWith('+')) {
      // Typescript is not yet smart enough to infer that substring is keyof T
      key = arg.substr(1) as keyof T;
    } else {
      // Likewise it is not yet smart enough to infer that arg is not keyof T
      key = arg as keyof T;
    }
    return function (a: T, b: T) {
      const result = a[key] < b[key] ? -1 : a[key] > b[key] ? 1 : 0;

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
export function degreesToHms(deg: number, decimal_places: number = 2): string {
  if (deg < 0) {
    throw new Error('The degrees must be non-negative');
  }

  let hours = Math.floor(deg / 15);
  let minutes = Math.floor((deg / 15 - hours) * 60);
  let seconds =
    Math.round(
      (deg / 15 - hours - minutes / 60) * 3600 * Math.pow(10, decimal_places)
    ) / Math.pow(10, decimal_places);

  seconds >= 60 && (minutes++, (seconds = 0)); //if seconds rounds to 60 then increment minutes, reset seconds
  minutes == 60 && (hours++, (minutes = 0)); //if minutes rounds to 60 then increment hours, reset minutes

  const ra_h = hours < 10 ? '0' + String(hours) : String(hours);
  const ra_m = minutes < 10 ? '0' + String(minutes) : String(minutes);
  const ra_s =
    seconds < 10
      ? '0' + seconds.toFixed(decimal_places)
      : seconds.toFixed(decimal_places);

  return ra_h + ':' + ra_m + ':' + ra_s;
}

// @ input {deg}     Numeric; degrees number to convert
// @ input {decimal_places} Decimal places to use for output seconds
//                   Default 2 places
// @ return {DMS} string degrees : minutes : seconds
//
// reference https://stackoverflow.com/a/61961361
export function degreesToDms(deg: number, decimal_places: number = 2): string {
  const sign = deg < 0 ? -1 : 1;
  deg = Math.abs(deg);

  let degrees = Math.floor(deg);
  let arcminutes = Math.floor((deg - degrees) * 60);
  let arcseconds =
    Math.round(
      (deg - degrees - arcminutes / 60) * 3600 * Math.pow(10, decimal_places)
    ) / Math.pow(10, decimal_places);

  arcseconds >= 60 && (arcminutes++, (arcseconds = 0)); //if arcseconds rounds to 60 then increment minutes, reset seconds
  arcminutes == 60 && (degrees++, (arcminutes = 0)); //if arcminutes rounds to 60 then increment degrees, reset minutes

  const dec_degrees = degrees < 10 ? '0' + String(degrees) : String(degrees);
  const dec_arcminutes =
    arcminutes < 10 ? '0' + String(arcminutes) : String(arcminutes);
  const dec_arcseconds =
    arcseconds < 10
      ? '0' + arcseconds.toFixed(decimal_places)
      : arcseconds.toFixed(decimal_places);

  const dms_string = dec_degrees + ':' + dec_arcminutes + ':' + dec_arcseconds;

  return sign < 0 ? '-' + dms_string : '+' + dms_string;
}
