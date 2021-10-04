import { AccessToken } from './types/authentication';

export function storeAccessToken(tokenData: AccessToken) {
  localStorage.setItem('accessToken', tokenData.accessToken);
  localStorage.setItem('expiresAt', tokenData.expiresAt);
}
