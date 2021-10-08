import { AccessToken } from './types/authentication';

export const GENERIC_ERROR_MESSAGE =
  'Sorry, something has gone wrong. Please try again later.';

export function storeAccessToken(tokenData: AccessToken) {
  localStorage.setItem('accessToken', tokenData.accessToken);
  localStorage.setItem('expiresAt', tokenData.expiresAt);
}
