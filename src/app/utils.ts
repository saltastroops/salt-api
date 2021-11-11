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
